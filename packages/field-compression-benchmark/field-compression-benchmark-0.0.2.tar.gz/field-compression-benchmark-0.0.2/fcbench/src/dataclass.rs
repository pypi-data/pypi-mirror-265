use std::{marker::PhantomData, ops::Deref};

use pyo3::{
    exceptions::PyValueError,
    intern,
    prelude::*,
    types::{
        IntoPyDict, PyBool, PyBytes, PyDict, PyFloat, PyInt, PyList, PyMapping, PyString, PyTuple,
    },
    PyTypeInfo,
};
use pythonize::{PythonizeDictType, PythonizeTypes};

pub struct Dataclass<T: serde::Serialize> {
    data: T,
}

impl<T: serde::Serialize> Dataclass<T> {
    #[must_use]
    pub const fn new(data: T) -> Self {
        Self { data }
    }

    #[must_use]
    pub fn into_data(self) -> T {
        self.data
    }

    pub fn output(&self, py: Python) -> Result<DataclassOut<T>, PyErr> {
        DataclassOut::new(&self.data, py)
    }

    pub fn output_frozen(&self, py: Python) -> Result<DataclassOutFrozen<T>, PyErr> {
        DataclassOutFrozen::new(&self.data, py)
    }
}

impl<T: serde::Serialize> Deref for Dataclass<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl<'py, T: serde::Serialize + serde::Deserialize<'py>> FromPyObject<'py> for Dataclass<T> {
    fn extract(obj: &'py PyAny) -> Result<Self, PyErr> {
        let mut depythonizer = pythonize::Depythonizer::from_object(obj);

        match serde_path_to_error::deserialize(&mut depythonizer) {
            Ok(data) => Ok(Self { data }),
            Err(err) => {
                let err_with_path =
                    PyValueError::new_err(format!("failed to extract at {}", err.path()));
                err_with_path.set_cause(obj.py(), Some(PyErr::from(err.into_inner())));
                Err(err_with_path)
            },
        }
    }
}

// TODO: unite with Dataclass once there is a fallible IntoPy
pub struct DataclassOut<T: serde::Serialize> {
    data: Py<PyAny>,
    inner: PhantomData<fn(T)>,
}

impl<T: serde::Serialize> DataclassOut<T> {
    pub fn new(data: &T, py: Python) -> Result<Self, PyErr> {
        match pythonize::pythonize_custom::<PythonizeNamespace, T>(py, data) {
            Ok(data) => Ok(Self {
                data,
                inner: PhantomData::<fn(T)>,
            }),
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

impl<T: serde::Serialize> IntoPy<Py<PyAny>> for DataclassOut<T> {
    fn into_py(self, _py: Python) -> Py<PyAny> {
        self.data
    }
}

pub struct DataclassOutFrozen<T: serde::Serialize> {
    data: Py<PyAny>,
    inner: PhantomData<T>,
}

impl<T: serde::Serialize> DataclassOutFrozen<T> {
    pub fn new(data: &T, py: Python) -> Result<Self, PyErr> {
        match pythonize::pythonize_custom::<PythonizeFrozenDataclass, T>(py, data) {
            Ok(data) => Ok(Self {
                data,
                inner: PhantomData::<T>,
            }),
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

pub struct DataclassRegistry {
    tracer: serde_reflection::Tracer,
    samples: serde_reflection::Samples,
}

impl DataclassRegistry {
    #[must_use]
    pub fn new() -> Self {
        Self {
            tracer: serde_reflection::Tracer::new(
                serde_reflection::TracerConfig::default()
                    .is_human_readable(false)
                    .record_samples_for_newtype_structs(true)
                    .record_samples_for_structs(true)
                    .record_samples_for_tuple_structs(true)
                    .cut_option_exploration(false)
                    .cut_seq_exploration(false)
                    .cut_map_exploration(false)
                    .cut_enum_exploration(false),
            ),
            samples: serde_reflection::Samples::new(),
        }
    }

    pub fn insert<'a, T: serde::Serialize + serde::Deserialize<'a>>(&'a mut self) {
        #[allow(clippy::expect_used)]
        let (_format, _guesses) = self
            .tracer
            .trace_type::<T>(&self.samples)
            .expect("DataclassRegistry::insert failed");
    }

    pub fn insert_with_sample<'a, T: serde::Serialize + serde::Deserialize<'a>>(
        &'a mut self,
        sample: &T,
    ) {
        #[allow(clippy::expect_used)]
        let (_format, _guess) = self
            .tracer
            .trace_value(&mut self.samples, sample)
            .expect("DataclassRegistry::insert_with_sample failed on sample");
    }

    pub fn export(self, py: Python, module: &PyModule) -> Result<(), PyErr> {
        #[allow(clippy::expect_used)]
        let mut registry = self
            .tracer
            .registry()
            .expect("DataclassRegistry::export failed with incomplete types");

        let mut extra_containers = Vec::new();
        for (name, format) in &mut registry {
            if let serde_reflection::ContainerFormat::Enum(variants) = format {
                for format in variants.values_mut() {
                    match &format.value {
                        #[allow(clippy::unreachable)]
                        serde_reflection::VariantFormat::Variable(_) => {
                            unreachable!("{name}::{} is an unresolved variant type", format.name)
                        },
                        serde_reflection::VariantFormat::Unit => (),
                        serde_reflection::VariantFormat::NewType(newtype) => {
                            if name == "Result" && (format.name == "Ok" || format.name == "Err") {
                                extra_containers.push((
                                    format.name.clone(),
                                    serde_reflection::ContainerFormat::Struct(vec![
                                        serde_reflection::Named {
                                            name: format.name.clone(),
                                            value: (**newtype).clone(),
                                        },
                                    ]),
                                ));
                                format.value = serde_reflection::VariantFormat::NewType(Box::new(
                                    serde_reflection::Format::TypeName(format.name.clone()),
                                ));
                            }
                        },
                        #[allow(clippy::unreachable)]
                        serde_reflection::VariantFormat::Tuple(_) => {
                            unreachable!("{name}::{} is an unsupported tuple variant", format.name)
                        },
                        serde_reflection::VariantFormat::Struct(fields) => {
                            let variant_name =
                                format!("{}_{}", Self::normalise_type_name(name), format.name);
                            extra_containers.push((
                                variant_name.clone(),
                                serde_reflection::ContainerFormat::Struct(fields.clone()),
                            ));
                            format.name = variant_name.clone();
                            format.value = serde_reflection::VariantFormat::NewType(Box::new(
                                serde_reflection::Format::TypeName(variant_name),
                            ));
                        },
                    }
                }
            }
        }
        registry.extend(extra_containers);

        for (name, format) in &registry {
            if let serde_reflection::ContainerFormat::Struct(_) = format {
                let name = Self::normalise_type_name(name);
                let ty = Self::container_type_hint(py, &name, format, &registry)?;
                module.add(&name, ty)?;
            }
        }

        Ok(())
    }

    fn normalise_type_name(name: &str) -> String {
        name.split(&['<', '>', ','])
            .filter_map(|path| {
                if path.is_empty() {
                    None
                } else {
                    Some(path.rsplit_once("::").map_or(path, |path| path.1).trim())
                }
            })
            .collect::<Vec<_>>()
            .join("_")
    }

    fn container_type_hint(
        py: Python,
        name: &str,
        format: &serde_reflection::ContainerFormat,
        registry: &serde_reflection::Registry,
    ) -> Result<Py<PyAny>, PyErr> {
        match format {
            serde_reflection::ContainerFormat::UnitStruct => Ok(py.None()),
            serde_reflection::ContainerFormat::NewTypeStruct(inner) => {
                Self::format_type_hint(py, name, Field::Tuple(0), inner, registry)
            },
            serde_reflection::ContainerFormat::TupleStruct(fields) => Ok(PyTuple::type_object(py)
                .get_item(PyTuple::new(
                    py,
                    fields
                        .iter()
                        .enumerate()
                        .map(|(i, field)| {
                            Self::format_type_hint(py, name, Field::Tuple(i), field, registry)
                        })
                        .collect::<Result<Vec<_>, _>>()?,
                ))?
                .into_py(py)),
            serde_reflection::ContainerFormat::Struct(fields) => Ok(py
                .import(intern!(py, "dataclasses"))?
                .getattr(intern!(py, "make_dataclass"))?
                .call(
                    (
                        Self::normalise_type_name(name),
                        PyTuple::new(
                            py,
                            fields
                                .iter()
                                .map(|field| -> Result<_, PyErr> {
                                    Ok((
                                        field.name.as_str(),
                                        Self::format_type_hint(
                                            py,
                                            name,
                                            Field::Struct(&field.name),
                                            &field.value,
                                            registry,
                                        )?,
                                    ))
                                })
                                .collect::<Result<Vec<_>, _>>()?,
                        ),
                    ),
                    Some(
                        [
                            (
                                intern!(py, "bases"),
                                &**PyTuple::new(
                                    py,
                                    [py.import(intern!(py, "collections"))?
                                        .getattr(intern!(py, "abc"))?
                                        .getattr(intern!(py, "Mapping"))?],
                                ),
                            ),
                            (intern!(py, "kw_only"), PyBool::new(py, true)),
                        ]
                        .into_py_dict(py),
                    ),
                )?
                .into_py(py)),
            serde_reflection::ContainerFormat::Enum(variants) => Ok(py
                .import(intern!(py, "typing"))?
                .getattr(intern!(py, "Union"))?
                .get_item(PyTuple::new(
                    py,
                    variants
                        .values()
                        .map(|variant| Self::variant_type_hint(py, name, variant, registry))
                        .collect::<Result<Vec<_>, _>>()?,
                ))?
                .into_py(py)),
        }
    }

    fn variant_type_hint(
        py: Python,
        name: &str,
        variant: &serde_reflection::Named<serde_reflection::VariantFormat>,
        registry: &serde_reflection::Registry,
    ) -> Result<Py<PyAny>, PyErr> {
        let typing = py.import(intern!(py, "typing"))?;

        match &variant.value {
            #[allow(clippy::unreachable)]
            serde_reflection::VariantFormat::Variable(_) => {
                unreachable!("{name}::{} is an unresolved variant type", variant.name)
            },
            serde_reflection::VariantFormat::Unit => Ok(typing
                .getattr(intern!(py, "Literal"))?
                .get_item(&variant.name)?
                .into_py(py)),
            // FIXME: test matching format in the unit tests
            serde_reflection::VariantFormat::NewType(newtype) => match &**newtype {
                serde_reflection::Format::TypeName(newtype) if variant.name.as_str() == newtype => {
                    Self::type_name_hint(py, newtype, registry)
                },
                #[allow(clippy::unreachable)]
                _ => unreachable!(
                    "{name}::{} is an unsupported newtype variant: variant and type name don't \
                     match",
                    variant.name
                ),
            },
            #[allow(clippy::unreachable)]
            serde_reflection::VariantFormat::Tuple(_) => {
                unreachable!("{name}::{} is an unsupported tuple variant", variant.name)
            },
            #[allow(clippy::unreachable)]
            serde_reflection::VariantFormat::Struct(_) => {
                unreachable!(
                    "{name}::{} is an unsupported struct variant - should be handled earlier",
                    variant.name
                )
            },
        }
    }

    fn format_type_hint(
        py: Python,
        name: &str,
        field: Field,
        format: &serde_reflection::Format,
        registry: &serde_reflection::Registry,
    ) -> Result<Py<PyAny>, PyErr> {
        let typing = py.import(intern!(py, "typing"))?;
        let collections_abc = py
            .import(intern!(py, "collections"))?
            .getattr(intern!(py, "abc"))?;

        match format {
            #[allow(clippy::unreachable)]
            serde_reflection::Format::Variable(_) => {
                unreachable!("{name}.{field} is an unresolved field type")
            },
            serde_reflection::Format::TypeName(ty) => Self::type_name_hint(py, ty, registry),
            serde_reflection::Format::Unit => Ok(py.None()),
            serde_reflection::Format::Bool => Ok(PyBool::type_object(py).into_py(py)),
            serde_reflection::Format::I8
            | serde_reflection::Format::I16
            | serde_reflection::Format::I32
            | serde_reflection::Format::I64
            | serde_reflection::Format::I128
            | serde_reflection::Format::U8
            | serde_reflection::Format::U16
            | serde_reflection::Format::U32
            | serde_reflection::Format::U64
            | serde_reflection::Format::U128 => Ok(PyInt::type_object(py).into_py(py)),
            serde_reflection::Format::F32 | serde_reflection::Format::F64 => {
                Ok(PyFloat::type_object(py).into_py(py))
            },
            serde_reflection::Format::Char | serde_reflection::Format::Str => {
                Ok(PyString::type_object(py).into_py(py))
            },
            serde_reflection::Format::Bytes => Ok(PyBytes::type_object(py).into_py(py)),
            serde_reflection::Format::Option(inner) => Ok(typing
                .getattr(intern!(py, "Optional"))?
                .get_item(Self::format_type_hint(py, name, field, inner, registry)?)?
                .into_py(py)),
            serde_reflection::Format::Seq(elem) => Ok(collections_abc
                .getattr(intern!(py, "Sequence"))?
                .get_item(Self::format_type_hint(py, name, field, elem, registry)?)?
                .into_py(py)),
            serde_reflection::Format::Map { key, value } => Ok(collections_abc
                .getattr(intern!(py, "Mapping"))?
                .get_item((
                    Self::format_type_hint(py, name, field, key, registry)?,
                    Self::format_type_hint(py, name, field, value, registry)?,
                ))?
                .into_py(py)),
            serde_reflection::Format::Tuple(elems) => Ok(PyTuple::type_object(py)
                .get_item(
                    elems
                        .iter()
                        .map(|elem| Self::format_type_hint(py, name, field, elem, registry))
                        .collect::<Result<Vec<_>, _>>()?,
                )?
                .into_py(py)),
            serde_reflection::Format::TupleArray { content, size } => {
                let elem = Self::format_type_hint(py, name, field, content, registry)?;
                Ok(PyTuple::type_object(py)
                    .get_item(PyTuple::new(py, (0..*size).map(|_| elem.as_ref(py))))?
                    .into_py(py))
            },
        }
    }

    fn type_name_hint(
        py: Python,
        name: &str,
        registry: &serde_reflection::Registry,
    ) -> Result<Py<PyAny>, PyErr> {
        match registry.get(name) {
            Some(serde_reflection::ContainerFormat::Struct(_)) => Ok(py
                .import(intern!(py, "typing"))?
                .getattr(intern!(py, "ForwardRef"))?
                .call1((Self::normalise_type_name(name),))?
                .into_py(py)),
            Some(format) => Self::container_type_hint(py, name, format, registry),
            #[allow(clippy::panic)]
            None => panic!("{name} is an unresolved type"),
        }
    }
}

#[derive(Clone, Copy)]
enum Field<'a> {
    Tuple(usize),
    Struct(&'a str),
}

impl<'a> std::fmt::Display for Field<'a> {
    fn fmt(&self, fmt: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            Field::Tuple(idx) => fmt.write_fmt(format_args!("{idx}")),
            Field::Struct(name) => fmt.write_str(name),
        }
    }
}

impl<T: serde::Serialize> IntoPy<Py<PyAny>> for DataclassOutFrozen<T> {
    fn into_py(self, _py: Python) -> Py<PyAny> {
        self.data
    }
}

pub enum PythonizeNamespace {}

impl PythonizeTypes for PythonizeNamespace {
    type List = PyList;
    type Map = Self;
}

impl PythonizeDictType for PythonizeNamespace {
    fn create_mapping(py: Python) -> Result<&PyMapping, PyErr> {
        Ok(PyDict::new(py).as_mapping())
    }

    fn create_mapping_with_items<
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> PyResult<&PyMapping> {
        Ok(items.into_py_dict(py).as_mapping())
    }

    fn create_mapping_with_items_name<
        'py,
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python<'py>,
        name: &str,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> Result<&'py PyMapping, PyErr> {
        let items = items.into_py_dict(py);

        let bases = (
            py.import(intern!(py, "types"))?
                .getattr(intern!(py, "SimpleNamespace"))?,
            py.import(intern!(py, "collections"))?
                .getattr(intern!(py, "abc"))?
                .getattr(intern!(py, "Mapping"))?,
        );

        let namespace: &PyDict = py
            .eval(
                "dict(
            __len__ = lambda self: self.__dict__.__len__(),
            __getitem__ = lambda self, key: self.__dict__.__getitem__(key),
            __iter__ = lambda self: self.__dict__.__iter__(),
        )",
                None,
                None,
            )?
            .extract()?;

        let class = py
            .import(intern!(py, "builtins"))?
            .getattr(intern!(py, "type"))?
            .call1((name, bases, namespace))?;

        class.call((), Some(items.into_py_dict(py)))?.extract()
    }
}

pub enum PythonizeFrozenDataclass {}

impl PythonizeTypes for PythonizeFrozenDataclass {
    type List = PyTuple;
    type Map = Self;
}

impl PythonizeDictType for PythonizeFrozenDataclass {
    fn create_mapping(py: Python) -> Result<&PyMapping, PyErr> {
        py.import(intern!(py, "types"))?
            .getattr(intern!(py, "MappingProxyType"))?
            .call1((PyDict::new(py),))?
            .extract()
    }

    fn create_mapping_with_items<
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> PyResult<&PyMapping> {
        py.import(intern!(py, "types"))?
            .getattr(intern!(py, "MappingProxyType"))?
            .call1((items.into_py_dict(py),))?
            .extract()
    }

    fn create_mapping_with_items_name<
        'py,
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python<'py>,
        name: &str,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> Result<&'py PyMapping, PyErr> {
        let items = items.into_py_dict(py);

        let bases = (
            py.import(intern!(py, "collections"))?
                .getattr(intern!(py, "namedtuple"))?
                .call1((name, items.keys()))?,
            py.import(intern!(py, "collections"))?
                .getattr(intern!(py, "abc"))?
                .getattr(intern!(py, "Mapping"))?,
        );

        let namespace: &PyDict = py
            .eval(
                "dict(
            __slots__ = (),
            __contains__ = lambda self, key: self._fields.__contains__(key),
            __getitem__ = lambda self, key: self._asdict().__getitem__(key),
            __iter__ = lambda self: self._fields.__iter__(),
            _asdict = lambda self: { f: v for f, v in zip(self._fields, \
                 type(self).__bases__[0].__iter__(self)) },
        )",
                None,
                None,
            )?
            .extract()?;

        let class = py
            .import(intern!(py, "builtins"))?
            .getattr(intern!(py, "type"))?
            .call1((name, bases, namespace))?;

        class.call((), Some(items.into_py_dict(py)))?.extract()
    }
}
