use std::{borrow::BorrowMut, marker::PhantomData};

use semver::Version;
use wasm_component_layer::{
    ComponentList, ExportInstance, Func, Instance, InterfaceIdentifier, PackageIdentifier,
    PackageName, Store, TypedFunc, Value,
};
use wasm_runtime_layer::backend::WasmEngine;

use core_error::LocationError;

use crate::{codec::WasmCodec, Error};

#[allow(clippy::type_complexity, clippy::module_name_repetitions)]
pub struct CodecPlugin<E: WasmEngine> {
    // FIXME: make typed instead
    from_config: Func,
    pub(crate) encode: Func,
    pub(crate) decode: Func,
    codec_id: TypedFunc<(), String>,
    signature: TypedFunc<(), String>,
    documentation: TypedFunc<(), String>,
    pub(crate) get_config: Func,
    pub(crate) instruction_counter: TypedFunc<(), u64>,
    instance: Instance,
    pub(crate) ctx: Store<(), E>,
}

impl<E: WasmEngine> CodecPlugin<E> {
    pub fn new(instance: Instance, ctx: Store<(), E>) -> Result<Self, LocationError<Error>> {
        fn load_func(interface: &ExportInstance, name: &str) -> Result<Func, LocationError<Error>> {
            let Some(func) = interface.func(name) else {
                return Err(LocationError::from2(anyhow::Error::msg(format!(
                    "WASM component interface does not contain a function named `{name}`"
                ))));
            };

            Ok(func)
        }

        fn load_typed_func<P: ComponentList, R: ComponentList>(
            interface: &ExportInstance,
            name: &str,
        ) -> Result<TypedFunc<P, R>, LocationError<Error>> {
            load_func(interface, name)?
                .typed()
                .map_err(LocationError::from2)
        }

        let codecs_interface_id = InterfaceIdentifier::new(
            PackageIdentifier::new(
                PackageName::new("fcbench", "codec"),
                Some(Version::new(0, 1, 0)),
            ),
            "codecs",
        );
        let Some(codecs_interface) = instance.exports().instance(&codecs_interface_id) else {
            return Err(LocationError::from2(anyhow::Error::msg(format!(
                "WASM component does not contain an interface named `{codecs_interface_id}`"
            ))));
        };

        let perf_interface_id = InterfaceIdentifier::new(
            PackageIdentifier::new(
                PackageName::new("wasi", "perf"),
                Some(Version::new(0, 1, 0)),
            ),
            "perf",
        );
        let Some(perf_interface) = instance.exports().instance(&perf_interface_id) else {
            return Err(LocationError::from2(anyhow::Error::msg(format!(
                "WASM component does not contain an interface named `{perf_interface_id}`"
            ))));
        };

        Ok(Self {
            from_config: load_func(codecs_interface, "[static]codec.from-config")?,
            encode: load_func(codecs_interface, "[method]codec.encode")?,
            decode: load_func(codecs_interface, "[method]codec.decode")?,
            codec_id: load_typed_func(codecs_interface, "codec-id")?,
            signature: load_typed_func(codecs_interface, "signature")?,
            documentation: load_typed_func(codecs_interface, "documentation")?,
            get_config: load_func(codecs_interface, "[method]codec.get-config")?,
            instruction_counter: load_typed_func(perf_interface, "instruction-counter")?,
            instance,
            ctx,
        })
    }

    pub fn codec_id(&mut self) -> Result<String, LocationError<Error>> {
        self.codec_id
            .call(&mut self.ctx, ())
            .map_err(LocationError::from2)
    }

    pub fn signature(&mut self) -> Result<String, LocationError<Error>> {
        self.signature
            .call(&mut self.ctx, ())
            .map_err(LocationError::from2)
    }

    pub fn documentation(&mut self) -> Result<String, LocationError<Error>> {
        self.documentation
            .call(&mut self.ctx, ())
            .map_err(LocationError::from2)
    }

    #[allow(clippy::type_complexity)]
    pub fn from_config<P: BorrowMut<Self>>(
        mut plugin: P,
        config: &str,
    ) -> Result<Result<WasmCodec<E, P>, String>, LocationError<Error>> {
        let plugin_borrow: &mut Self = plugin.borrow_mut();

        let args = Value::String(config.into());
        let mut result = Value::U8(0);

        plugin_borrow
            .from_config
            .call(
                &mut plugin_borrow.ctx,
                std::slice::from_ref(&args),
                std::slice::from_mut(&mut result),
            )
            .map_err(LocationError::from2)?;

        match result {
            Value::Result(result) => match &*result {
                Ok(Some(Value::Own(resource))) => Ok(Ok(WasmCodec {
                    resource: resource.clone(),
                    plugin,
                    instruction_counter: 0,
                    _marker: PhantomData::<E>,
                })),
                Err(Some(Value::String(err))) => Ok(Err(String::from(&**err))),
                result => Err(LocationError::from2(anyhow::Error::msg(format!(
                    "unexpected from-config result value {result:?}"
                )))),
            },
            value => Err(LocationError::from2(anyhow::Error::msg(format!(
                "unexpected from-config result value {value:?}"
            )))),
        }
    }

    pub fn drop(mut self) -> Result<(), LocationError<Error>> {
        let result = self
            .instance
            .drop(&mut self.ctx)
            .map_err(LocationError::from2);

        // We need to forget here instead of using ManuallyDrop since we need
        //  both a mutable borrow to self.plugin and an immutable borrow to
        //  self.resource at the same time
        std::mem::forget(self);

        let errors = result?;
        if errors.is_empty() {
            return Ok(());
        }

        Err(LocationError::from2(anyhow::Error::msg(format!(
            "dropping instance and all of its resources failed: {}",
            errors
                .into_iter()
                .map(|err| format!("{err:#}"))
                .collect::<Vec<_>>()
                .join(" || "),
        ))))
    }
}

impl<E: WasmEngine> Drop for CodecPlugin<E> {
    fn drop(&mut self) {
        std::mem::drop(self.instance.drop(&mut self.ctx));
    }
}
