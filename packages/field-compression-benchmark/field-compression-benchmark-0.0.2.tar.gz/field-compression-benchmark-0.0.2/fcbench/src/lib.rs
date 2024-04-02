#![allow(clippy::missing_errors_doc)] // FIXME
#![allow(clippy::redundant_pub_crate)]

use pyo3::prelude::*;

mod benchmark;
pub mod compressor;
mod dataclass;
mod dataset;
pub mod model;

#[pymodule]
#[pyo3(name = "_fcbench")]
fn fcbench(py: Python, module: &PyModule) -> Result<(), PyErr> {
    let benchmark = benchmark::create_module(py)?;
    let codecs =
        codecs_frontend::init_codecs(py, module).map_err(core_error::LocationError::into_error)?;
    let compressor = compressor::create_module(py)?;
    let dataset = dataset::create_module(py)?;
    let model = model::create_module(py)?;

    module.add_submodule(benchmark)?;
    module.add_submodule(codecs)?;
    module.add_submodule(compressor)?;
    module.add_submodule(dataset)?;
    module.add_submodule(model)?;

    Ok(())
}
