#![cfg_attr(not(test), no_main)]

use std::sync::Mutex;

use rand::{
    distributions::{Distribution, Open01},
    Rng, SeedableRng,
};
use rand_chacha::ChaChaRng;

#[must_use]
pub fn add_uniform_noise<T: Float>(data: &[T], rng: &mut impl Rng, scale: T) -> Vec<T>
where
    Open01: Distribution<T>,
{
    data.iter()
        .map(|x| Open01.sample(rng).mul_add(scale, *x))
        .collect()
}

pub struct UniformNoiseCodec {
    rng: Mutex<ChaChaRng>,
    config: UniformNoiseCodecConfig,
}

impl Clone for UniformNoiseCodec {
    fn clone(&self) -> Self {
        Self {
            #[allow(clippy::unwrap_used)] // FIXME
            rng: Mutex::new(self.rng.try_lock().unwrap().clone()),
            config: self.config.clone(),
        }
    }
}

impl codecs_core::Codec for UniformNoiseCodec {
    type DecodedBuffer = codecs_core::VecBuffer;
    type EncodedBuffer = codecs_core::VecBuffer;

    const CODEC_ID: &'static str = "uniform-noise";

    fn from_config<'de, D: serde::Deserializer<'de>>(config: D) -> Result<Self, D::Error> {
        let config: UniformNoiseCodecConfig = serde::Deserialize::deserialize(config)?;

        Ok(Self {
            rng: Mutex::new(ChaChaRng::seed_from_u64(config.seed)),
            config,
        })
    }

    fn encode(
        &self,
        buf: codecs_core::BufferSlice,
        shape: &[usize],
    ) -> Result<codecs_core::ShapedBuffer<Self::EncodedBuffer>, String> {
        let Ok(mut rng) = self.rng.lock() else {
            return Err(String::from("UniformNoise::encode cannot use poisoned rng"));
        };

        let encoded =
            match buf {
                #[allow(clippy::cast_possible_truncation)]
                codecs_core::BufferSlice::F32(data) => codecs_core::BufferVec::F32(
                    add_uniform_noise(data, &mut *rng, self.config.scale as f32),
                ),
                codecs_core::BufferSlice::F64(data) => codecs_core::BufferVec::F64(
                    add_uniform_noise(data, &mut *rng, self.config.scale),
                ),
                buf => {
                    return Err(format!(
                        "UniformNoise::encode does not support the buffer dtype `{}`",
                        buf.ty(),
                    ))
                },
            };

        Ok(codecs_core::ShapedBuffer {
            shape: Vec::from(shape),
            buffer: encoded,
        })
    }

    fn decode(
        &self,
        buf: codecs_core::BufferSlice,
        shape: &[usize],
    ) -> Result<codecs_core::ShapedBuffer<Self::DecodedBuffer>, String> {
        let decoded = match buf {
            codecs_core::BufferSlice::F32(data) => codecs_core::BufferVec::F32(Vec::from(data)),
            codecs_core::BufferSlice::F64(data) => codecs_core::BufferVec::F64(Vec::from(data)),
            buf => {
                return Err(format!(
                    "UniformNoise::decode does not support the buffer dtype `{}`",
                    buf.ty(),
                ))
            },
        };

        Ok(codecs_core::ShapedBuffer {
            shape: Vec::from(shape),
            buffer: decoded,
        })
    }

    fn get_config<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serde::Serialize::serialize(&self.config, serializer)
    }
}

codecs_core_wasm::export_codec! {
    /// Uniform noise codec which adds U(-scale/2, scale/2) uniform random
    /// noise to the input on encoding and passes through the input unchanged
    /// during decoding.
    ///
    /// Note that this code has interior mutable state and encoding the same
    /// data twice will not produce the same result. To encode reproducibly,
    /// create a new codec with the same seed before every encoding.
    ///
    /// Args:
    ///     scale (float): Scale/width of the uniform noise to add on encoding.
    ///     seed (int): Seed for the random number generator.
    UniformNoiseCodec(scale, seed)
}

#[derive(Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "UniformNoiseCodec")]
struct UniformNoiseCodecConfig {
    scale: f64,
    seed: u64,
}

pub trait Float: Copy {
    #[must_use]
    fn mul_add(self, a: Self, b: Self) -> Self;
}

impl Float for f32 {
    fn mul_add(self, a: Self, b: Self) -> Self {
        Self::mul_add(self, a, b)
    }
}

impl Float for f64 {
    fn mul_add(self, a: Self, b: Self) -> Self {
        Self::mul_add(self, a, b)
    }
}
