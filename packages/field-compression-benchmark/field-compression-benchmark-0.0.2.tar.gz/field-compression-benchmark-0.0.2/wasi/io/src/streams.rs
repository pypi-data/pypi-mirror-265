use crate::{
    bindings::exports::wasi::io::{
        poll::Pollable,
        streams::{
            Guest as WasiIoStreams, GuestInputStream, GuestOutputStream, InputStream,
            InputStreamBorrow, OutputStream, StreamError,
        },
    },
    poll::VirtPollable,
    VirtIO,
};

impl WasiIoStreams for VirtIO {
    type InputStream = VirtInputStream;
    type OutputStream = VirtOutputStream;
}

pub struct VirtInputStream;
pub struct VirtOutputStream;

impl GuestInputStream for VirtInputStream {
    fn read(&self, _len: u64) -> Result<Vec<u8>, StreamError> {
        Err(StreamError::Closed)
    }

    fn blocking_read(&self, _len: u64) -> Result<Vec<u8>, StreamError> {
        Err(StreamError::Closed)
    }

    fn skip(&self, _len: u64) -> Result<u64, StreamError> {
        Err(StreamError::Closed)
    }

    fn blocking_skip(&self, _len: u64) -> Result<u64, StreamError> {
        Err(StreamError::Closed)
    }

    fn subscribe(&self) -> Pollable {
        VirtPollable::ready()
    }
}

impl VirtInputStream {
    #[must_use]
    pub fn closed() -> InputStream {
        InputStream::new(Self)
    }
}

impl GuestOutputStream for VirtOutputStream {
    fn check_write(&self) -> Result<u64, StreamError> {
        Ok(1024 * 1024)
    }

    fn write(&self, _contents: Vec<u8>) -> Result<(), StreamError> {
        Ok(())
    }

    fn blocking_write_and_flush(&self, _contents: Vec<u8>) -> Result<(), StreamError> {
        Ok(())
    }

    fn flush(&self) -> Result<(), StreamError> {
        Ok(())
    }

    fn blocking_flush(&self) -> Result<(), StreamError> {
        Ok(())
    }

    fn subscribe(&self) -> Pollable {
        VirtPollable::ready()
    }

    fn write_zeroes(&self, _len: u64) -> Result<(), StreamError> {
        Ok(())
    }

    fn blocking_write_zeroes_and_flush(&self, _len: u64) -> Result<(), StreamError> {
        Ok(())
    }

    fn splice(&self, _src: InputStreamBorrow, _len: u64) -> Result<u64, StreamError> {
        Err(StreamError::Closed)
    }

    fn blocking_splice(&self, _src: InputStreamBorrow, _len: u64) -> Result<u64, StreamError> {
        Err(StreamError::Closed)
    }
}

impl VirtOutputStream {
    #[must_use]
    pub fn sink() -> OutputStream {
        OutputStream::new(Self)
    }
}
