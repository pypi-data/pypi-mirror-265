use std::{
    path::{Path, PathBuf},
    sync::Arc,
};

use pyo3::{
    exceptions::PyRuntimeError,
    intern,
    prelude::*,
    types::{IntoPyDict, PyString},
    PyTypeInfo,
};
use wasm_component_layer::{Component, Linker, Store};
use wasm_runtime_layer::Engine;

use core_error::LocationError;

use crate::{codec::WasmCodec, engine::ValidatedEngine, error::PyLocationErr, WasmCodecError};

#[pyclass(frozen)]
pub struct WasmCodecTemplate {
    _path: PathBuf,
    engine: Engine<ValidatedEngine<crate::WasmEngine>>,
    component: Component,
    linker: Linker,
}

#[pymethods]
impl WasmCodecTemplate {
    #[staticmethod]
    pub fn load(_py: Python, path: PathBuf) -> Result<Self, PyLocationErr> {
        Self::new(path).map_err(|err| {
            err.map(|err| PyRuntimeError::new_err(format!("{err:#}")))
                .into()
        })
    }

    pub fn create_codec_class<'py>(
        this: PyRef<'py, Self>,
        py: Python<'py>,
        module: &'py PyModule,
    ) -> Result<&'py PyAny, PyLocationErr> {
        let this: Py<Self> = this.into();
        let (codec_id, signature, documentation) = py
            .with_pool(
                |py| -> Result<(String, String, String), LocationError<WasmCodecError>> {
                    let this = this.borrow(py);
                    let mut plugin = this.instantiate_plugin()?;
                    let codec_id = plugin.codec_id().map_err(WasmCodecError::Wasm)?;
                    let signature = plugin.signature().map_err(WasmCodecError::Wasm)?;
                    let documentation = plugin.documentation().map_err(WasmCodecError::Wasm)?;
                    Ok((codec_id, signature, documentation))
                },
            )
            .map_err(|err| err.map(|err| PyRuntimeError::new_err(format!("{err:#}"))))?;
        let codec_class_name = convert_case::Casing::to_case(&codec_id, convert_case::Case::Pascal);

        let codec_class_bases = (
            WasmCodec::type_object(py),
            py.import(intern!(py, "numcodecs"))?
                .getattr(intern!(py, "abc"))?
                .getattr(intern!(py, "Codec"))?,
        );

        let codec_class_namespace = [
            (intern!(py, "__doc__"), &**PyString::new(py, &documentation)),
            (intern!(py, "codec_id"), PyString::new(py, &codec_id)),
            (
                intern!(py, "__init__"),
                py.eval(&format!("lambda self, {signature}: None"), None, None)?,
            ),
        ]
        .into_py_dict(py);

        let codec_class = py
            .import(intern!(py, "builtins"))?
            .getattr(intern!(py, "type"))?
            .call1((&codec_class_name, codec_class_bases, codec_class_namespace))?;
        codec_class.setattr(intern!(py, "_template"), this.into_py(py))?;
        codec_class.setattr(intern!(py, "__module__"), module.name()?)?;

        module.add(&codec_class_name, codec_class)?;

        py.import(intern!(py, "numcodecs"))?
            .getattr(intern!(py, "registry"))?
            .getattr(intern!(py, "register_codec"))?
            .call1((codec_class,))?;

        Ok(codec_class)
    }

    #[staticmethod]
    pub fn import_codec_class<'py>(
        py: Python<'py>,
        path: PathBuf,
        module: &'py PyModule,
    ) -> Result<&'py PyAny, PyLocationErr> {
        let template = Self::load(py, path)?;
        let template = PyCell::new(py, template)?;

        Self::create_codec_class(template.borrow(), py, module)
    }
}

impl WasmCodecTemplate {
    pub fn new(path: PathBuf) -> Result<Self, LocationError<WasmCodecError>> {
        let wasm_module = Self::load_and_transform_wasm_module(&path)?;

        let engine = Self::new_engine(&path)?;
        let component = Component::new(&engine, &wasm_module)
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?;

        Ok(Self {
            _path: path,
            engine,
            component,
            linker: Linker::default(),
        })
    }

    pub fn instantiate_plugin(
        &self,
    ) -> Result<codecs_core_host::CodecPlugin<ValidatedEngine<crate::WasmEngine>>, WasmCodecError>
    {
        let mut ctx = Store::new(&self.engine, ());

        let instance = self
            .linker
            .instantiate(&mut ctx, &self.component)
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?;

        codecs_core_host::CodecPlugin::new(instance, ctx).map_err(WasmCodecError::Wasm)
    }

    #[allow(clippy::too_many_lines)] // FIXME
    fn load_and_transform_wasm_module(
        path: &Path,
    ) -> Result<Vec<u8>, LocationError<WasmCodecError>> {
        const ROOT_COMPONENT: &str = "fcbench:codec";

        let component = Arc::new(std::fs::read(path).map_err(WasmCodecError::IO)?);

        let imports =
            get_component_ports(&component, |world| world.imports.keys().cloned().collect())?;

        let wasi_components = virtual_wasi_build::ALL_COMPONENTS
            .iter()
            .map(
                |(component_name, component_bytes)| -> Result<_, LocationError<WasmCodecError>> {
                    let component_imports = get_component_ports(component_bytes, |world| {
                        world.imports.keys().cloned().collect()
                    })?;
                    let component_exports = get_component_ports(component_bytes, |world| {
                        world.exports.keys().cloned().collect()
                    })?;

                    Ok((
                        component_name,
                        Arc::new(Vec::from(*component_bytes)),
                        component_imports,
                        component_exports,
                    ))
                },
            )
            .collect::<Result<Vec<_>, _>>()?;

        let mut required_packages_queue = imports
            .iter()
            .map(|(package, _interface)| package.clone())
            .collect::<std::collections::VecDeque<_>>();
        let mut sorted_components = topological_sort::TopologicalSort::new();
        #[allow(clippy::iter_on_single_items)]
        let mut package_providers = [(String::from(ROOT_COMPONENT), String::from(ROOT_COMPONENT))]
            .into_iter()
            .collect::<vecmap::VecMap<_, _>>();
        #[allow(clippy::iter_on_single_items)]
        let mut required_components = [(String::from(ROOT_COMPONENT), imports.into_vec())]
            .into_iter()
            .collect::<vecmap::VecMap<_, _>>();

        while let Some(required_package) = required_packages_queue.pop_front() {
            if package_providers.contains_key(&required_package) {
                continue;
            }

            let Some((component_name, _component_bytes, component_imports, component_exports)) =
                wasi_components.iter().find(
                    |(_component_name, _component_bytes, _component_imports, component_exports)| {
                        component_exports
                            .iter()
                            .any(|(package_name, _exports)| package_name == &required_package)
                    },
                )
            else {
                return Err(LocationError::new(WasmCodecError::Message(format!(
                    "WASM component requires unresolved import(s) from package {required_package}"
                ))));
            };

            for (package, _interface) in component_imports {
                required_packages_queue.push_back(package.clone());
            }

            for (package, _interface) in component_exports {
                package_providers.insert(package.clone(), String::from(**component_name));
            }

            required_components.insert(
                String::from(**component_name),
                component_imports.iter().cloned().collect(),
            );
        }

        for (component_name, imports) in &required_components {
            for (import_package, _import_interface) in imports {
                let Some(provider) = package_providers.get(import_package) else {
                    return Err(LocationError::new(WasmCodecError::Message(format!(
                        "WASM component requires package {import_package} which no component \
                         provides"
                    ))));
                };

                sorted_components.add_link(topological_sort::DependencyLink {
                    prec: provider.clone(),
                    succ: component_name.clone(),
                });
            }
        }

        let mut wac = String::from("package fcbench:codec-virt-wasi;\n\n");

        while let Some(component_name) = sorted_components.pop() {
            let Some(dependencies) = required_components.get(&component_name) else {
                return Err(LocationError::new(WasmCodecError::Message(format!(
                    "BUG: WASM component depends on component {component_name} but it is not a \
                     required dependency"
                ))));
            };

            wac.push_str("let ");
            wac.push_str(&component_name.replace(':', "-"));
            wac.push_str(" = new ");
            wac.push_str(&component_name);
            wac.push_str(" { ");

            let mut first = true;
            for (dependency_package, dependency_interface) in dependencies {
                let Some(dependency_interface) = dependency_interface else {
                    return Err(LocationError::new(WasmCodecError::Message(format!(
                        "WASM component depends on package {dependency_package} without an \
                         interface"
                    ))));
                };

                let Some(provider) = package_providers.get(dependency_package) else {
                    return Err(LocationError::new(WasmCodecError::Message(format!(
                        "WASM component requires package {dependency_package} which no component \
                         provides"
                    ))));
                };

                if !first {
                    wac.push_str(", ");
                }
                first = false;

                wac.push_str(dependency_interface);
                wac.push_str(": ");
                wac.push_str(&provider.replace(':', "-"));
                wac.push('.');
                wac.push_str(dependency_interface);
            }

            wac.push_str(" };\n");
        }

        wac.push_str("\nexport ");
        wac.push_str(&ROOT_COMPONENT.replace(':', "-"));
        wac.push_str(".codecs;\n");

        wac.push_str(
            "\nlet virtual-wasi-perf = new virtual-wasi:perf { };\nexport \
             virtual-wasi-perf.perf;\n",
        );

        let wac_document = wac_parser::ast::Document::parse(&wac)
            .map_err(anyhow::Error::new)
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?;
        let mut wac_packages = required_components
            .iter()
            .map(|(component_name, _component_imports)| {
                if component_name == ROOT_COMPONENT {
                    return Ok((
                        wac_parser::PackageKey {
                            name: component_name,
                            version: None,
                        },
                        component.clone(),
                    ));
                }

                for (
                    wasi_component_name,
                    wasi_component,
                    _wasi_component_imports,
                    _wasi_component_exports,
                ) in &wasi_components
                {
                    if component_name.as_str() == **wasi_component_name {
                        return Ok((
                            wac_parser::PackageKey {
                                name: component_name,
                                version: None,
                            },
                            wasi_component.clone(),
                        ));
                    }
                }

                Err(LocationError::new(WasmCodecError::Message(format!(
                    "BUG: WASM component requires component {component_name} but it could not be \
                     resolved"
                ))))
            })
            .collect::<Result<indexmap::IndexMap<_, _>, _>>()?;

        wac_packages.insert(
            wac_parser::PackageKey {
                name: "virtual-wasi:perf",
                version: None,
            },
            Arc::new(create_instruction_counter_component()?),
        );

        let wac_resolved = wac_parser::Composition::from_ast(&wac_document, wac_packages)
            .map_err(anyhow::Error::new)
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?;

        let wasm = wac_resolved
            .encode(wac_parser::EncodingOptions {
                define_packages: true,
            })
            .map_err(anyhow::Error::msg)
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?;

        wasmparser::Validator::new_with_features(wasmparser::WasmFeatures {
            // MUST: mutable globals do not introduce non-determinism, as long
            //       as the host does not change their value to be non-
            //       deterministic
            mutable_global: true,
            // OK: saturating float -> int conversions only produce finite values
            saturating_float_to_int: true,
            // MUST: arithmetic sign extension operators are deterministic
            sign_extension: true,
            // (unsure): disabled for now, needs further research
            reference_types: false,
            // OK: returning multiple values does not interact with determinism
            multi_value: true,
            // MUST: operations like memcpy and memset are deterministic
            bulk_memory: true,
            // (ok): fixed-width SIMD replicates scalar float semantics
            simd: true,
            // BAD: exposes platform-dependent behaviour and non-determinism
            relaxed_simd: false,
            // BAD: allows non-deterministic concurrency and race conditions
            threads: false,
            // (ok): using tail calls does not interact with determinism
            //       but support is not universal yet:
            //       https://webassembly.org/features/
            tail_call: false,
            // MUST: float operations can introduce non-deterministic NaNs
            floats: true,
            // MUST: using multiple memories does not interact with determinism
            multi_memory: true,
            // (unsure): disabled for now, needs further research
            exceptions: false,
            // (nope): using a 64bit memory space does not interact with
            //         determinism but encourages large memory usage
            memory64: false,
            // (ok): const i[32|64] add, sub, and mul are deterministic
            //       but support is not universal yet:
            //       https://webassembly.org/features/
            extended_const: false,
            // MUST: codecs and reproducible WASI are implemented as components
            component_model: true,
            // (unsure): disabled for now, needs further research
            function_references: false,
            // (unsure): disabled for now, needs further research
            memory_control: false,
            // (unsure): disabled for now, needs further research
            gc: false,
            // OK: using linear values in component init is deterministic, as
            //     long as the values provided are deterministic
            component_model_values: true,
            // OK: nested component names do not interact with determinism
            component_model_nested_names: true,
        })
        .validate_all(&wasm)
        .map_err(anyhow::Error::new)
        .map_err(LocationError::from2)
        .map_err(WasmCodecError::Wasm)?;

        Ok(wasm)
    }
}

#[cfg(feature = "wasmtime")]
impl WasmCodecTemplate {
    // codecs don't need to preallocate the full 4GB wasm32 memory space, but
    //  still give them a reasonable static allocation for better codegen
    const DYNAMIC_MEMORY_GUARD_SIZE: u32 = Self::WASM_PAGE_SIZE /* 64kiB */;
    const DYNAMIC_MEMORY_RESERVED_FOR_GROWTH: u32 = Self::WASM_PAGE_SIZE * 16 * 64 /* 64MiB */;
    const STATIC_MEMORY_GUARD_SIZE: u32 = Self::WASM_PAGE_SIZE * 16 * 64 /* 64MiB */;
    const STATIC_MEMORY_MAXIMUM_SIZE: u32 = Self::WASM_PAGE_SIZE * 16 * 64 /* 64MiB */;
    const WASM_PAGE_SIZE: u32 = 0x10000 /* 64kiB */;

    fn new_engine(
        path: &Path,
    ) -> Result<Engine<ValidatedEngine<crate::WasmEngine>>, LocationError<WasmCodecError>> {
        let mut config = wasmtime::Config::new();
        config
            .cranelift_nan_canonicalization(true)
            .cranelift_opt_level(wasmtime::OptLevel::Speed)
            .static_memory_maximum_size(u64::from(Self::STATIC_MEMORY_MAXIMUM_SIZE))
            .static_memory_guard_size(u64::from(Self::STATIC_MEMORY_GUARD_SIZE))
            .dynamic_memory_guard_size(u64::from(Self::DYNAMIC_MEMORY_GUARD_SIZE))
            .dynamic_memory_reserved_for_growth(u64::from(Self::DYNAMIC_MEMORY_RESERVED_FOR_GROWTH))
            // TODO: allow configuration to be taken from somewhere else
            .cache_config_load(path.with_file_name("wasmtime.toml"))
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?
            // WASM feature restrictions, follows the feature validation in
            //  ValidatedModule::new
            .wasm_bulk_memory(true)
            .wasm_component_model(false)
            .wasm_function_references(false)
            .wasm_memory64(false)
            .wasm_multi_memory(true)
            .wasm_multi_value(true)
            .wasm_reference_types(false)
            .wasm_relaxed_simd(false)
            .wasm_simd(false)
            .wasm_tail_call(false)
            .wasm_threads(false);
        let engine = wasmtime::Engine::new(&config)
            .map_err(LocationError::from2)
            .map_err(WasmCodecError::Wasm)?;
        Ok(Engine::new(ValidatedEngine::new(engine)))
    }
}

#[cfg(feature = "pyodide")]
impl WasmCodecTemplate {
    #[allow(clippy::unnecessary_wraps)]
    fn new_engine(
        _path: &Path,
    ) -> Result<Engine<ValidatedEngine<crate::WasmEngine>>, LocationError<WasmCodecError>> {
        Ok(Engine::new(ValidatedEngine::new(
            pyodide_webassembly_runtime_layer::Engine::default(),
        )))
    }
}

fn get_component_ports(
    component: &[u8],
    get_world_ports: impl Fn(&wit_parser::World) -> Vec<wit_parser::WorldKey>,
) -> Result<vecmap::VecSet<(String, Option<String>)>, LocationError<WasmCodecError>> {
    let component = wit_component::decode_reader(component)
        .map_err(LocationError::from2)
        .map_err(WasmCodecError::Wasm)?;
    let wit_component::DecodedWasm::Component(resolve, world) = component else {
        return Err(LocationError::new(WasmCodecError::Message(String::from(
            "expected WASM component but found package",
        ))));
    };
    let Some(world) = resolve.worlds.get(world) else {
        return Err(LocationError::new(WasmCodecError::Message(String::from(
            "invalid WASM component with dangling root world",
        ))));
    };
    let mut ports = vecmap::VecSet::new();
    for port in get_world_ports(world) {
        let wit_parser::WorldKey::Interface(interface) = port else {
            continue;
        };
        let Some(interface) = resolve.interfaces.get(interface) else {
            return Err(LocationError::new(WasmCodecError::Message(String::from(
                "invalid WASM component with dangling interface",
            ))));
        };
        let Some(package) = interface.package else {
            continue;
        };
        let Some(package) = resolve.packages.get(package) else {
            return Err(LocationError::new(WasmCodecError::Message(String::from(
                "invalid WASM component with dangling package",
            ))));
        };
        ports.insert((format!("{}", package.name), interface.name.clone()));
    }
    Ok(ports)
}

fn create_instruction_counter_component() -> Result<Vec<u8>, LocationError<WasmCodecError>> {
    let mut module = create_instruction_counter_module();

    let mut resolve = wit_parser::Resolve::new();

    let interface = resolve.interfaces.alloc(wit_parser::Interface {
        name: Some(String::from("perf")),
        types: indexmap::IndexMap::new(),
        #[allow(clippy::iter_on_single_items)]
        functions: [(
            String::from("instruction-counter"),
            wit_parser::Function {
                name: String::from("instruction-counter"),
                kind: wit_parser::FunctionKind::Freestanding,
                params: Vec::new(),
                results: wit_parser::Results::Anon(wit_parser::Type::U64),
                docs: wit_parser::Docs { contents: None },
            },
        )]
        .into_iter()
        .collect(),
        docs: wit_parser::Docs { contents: None },
        package: None, // The package is linked up below
    });

    let package_name = wit_parser::PackageName {
        namespace: String::from("wasi"),
        name: String::from("perf"),
        version: Some(semver::Version::new(0, 1, 0)),
    };
    let package = resolve.packages.alloc(wit_parser::Package {
        name: package_name.clone(),
        docs: wit_parser::Docs { contents: None },
        #[allow(clippy::iter_on_single_items)]
        interfaces: [(String::from("perf"), interface)].into_iter().collect(),
        worlds: indexmap::IndexMap::new(),
    });
    resolve.package_names.insert(package_name, package);

    if let Some(interface) = resolve.interfaces.get_mut(interface) {
        interface.package = Some(package);
    }

    let world = resolve.worlds.alloc(wit_parser::World {
        name: String::from("root"),
        imports: indexmap::IndexMap::new(),
        #[allow(clippy::iter_on_single_items)]
        exports: [(
            wit_parser::WorldKey::Interface(interface),
            wit_parser::WorldItem::Interface(interface),
        )]
        .into_iter()
        .collect(),
        package: None, // The package is linked up below
        docs: wit_parser::Docs { contents: None },
        includes: Vec::new(),
        include_names: Vec::new(),
    });

    let root_name = wit_parser::PackageName {
        namespace: String::from("root"),
        name: String::from("component"),
        version: None,
    };
    let root = resolve.packages.alloc(wit_parser::Package {
        name: root_name.clone(),
        docs: wit_parser::Docs { contents: None },
        interfaces: indexmap::IndexMap::new(),
        #[allow(clippy::iter_on_single_items)]
        worlds: [(String::from("root"), world)].into_iter().collect(),
    });
    resolve.package_names.insert(root_name, root);

    if let Some(world) = resolve.worlds.get_mut(world) {
        world.package = Some(root);
    }

    wit_component::embed_component_metadata(
        &mut module,
        &resolve,
        world,
        wit_component::StringEncoding::UTF8,
    )
    .map_err(LocationError::from2)
    .map_err(WasmCodecError::Wasm)?;

    let encoder = wit_component::ComponentEncoder::default()
        .module(&module)
        .map_err(|err| {
            WasmCodecError::Message(format!(
                "wit_component::ComponentEncoder::module failed: {err}"
            ))
        })?;

    let component = encoder.encode().map_err(|err| {
        WasmCodecError::Message(format!(
            "wit_component::ComponentEncoder::encode failed: {err}"
        ))
    })?;

    Ok(component)
}

fn create_instruction_counter_module() -> Vec<u8> {
    let mut module = walrus::Module::with_config(walrus::ModuleConfig::new());

    // We first define just the expored function with an unreachable body,
    //  which is later filled in by the wasm_runtime_layer module wrapper
    let mut function =
        walrus::FunctionBuilder::new(&mut module.types, &[], &[walrus::ValType::I64]);
    function.func_body().unreachable();
    let function = module.funcs.add_local(function.local_func(Vec::new()));

    module
        .exports
        .add("wasi:perf/perf@0.1.0#instruction-counter", function);

    module.emit_wasm()
}
