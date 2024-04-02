# ESiWACE3 Data Compression Benchmark Suite

The suite compares the performance of various data compression methods with different settings across a variety of variables and their derivatives from different GRIB, NetCDF, or Zarr datasets.

## Usage

`> field-compression-benchmark [OPTIONS] <COMMAND>`

**Commands**:

* `bench` Execute the benchmarking suite
* `help` Print this message or the help of the given subcommand(s)

**Options**:

* `-l`, `--log <LOG>`

   Level of log messages which are printed to stderr
          
   [possible values: `off`, `error`, `warn`, `info`, `debug`, `trace`]

* `-q`, `--quiet`

   Disable any messages to be printed to stdout or stderr

* `-c`, `--color <COLOR>`

   Colour and pretty-format console messages
          
   [possible values: `auto`, `always`, `never`]

* `-h`, `--help`

   Print help (see a summary with `-h`)

* `-V`, `--version`

   Print version

### `bench` subcommand

Execute the benchmarking suite

**Usage**: 

`> field-compression-benchmark bench [OPTIONS]`

**Options**:

* `--codec [<CODECS>...]`

   Include the following WASM codec files or directories
          
   [default: `data/codecs`]

* `--exclude-codec [<EXCLUDED_CODECS>...]`

   Exclude the following WASM codec files or directories

* `--compressor [<COMPRESSORS>...]`

   Include the following compressor config files or directories
          
   [default: `data/compressors`]

* `--exclude-compressor [<EXCLUDED_COMPRESSORS>...]`

   Exclude the following compressor config files or directories

* `--dataset [<DATASETS>...]`

   Include the following dataset config files or directories
          
   [default: `data/datasets`]

* `--exclude-dataset [<EXCLUDED_DATASETS>...]`

   Exclude the following dataset config files or directories

* `-c`, `--cases <CASES>`
   
   Store the line-separated list of case UUIDs to this file (with `--dry-run`) or load the list of case UUIDs from this file (with `--no-dry-run`)

* `-m`, `--minimal [<MINIMAL>...]`

   Only benchmark the smallest subset of benchmark dimension
          
   [possible values: `all`, `codec-parameters`, `dataset-variables`, `variable-dimensions`, `variable-derivatives`]

* `-d`, `--dry-run`

   Don't actually run any benchmark; just check all inputs

*  `-n`, `--num-repeats <NUM_REPEATS>`

   Repeat each benchmark case several times to collect multiple measurements
          
   [default: `10`]

* `-s`, `--bootstrap-seed <BOOTSTRAP_SEED>`

   Seed the random number generator used for bootstrap analysis, or use a random seed

* `-b`, `--bootstrap-samples <BOOTSTRAP_SAMPLES>`

   Resample all measurements with replacement to generate bootstrapping statistics
          
   [default: `1000`]

* `--error-bins <ERROR_BINS>`

   Number of bins in the compression error histogram
          
   [default: `100`]

* `--error-resamples <ERROR_RESAMPLES>`

   Resample the compression error distribution at regular intervals
          
   [default: `100`]

* `--dataset-auto-chunk-size <DATASET_AUTO_CHUNK_SIZE>`

   Default chunk size for automatic chunking of datasets

   [default: `32 MiB`]

* `-o`, `--output <OUTPUT>`

   Store the results to a JSON report file

* `--resume`

   Resume the benchmark from an existing JSON report file

* `-k`, `--keep-going`

   Keep going when a benchmark case fails

* `-p`, `--num-processes <NUM_PROCESSES>`

   Distribute the benchmark across several processes, or use the available parallelism

* `--progress <PROGRESS>`

   Select the detail of the progress updates as benchmark cases complete [possible values: `off`, `minimal`, `report`]

* `--no-dry-run`

   Execute all benchmark cases (default)

* `--no-resume`

   Create a fresh JSON report file, do not resume from one (default)

* `--no-keep-going`

   Stop with the first benchmark case failure (default)

* `-h`, `--help`

   Print help (see a summary with `-h`)

* `-V`, `--version`

   Print version

## License

Licensed under either of

 * Apache License, Version 2.0
   ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
 * MIT license
   ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.

## Funding

The ESiWACE3 Field Compression Benchmark has been developed as part of [ESiWACE3](https://www.esiwace.eu), the third phase of the Centre of Excellence in Simulation of Weather and Climate in Europe.

Funded by the European Union. This work has received funding from the European High Performance Computing Joint Undertaking (JU) under grant agreement No 101093054.
