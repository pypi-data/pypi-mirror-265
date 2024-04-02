#![allow(clippy::missing_errors_doc)]

// mod bin;
mod codec;
mod plugin;

pub use codec::WasmCodec;
pub use plugin::CodecPlugin;

#[derive(Debug, thiserror::Error)]
#[error(transparent)]
pub struct Error(#[from] anyhow::Error);
