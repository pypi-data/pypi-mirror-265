use numpy::{Element, PyArray1, PyArrayDyn, PyUntypedArray};
use pyo3::{
    exceptions::{PyRuntimeError, PyTypeError, PyValueError},
    intern,
    prelude::*,
    types::{IntoPyDict, PyBool, PyDict, PyType},
};

use core_error::LocationError;

use crate::{engine::ValidatedEngine, WasmCodecError, WasmCodecTemplate};

#[pyclass(subclass)]
// not frozen as the codec is mutated when WASM is called
pub struct WasmCodec {
    cls_module: String,
    cls_name: String,
    codec: codecs_core_host::WasmCodec<
        ValidatedEngine<crate::WasmEngine>,
        codecs_core_host::CodecPlugin<ValidatedEngine<crate::WasmEngine>>,
    >,
}

#[pymethods]
impl WasmCodec {
    #[new]
    #[classmethod]
    #[pyo3(signature = (**kwargs))]
    fn new<'py>(
        cls: &'py PyType,
        py: Python<'py>,
        kwargs: Option<&'py PyDict>,
    ) -> Result<Self, PyErr> {
        fn new_inner(
            template: &WasmCodecTemplate,
            kwargs: &str,
            cls_module: &str,
            cls_name: &str,
        ) -> Result<WasmCodec, LocationError<WasmCodecError>> {
            let plugin = template.instantiate_plugin()?;

            let codec = codecs_core_host::CodecPlugin::from_config(plugin, kwargs)
                .map_err(WasmCodecError::Wasm)?
                .map_err(WasmCodecError::Message)?;

            Ok(WasmCodec {
                codec,
                cls_module: String::from(cls_module),
                cls_name: String::from(cls_name),
            })
        }

        let cls_module: &str = cls.getattr(intern!(py, "__module__"))?.extract()?;
        let cls_name: &str = cls.name()?;

        let template: &PyCell<WasmCodecTemplate> = cls
            .getattr(intern!(py, "_template"))
            .map_err(|_| {
                PyValueError::new_err(format!(
                    "{cls_module}.{cls_name} is not linked to a WASM codec template, use \
                     WasmCodecTemplate::create_codec_class to create a new WASM codec class with \
                     a template"
                ))
            })?
            .extract()?;
        let template: PyRef<WasmCodecTemplate> = template.try_borrow()?;

        let json_dumps = py
            .import(intern!(py, "json"))?
            .getattr(intern!(py, "dumps"))?;
        let kwargs: Option<&str> = kwargs
            .map(|kwargs| json_dumps.call1((kwargs,)).and_then(PyAny::extract))
            .transpose()?;
        let kwargs = kwargs.unwrap_or("{}");

        new_inner(&template, kwargs, cls_module, cls_name).map_err(|err| {
            PyValueError::new_err(format!(
                "{cls_module}.{cls_name}::from_config(config={kwargs}) failed with:\n{err:#}"
            ))
        })
    }

    fn encode<'py>(&mut self, py: Python<'py>, buf: &'py PyAny) -> Result<&'py PyAny, PyErr> {
        self.process(
            py,
            buf,
            codecs_core_host::WasmCodec::encode,
            &format!("{}.{}::encode", self.cls_module, self.cls_name),
        )
    }

    fn decode<'py>(
        &mut self,
        py: Python<'py>,
        buf: &'py PyAny,
        out: Option<&'py PyAny>,
    ) -> Result<&'py PyAny, PyErr> {
        let ndarray_copy = py
            .import(intern!(py, "numcodecs"))?
            .getattr(intern!(py, "compat"))?
            .getattr(intern!(py, "ndarray_copy"))?;

        let decoded = self.process(
            py,
            buf,
            codecs_core_host::WasmCodec::decode,
            &format!("{}.{}::decode", self.cls_module, self.cls_name),
        )?;

        ndarray_copy.call1((decoded, out))
    }

    fn get_config<'py>(&mut self, py: Python<'py>) -> Result<&'py PyDict, PyErr> {
        let json_loads = py
            .import(intern!(py, "json"))?
            .getattr(intern!(py, "loads"))?;

        let config = self
            .codec
            .get_config()
            .map_err(|err| PyValueError::new_err(format!("{err}")))?
            .map_err(PyValueError::new_err)?;

        json_loads.call1((config,))?.extract()
    }

    #[classmethod]
    fn from_config<'py>(cls: &'py PyType, config: &'py PyDict) -> Result<&'py PyAny, PyErr> {
        // Ensures that cls(**config) is called and an instance of cls is returned
        cls.call((), Some(config))
    }

    fn __repr__(mut this: PyRefMut<Self>, py: Python) -> Result<String, PyErr> {
        let config: &PyDict = this.get_config(py)?;
        let py_this: Py<PyAny> = this.into_py(py);

        let mut repr: String = py_this
            .as_ref(py)
            .get_type()
            .getattr(intern!(py, "__name__"))?
            .extract()?;
        repr.push('(');

        let mut first = true;

        for parameter in config.call_method0(intern!(py, "items"))?.iter()? {
            let (name, value): (&str, &PyAny) = parameter?.extract()?;

            if name == "id" {
                // Exclude the id config parameter from the repr
                continue;
            }

            let value_repr: &str = value.repr()?.extract()?;

            if !first {
                repr.push_str(", ");
            }
            first = false;

            repr.push_str(name);
            repr.push('=');
            repr.push_str(value_repr);
        }

        repr.push(')');

        Ok(repr)
    }

    #[getter]
    const fn instruction_counter(&self) -> u64 {
        self.codec.instruction_counter()
    }
}

impl WasmCodec {
    fn process<'py>(
        &mut self,
        py: Python<'py>,
        buf: &'py PyAny,
        process: impl for<'a> Fn(
            &'a mut codecs_core_host::WasmCodec<
                ValidatedEngine<crate::WasmEngine>,
                codecs_core_host::CodecPlugin<ValidatedEngine<crate::WasmEngine>>,
            >,
            codecs_core::BufferSlice,
            &[usize],
        ) -> Result<
            Result<codecs_core::ShapedBuffer<codecs_core::VecBuffer>, String>,
            LocationError<codecs_core_host::Error>,
        >,
        class_method: &str,
    ) -> Result<&'py PyAny, PyErr> {
        let ensure_contiguous_ndarray_like = py
            .import(intern!(py, "numcodecs"))?
            .getattr(intern!(py, "compat"))?
            .getattr(intern!(py, "ensure_contiguous_ndarray_like"))?;
        let no_flatten = [(intern!(py, "flatten"), &**PyBool::new(py, false))].into_py_dict(py);

        let data: &PyUntypedArray = ensure_contiguous_ndarray_like
            .call((buf,), Some(no_flatten))?
            .extract()?;
        let dtype = data.dtype();

        let processed = if dtype.is_equiv_to(numpy::dtype::<u8>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<u8>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<u16>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<u16>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<u32>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<u32>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<u64>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<u64>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<i8>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<i8>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<i16>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<i16>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<i32>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<i32>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<i64>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<i64>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<f32>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<f32>>()?,
                process,
                class_method,
            )
        } else if dtype.is_equiv_to(numpy::dtype::<f64>(py)) {
            self.process_inner(
                py,
                data.downcast::<PyArrayDyn<f64>>()?,
                process,
                class_method,
            )
        } else {
            Err(PyTypeError::new_err(format!(
                "{class_method} received buffer of unsupported dtype `{dtype}`",
            )))
        }?;

        Ok(processed.as_ref())
    }

    fn process_inner<'py, T: Element>(
        &mut self,
        py: Python<'py>,
        data: &'py PyArrayDyn<T>,
        process: impl for<'a> Fn(
            &'a mut codecs_core_host::WasmCodec<
                ValidatedEngine<crate::WasmEngine>,
                codecs_core_host::CodecPlugin<ValidatedEngine<crate::WasmEngine>>,
            >,
            codecs_core::BufferSlice,
            &[usize],
        ) -> Result<
            Result<codecs_core::ShapedBuffer<codecs_core::VecBuffer>, String>,
            LocationError<codecs_core_host::Error>,
        >,
        class_method: &str,
    ) -> Result<&'py PyUntypedArray, PyErr>
    where
        for<'b> codecs_core::BufferSlice<'b>: From<&'b [T]>,
    {
        let readonly_data = data.try_readonly()?;
        let data_slice = readonly_data.as_slice()?;

        let processed = process(
            &mut self.codec,
            codecs_core::BufferSlice::from(data_slice),
            data.shape(),
        )
        .map_err(|err| PyRuntimeError::new_err(format!("{class_method} failed with: {err}")))?
        .map_err(WasmCodecError::Message)
        .map_err(|err| PyRuntimeError::new_err(format!("{class_method} failed with: {err}")))?;

        let processed_py = {
            // Ensure that the scope of the entire ShapedBuffer ends here
            let processed = std::convert::identity(processed);

            match processed.buffer {
                codecs_core::BufferVec::U8(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::U16(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::U32(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::U64(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::I8(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::I16(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::I32(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::I64(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::F32(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                codecs_core::BufferVec::F64(v) => PyArray1::from_slice(py, &v)
                    .reshape(processed.shape)?
                    .as_untyped(),
                buf => {
                    return Err(PyTypeError::new_err(format!(
                        "{class_method} returned unsupported dtype `{}`",
                        buf.as_slice().ty()
                    )))
                },
            }
        };

        Ok(processed_py)
    }
}
