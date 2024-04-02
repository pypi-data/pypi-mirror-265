#![allow(clippy::missing_errors_doc)]

mod config;
#[cfg(target_arch = "wasm32")]
mod convert;

#[doc(hidden)]
#[allow(clippy::missing_safety_doc)]
pub mod bindings {
    wit_bindgen::generate!({
        path: "../wit",
        world: "fcbench-codec",
        pub_export_macro: true,
    });
}

#[macro_export]
macro_rules! export_codec {
    ($(#[doc = $doc:literal])* $codec:ident ( $($arg:expr),* )) => {
        #[cfg(target_arch = "wasm32")]
        $crate::bindings::export!($codec with_types_in $crate::bindings);

        impl $crate::CodecDocs for $codec {
            const SIGNATURE: &'static str = concat!($(stringify!($arg), ", "),*);
            const DOCUMENTATION: &'static str = concat!($($doc, "\n"),*);
        }
    };
}

#[doc(hidden)]
pub trait CodecDocs {
    const SIGNATURE: &'static str;
    const DOCUMENTATION: &'static str;
}

#[cfg(target_arch = "wasm32")]
#[doc(hidden)]
impl<C: codecs_core::Codec + CodecDocs> bindings::exports::fcbench::codec::codecs::Guest for C {
    type Codec = Self;

    fn codec_id() -> String {
        String::from(<Self as codecs_core::Codec>::CODEC_ID)
    }

    fn signature() -> String {
        String::from(<Self as CodecDocs>::SIGNATURE)
    }

    fn documentation() -> String {
        String::from(<Self as CodecDocs>::DOCUMENTATION)
    }
}

#[cfg(target_arch = "wasm32")]
impl<C: codecs_core::Codec> bindings::exports::fcbench::codec::codecs::GuestCodec for C {
    fn from_config(
        config: String,
    ) -> Result<bindings::exports::fcbench::codec::codecs::Codec, String> {
        match serde_json::from_str::<config::CodecConfig<Self>>(&config) {
            Ok(config::CodecConfig {
                id: config::CodecId { .. },
                codec,
            }) => {
                let codec: Self = codec.into_owned();
                Ok(bindings::exports::fcbench::codec::codecs::Codec::new(codec))
            },
            Err(err) => {
                let err = format_serde_error::SerdeError::new(config, err);
                Err(format!("{err}"))
            },
        }
    }

    fn encode(
        &self,
        data: bindings::exports::fcbench::codec::codecs::Buffer,
        shape: Vec<bindings::exports::fcbench::codec::codecs::Usize>,
    ) -> Result<bindings::exports::fcbench::codec::codecs::ShapedBuffer, String> {
        let data = convert::wit_buffer_to_codecs(&data);
        let shape = convert::u32_as_usize_vec(shape);

        let shaped_buffer = <Self as codecs_core::Codec>::encode(self, data, &shape)?;

        Ok(bindings::exports::fcbench::codec::codecs::ShapedBuffer {
            buffer: convert::codecs_buffer_to_wit(shaped_buffer.buffer)?,
            shape: convert::usize_as_u32_vec(shaped_buffer.shape),
        })
    }

    fn decode(
        &self,
        data: bindings::exports::fcbench::codec::codecs::Buffer,
        shape: Vec<bindings::exports::fcbench::codec::codecs::Usize>,
    ) -> Result<bindings::exports::fcbench::codec::codecs::ShapedBuffer, String> {
        let data = convert::wit_buffer_to_codecs(&data);
        let shape = convert::u32_as_usize_vec(shape);

        let shaped_buffer = <Self as codecs_core::Codec>::decode(self, data, &shape)?;

        Ok(bindings::exports::fcbench::codec::codecs::ShapedBuffer {
            buffer: convert::codecs_buffer_to_wit(shaped_buffer.buffer)?,
            shape: convert::usize_as_u32_vec(shaped_buffer.shape),
        })
    }

    fn get_config(&self) -> Result<String, String> {
        serde_json::to_string(&config::CodecConfig {
            id: config::CodecId::new(),
            codec: std::borrow::Cow::Borrowed(self),
        })
        .map_err(|err| format!("{err}"))
    }
}
