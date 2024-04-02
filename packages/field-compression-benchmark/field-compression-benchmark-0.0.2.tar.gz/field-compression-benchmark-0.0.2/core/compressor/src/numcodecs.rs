use pyo3::{
    exceptions::PyTypeError,
    intern,
    prelude::*,
    types::{IntoPyDict, PyDict, PyType},
};

#[repr(transparent)]
pub struct Codec {
    codec: PyAny,
}

impl Codec {
    pub fn codec_id(&self) -> Result<&str, PyErr> {
        let py = self.codec.py();

        let ty = self.codec.get_type();
        let codec_id = ty.getattr(intern!(py, "codec_id"))?.extract()?;

        Ok(codec_id)
    }

    pub fn encode<'py>(&'py self, buf: &'py PyAny) -> Result<&'py PyAny, PyErr> {
        let py = self.codec.py();

        self.codec.call_method1(intern!(py, "encode"), (buf,))
    }

    pub fn decode<'py>(
        &'py self,
        buf: &'py PyAny,
        out: Option<&'py PyAny>,
    ) -> Result<&'py PyAny, PyErr> {
        let py = self.codec.py();

        self.codec.call_method(
            intern!(py, "decode"),
            (buf,),
            Some([(intern!(py, "out"), out)].into_py_dict(py)),
        )
    }

    pub fn get_config(&self) -> Result<&PyDict, PyErr> {
        let py = self.codec.py();

        self.codec
            .call_method0(intern!(py, "get_config"))?
            .extract()
    }

    pub fn class(&self) -> &PyType {
        self.codec.get_type()
    }

    pub fn from_config<'py>(cls: &'py PyType, config: &'py PyDict) -> Result<&'py Self, PyErr> {
        let py = cls.py();
        let codec = py
            .import(intern!(py, "numcodecs.abc"))?
            .getattr(intern!(py, "Codec"))?;

        if !cls.is_subclass(codec)? {
            return Err(PyErr::new::<PyTypeError, _>(
                "not a subclass of numcodecs.abc.Codec",
            ));
        }

        cls.call_method1(intern!(py, "from_config"), (config,))?
            .extract()
    }
}

impl<'py> FromPyObject<'py> for &'py Codec {
    fn extract(object: &'py PyAny) -> Result<Self, PyErr> {
        let py = object.py();
        let codec = py
            .import(intern!(py, "numcodecs.abc"))?
            .getattr(intern!(py, "Codec"))?;

        if !object.is_instance(codec)? {
            return Err(PyErr::new::<PyTypeError, _>(
                "not an instance of numcodecs.abc.Codec",
            ));
        }

        #[allow(unsafe_code)]
        // Safety:
        // - object is an instance of numcodecs.abc.Codec
        // - Codec is a transparent newtype wrapper around PyAny
        let codec: &'py Codec = unsafe { &*(object as *const PyAny).cast::<Codec>() };

        Ok(codec)
    }
}

impl<'py> ToPyObject for &'py Codec {
    fn to_object(&self, _py: Python) -> PyObject {
        Py::from(&self.codec)
    }
}

impl AsRef<PyAny> for Codec {
    fn as_ref(&self) -> &PyAny {
        &self.codec
    }
}
