#![allow(clippy::missing_errors_doc)] // FIXME

use std::ops::ControlFlow;

use nonempty::NonEmpty;
use pyo3::{intern, prelude::*};
use rand::SeedableRng;
use sorted_vec::SortedSet;

use core_compressor::compressor::ConcreteCompressor;
use core_dataset::{
    dataset::Dataset,
    variable::{derivative::DataDerivative, DataVariable},
};

pub mod case;
pub mod error;
mod goodness;
pub mod measuring;
mod performance;
pub mod report;
pub mod reporter;
pub mod settings;

use crate::{
    case::BenchmarkCase,
    error::BenchmarkSingleCaseError,
    goodness::{compute_derivatives_goodness_measurements, compute_goodness_measurements},
    measuring::Measurements,
    performance::compress_and_perform_performance_measurements,
    report::BenchmarkCaseOutput,
    settings::{BenchmarkSettings, ErrorSettings},
};

pub fn run_benchmark_case<'a>(
    dataset: &'a Dataset,
    variable: &'a DataVariable,
    compressor: &ConcreteCompressor<'a>,
    settings: &BenchmarkSettings,
) -> Result<BenchmarkCaseOutput, BenchmarkSingleCaseError> {
    let mut rng = rand_chacha::ChaChaRng::seed_from_u64(settings.measurements.bootstrap.seed);

    let py_data_array = Python::with_gil(|py| {
        dataset
            .open_xarray_sliced_variable(py, variable)
            .map(|da| da.to_object(py))
    })?;

    let num_measurements = settings.measurements.num_repeats.get() * variable.num_reductions();

    let mut measurements = Measurements::new(
        num_measurements,
        settings.measurements.error.resamples.get(),
        variable.derivatives().len(),
        compressor.codecs().len(),
    );

    for it in 0..settings.measurements.num_repeats.get() {
        let mut reductions = variable.iter_reductions();

        loop {
            let Some(sliced_py_data_array) =
                Python::with_gil(|py| -> Result<_, BenchmarkSingleCaseError> {
                    reductions
                        .next(py)
                        .map(|reduction| {
                            py_data_array
                                .as_ref(py)
                                .get_item(reduction)
                                .map(|da| da.to_object(py))
                                .map_err(BenchmarkSingleCaseError::from)
                        })
                        .transpose()
                })?
            else {
                break;
            };

            run_benchmark_iteration_and_perform_measurements(
                compressor,
                variable.derivatives(),
                &sliced_py_data_array,
                &mut measurements,
                &settings.measurements.error,
                it == 0,
                settings.measurements.bootstrap.seed,
            )?;

            // Temporarily allow other code to run
            Python::with_gil(|py| py.allow_threads(|| ()));

            // We don't drop inside the GIL since the GIL is acquired in the next
            //  iteration and after all iterations anyways
            std::mem::drop(sliced_py_data_array);
        }
    }

    Ok(BenchmarkCaseOutput {
        stats: measurements.analyse(&mut rng, settings.measurements.bootstrap.samples)?,
    })
}

fn run_benchmark_iteration_and_perform_measurements(
    compressor: &ConcreteCompressor,
    derivatives: &SortedSet<NonEmpty<DataDerivative>>,
    py_data_array: &Py<PyAny>,
    measurements: &mut Measurements,
    error_settings: &ErrorSettings,
    compute_goodness: bool,
    seed: u64,
) -> Result<(), BenchmarkSingleCaseError> {
    let ControlFlow::Continue((py_data_array_computed, py_data_array_compressed)) =
        Python::with_gil(|py| {
            py.with_pool(|py| -> Result<_, BenchmarkSingleCaseError> {
                let py_data_array_compressed = compress_and_perform_performance_measurements(
                    py,
                    compressor,
                    py_data_array.as_ref(py),
                    measurements,
                )?;

                if !compute_goodness {
                    return Ok(ControlFlow::Break(()));
                }

                // Eagerly pre-load the uncompressed dataset to speed up analysis
                let py_data_array = py_data_array
                    .as_ref(py)
                    .call_method0(intern!(py, "compute"))?;

                compute_goodness_measurements(
                    py,
                    py_data_array,
                    py_data_array_compressed,
                    &mut measurements.goodness.head,
                    error_settings,
                    seed,
                )?;

                Ok(ControlFlow::Continue((
                    py_data_array.to_object(py),
                    py_data_array_compressed.to_object(py),
                )))
            })
        })?
    else {
        return Ok(());
    };

    compute_derivatives_goodness_measurements(
        derivatives,
        py_data_array_computed,
        py_data_array_compressed,
        &mut measurements.goodness.tail,
        error_settings,
        seed,
    )?;

    Ok(())
}
