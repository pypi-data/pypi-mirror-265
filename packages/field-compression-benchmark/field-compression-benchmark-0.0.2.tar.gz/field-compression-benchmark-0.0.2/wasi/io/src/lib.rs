#![cfg_attr(not(test), no_main)]

use crate::bindings::exports::wasi::{
    io::{
        poll::Pollable,
        streams::{InputStream, OutputStream},
    },
    virt::null_io::Guest as WasiVirtNullIO,
};

pub mod error;
pub mod poll;
pub mod streams;

#[allow(clippy::missing_safety_doc)]
mod bindings {
    wit_bindgen::generate!({
        path: "../wit",
        world: "virtual-wasi-io",
    });
}

pub enum VirtIO {}

#[allow(unsafe_code)]
mod export {
    use crate::VirtIO;
    crate::bindings::export!(VirtIO with_types_in crate::bindings);
}

impl WasiVirtNullIO for VirtIO {
    fn ready_pollable() -> Pollable {
        poll::VirtPollable::ready()
    }

    fn closed_input() -> InputStream {
        streams::VirtInputStream::closed()
    }

    fn output_sink() -> OutputStream {
        streams::VirtOutputStream::sink()
    }
}
