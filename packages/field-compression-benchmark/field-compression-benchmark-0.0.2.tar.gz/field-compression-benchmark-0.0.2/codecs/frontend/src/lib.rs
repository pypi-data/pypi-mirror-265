#![allow(clippy::missing_errors_doc)] // FIXME

macro_rules! cfg_single_wasm {
    ($item:item) => {
        #[cfg(any(
            all(feature = "wasmtime", not(feature = "pyodide")),
            all(feature = "pyodide", not(feature = "wasmtime")),
        ))]
        $item
    };
    ($($item:item)*) => {
        $(cfg_single_wasm! { $item })*
    }
}

use core_error::LocationError;

mod engine;
mod error;
mod transform;

pub use error::PyLocationErr;

#[derive(Debug, thiserror::Error)]
pub enum WasmCodecError {
    #[error(transparent)]
    Wasm(LocationError<codecs_core_host::Error>),
    #[error(transparent)]
    IO(std::io::Error),
    #[error("{0}")]
    Message(String),
}

cfg_single_wasm! {
    use pyo3::{intern, prelude::*, PyTypeInfo};

    mod codec;
    mod template;

    use codec::WasmCodec;
    pub use template::WasmCodecTemplate;

    #[cfg(feature = "wasmtime")]
    type WasmEngine = wasmtime::Engine;
    #[cfg(feature = "pyodide")]
    type WasmEngine = pyodide_webassembly_runtime_layer::Engine;

    pub fn init_codecs<'py>(py: Python<'py>, module: &'py PyModule) -> Result<&'py PyModule, LocationError<PyErr>> {
        let codecs = PyModule::new(py, "codecs")?;

        codecs.add_class::<WasmCodecTemplate>()?;
        codecs.add_class::<WasmCodec>()?;

        // FIXME: the __module__ is wrong in fcbench and the benchmark suite
        let __module__ = intern!(py, "__module__");
        let module_str = format!("{}.{}", module.name()?, codecs.name()?);

        WasmCodecTemplate::type_object(py).setattr(__module__, &module_str)?;
        WasmCodec::type_object(py).setattr(__module__, module_str)?;

        module.add_submodule(codecs)?;

        Ok(codecs)
    }
}
