#![allow(clippy::redundant_pub_crate)]

use std::time::Duration;

use numpy::PyUntypedArray;
use pyo3::{
    intern,
    prelude::*,
    types::{IntoPyDict, PyBool, PyTuple},
};

use core_error::LocationError;
use core_measure::{measurement::WallTime, Measurable};

use crate::numcodecs;

pub enum DataArrayCompressor {}

impl DataArrayCompressor {
    pub fn compute_compress_decompress<'py>(
        py: Python<'py>,
        da: &'py PyAny,
        compressor: &[&numcodecs::Codec],
    ) -> Result<(&'py PyAny, Vec<CodecPerformanceMeasurement>), LocationError<PyErr>> {
        let xarray_map_blocks = py
            .import(intern!(py, "xarray"))?
            .getattr(intern!(py, "map_blocks"))?;

        let tracker = PyCell::new(
            py,
            CompressorPerformanceTracker {
                per_codec: vec![
                    CodecPerformanceMeasurement {
                        encode_timing: Duration::ZERO,
                        decode_timing: Duration::ZERO,
                        encode_instructions: None,
                        decode_instructions: None,
                        encoded_bytes: 0,
                        decoded_bytes: 0,
                    };
                    compressor.len()
                ],
            },
        )?;

        let kwargs = [
            (intern!(py, "codecs"), &**PyTuple::new(py, compressor)),
            (intern!(py, "tracker"), tracker),
        ]
        .into_py_dict(py);

        // The compression-decompression must run single-threaded since the tracker
        //  requires mutable borrows
        let context = py
            .import(intern!(py, "dask"))?
            .getattr(intern!(py, "config"))?
            .getattr(intern!(py, "set"))?
            .call(
                PyTuple::empty(py),
                Some([(intern!(py, "scheduler"), intern!(py, "synchronous"))].into_py_dict(py)),
            )?;

        context.call_method0(intern!(py, "__enter__"))?;
        let decompressed = (|| -> Result<&PyAny, LocationError<PyErr>> {
            xarray_map_blocks
                .call1((
                    wrap_pyfunction!(compress_decompress_data_array_single_chunk, py)?,
                    da,
                    PyTuple::empty(py),
                    kwargs,
                ))?
                .call_method0(intern!(py, "compute"))
                .map_err(LocationError::new)
        })();
        context.call_method1(
            intern!(py, "__exit__"),
            (Option::<()>::None, Option::<()>::None, Option::<()>::None),
        )?;

        let decompressed = decompressed?;

        let CompressorPerformanceTracker {
            per_codec: measurement,
        } = tracker.replace(CompressorPerformanceTracker {
            per_codec: Vec::new(),
        });

        Ok((decompressed, measurement))
    }
}

pub enum NumpyArrayCompressor {}

impl NumpyArrayCompressor {
    pub fn compress_decompress<'py>(
        py: Python<'py>,
        array: &'py PyUntypedArray,
        compressor: Vec<&'py crate::numcodecs::Codec>,
    ) -> Result<(&'py PyUntypedArray, Vec<CodecPerformanceMeasurement>), LocationError<PyErr>> {
        let numpy = py.import(intern!(py, "numpy"))?;

        // ensure that the uncompressed data is in a unique and contiguous array
        let array: &PyUntypedArray = {
            let contiguous: &PyUntypedArray = numpy
                .getattr(intern!(py, "ascontiguousarray"))?
                .call1((array,))?
                .extract()?;
            if contiguous.is(array) {
                numpy
                    .getattr(intern!(py, "copy"))?
                    .call1((contiguous,))?
                    .extract()?
            } else {
                array
            }
        };

        let mut tracker = CompressorPerformanceTracker {
            per_codec: vec![
                CodecPerformanceMeasurement {
                    encode_timing: Duration::ZERO,
                    decode_timing: Duration::ZERO,
                    encode_instructions: None,
                    decode_instructions: None,
                    encoded_bytes: 0,
                    decoded_bytes: 0,
                };
                compressor.len()
            ],
        };

        let decompressed =
            compress_decompress_contiguous_numpy_array(py, array, compressor, &mut tracker)?;

        Ok((decompressed, tracker.per_codec))
    }
}

#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct CodecPerformanceMeasurement {
    pub encode_timing: Duration,
    pub decode_timing: Duration,
    pub encode_instructions: Option<u64>,
    pub decode_instructions: Option<u64>,
    pub encoded_bytes: usize,
    pub decoded_bytes: usize,
}

#[pyclass]
// not frozen as the tracker is mutated to update the stats
struct CompressorPerformanceTracker {
    per_codec: Vec<CodecPerformanceMeasurement>,
}

#[pyfunction]
fn compress_decompress_data_array_single_chunk<'py>(
    py: Python<'py>,
    da: &'py PyAny,
    codecs: Vec<&'py crate::numcodecs::Codec>,
    tracker: &'py mut CompressorPerformanceTracker,
) -> Result<&'py PyAny, PyErr> {
    let dims: &PyTuple = da.getattr(intern!(py, "dims"))?.extract()?;
    let new_chunks = dims.iter().map(|dim| (dim, -1)).into_py_dict(py);

    if da.getattr(intern!(py, "size"))?.extract::<usize>()? == 0 {
        // compressing and decompressing preserves the input shape
        return da
            .call_method(
                intern!(py, "copy"),
                PyTuple::empty(py),
                Some([(intern!(py, "deep"), false)].into_py_dict(py)),
            )?
            .call_method1(intern!(py, "chunk"), (new_chunks,));
    }

    let numpy = py.import(intern!(py, "numpy"))?;

    // eagerly compute the uncompressed input chunk
    let values = da.getattr(intern!(py, "values"))?;
    // ensure that the uncompressed data is in a unique and contiguous array
    let array: &PyUntypedArray = numpy
        .getattr(intern!(py, "ascontiguousarray"))?
        .call1((values,))?
        .extract()?;
    let array: &PyUntypedArray = if array.is(values) {
        numpy
            .getattr(intern!(py, "copy"))?
            .call1((array,))?
            .extract()?
    } else {
        array
    };

    let decoded = compress_decompress_contiguous_numpy_array(py, array, codecs, tracker)?;

    da.call_method(
        intern!(py, "copy"),
        PyTuple::empty(py),
        Some(
            [
                (intern!(py, "deep"), &**PyBool::new(py, false)),
                (intern!(py, "data"), decoded),
            ]
            .into_py_dict(py),
        ),
    )?
    .call_method1(intern!(py, "chunk"), (new_chunks,))
}

fn compress_decompress_contiguous_numpy_array<'py>(
    py: Python<'py>,
    array: &'py PyUntypedArray,
    codecs: Vec<&'py crate::numcodecs::Codec>,
    tracker: &mut CompressorPerformanceTracker,
) -> Result<&'py PyUntypedArray, PyErr> {
    // pre-obtain methods that are needed in the hot encode and decode loops
    let numpy = py.import(intern!(py, "numpy"))?;
    let ensure_contiguous_ndarray_like = py
        .import(intern!(py, "numcodecs"))?
        .getattr(intern!(py, "compat"))?
        .getattr(intern!(py, "ensure_contiguous_ndarray_like"))?;
    let nbytes = intern!(py, "nbytes");
    let empty = numpy.getattr(intern!(py, "empty"))?;
    let reshape = intern!(py, "reshape");
    let instruction_counter = intern!(py, "instruction_counter");

    let mut silhouettes = Vec::with_capacity(codecs.len());

    // encode the chunk as: codecs[-1].encode( ... codecs[0].encode(array) ... )
    let encoded = codecs.iter().zip(tracker.per_codec.iter_mut()).try_fold(
        array,
        |encoded, (codec, measurement)| -> Result<&PyUntypedArray, PyErr> {
            silhouettes.push((PyTuple::new(py, encoded.shape()), encoded.dtype()));

            let pre_instructions: Option<u64> = codec
                .as_ref()
                .getattr(instruction_counter)
                .and_then(PyAny::extract)
                .ok();
            let encode_start = match WallTime::start() {
                Ok(encode_start) => encode_start,
                Err(err) => err.infallible(),
            };
            let encoded: &PyUntypedArray = ensure_contiguous_ndarray_like
                .call1((codec.encode(encoded)?,))?
                .extract()?;
            let encode_timing = match WallTime::end(encode_start) {
                Ok(encode_timing) => encode_timing,
                Err(err) => err.infallible(),
            };
            let post_instructions: Option<u64> = codec
                .as_ref()
                .getattr(instruction_counter)
                .and_then(PyAny::extract)
                .ok();

            measurement.encode_timing += encode_timing;
            if let (Some(pre), Some(post)) = (pre_instructions, post_instructions) {
                *measurement.encode_instructions.get_or_insert(0) += post - pre;
            }
            measurement.encoded_bytes += encoded.getattr(nbytes)?.extract::<usize>()?;

            Ok(encoded)
        },
    )?;

    // decode the chunk as: codecs[0].decode( ... codecs[-1].decode(encoded) ... )
    let decoded = codecs
        .into_iter()
        .zip(tracker.per_codec.iter_mut())
        .zip(silhouettes.into_iter())
        .try_rfold(
            encoded,
            |decoded, ((codec, measurement), (shape, dtype))| -> Result<&PyUntypedArray, PyErr> {
                let out: &PyUntypedArray = empty.call1((shape, dtype))?.extract()?;

                let pre_instructions: Option<u64> = codec
                    .as_ref()
                    .getattr(instruction_counter)
                    .and_then(PyAny::extract)
                    .ok();
                let decode_start = match WallTime::start() {
                    Ok(decode_start) => decode_start,
                    Err(err) => err.infallible(),
                };
                let decoded: &PyUntypedArray = codec
                    .decode(decoded, Some(out))?
                    .call_method1(reshape, (shape,))?
                    .extract()?;
                let decode_timing = match WallTime::end(decode_start) {
                    Ok(decode_timing) => decode_timing,
                    Err(err) => err.infallible(),
                };
                let post_instructions: Option<u64> = codec
                    .as_ref()
                    .getattr(instruction_counter)
                    .and_then(PyAny::extract)
                    .ok();

                measurement.decode_timing += decode_timing;
                if let (Some(pre), Some(post)) = (pre_instructions, post_instructions) {
                    *measurement.decode_instructions.get_or_insert(0) += post - pre;
                }
                measurement.decoded_bytes += decoded.getattr(nbytes)?.extract::<usize>()?;

                Ok(decoded)
            },
        )?;

    Ok(decoded)
}
