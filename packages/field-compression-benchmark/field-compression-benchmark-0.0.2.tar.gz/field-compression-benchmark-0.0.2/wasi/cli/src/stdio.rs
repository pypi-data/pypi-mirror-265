use crate::{
    bindings::{
        exports::wasi::cli::{
            stderr::Guest as WasiCliStderr, stdin::Guest as WasiCliStdin,
            stdout::Guest as WasiCliStdout,
        },
        wasi::{
            io::streams::{InputStream, OutputStream},
            virt::null_io::{closed_input, output_sink},
        },
    },
    VirtCli,
};

impl WasiCliStdin for VirtCli {
    fn get_stdin() -> InputStream {
        closed_input()
    }
}

impl WasiCliStdout for VirtCli {
    fn get_stdout() -> OutputStream {
        output_sink()
    }
}

impl WasiCliStderr for VirtCli {
    fn get_stderr() -> OutputStream {
        output_sink()
    }
}
