use std::{convert::Infallible, fmt};

use core_error::LocationError;
use core_measure::Measurement;

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CompressionError {
    error: f64,
}

impl Measurement for CompressionError {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.error
    }

    fn try_from_f64(error: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self { error })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{:.3e}", self.error))
    }
}
