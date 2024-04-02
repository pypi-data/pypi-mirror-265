use std::{
    ffi::OsString,
    fs, io,
    path::{Path, PathBuf},
    process::Command,
};

const WASI_VERSION: u32 = 20;
const WASMTIME_VERSION_FULL: &str = "18.0.0";

fn main() -> io::Result<()> {
    // Check for `clippy` and return early in this case
    //  since `clippy` pollutes the `RUSTFLAGS` between rebuilds
    if std::env::var_os("RUSTC_WRAPPER")
        .or_else(|| std::env::var_os("RUSTC_WORKSPACE_WRAPPER"))
        .map_or(false, |wrapper| {
            Path::new(&wrapper).ends_with("clippy-driver")
        })
    {
        return Ok(());
    }

    std::env::remove_var("CARGO_ENCODED_RUSTFLAGS");

    let out_dir = PathBuf::from(std::env::var_os("OUT_DIR").ok_or_else(|| {
        io::Error::new(io::ErrorKind::NotFound, "missing env variable `OUT_DIR`")
    })?)
    .canonicalize()?;
    let target_dir = out_dir.join("target");
    let wasi_sdk_path = install_or_get_wasi_sdk_path(&out_dir)?;
    let adapter_path = install_or_get_wasi_snapshot_preview1_adapter_path(&out_dir)?;

    eprintln!("out_dir={out_dir:?}");
    eprintln!("target_dir={target_dir:?}");
    eprintln!("wasi_sdk_path={wasi_sdk_path:?}");
    eprintln!("adapter_path={adapter_path:?}");

    eprintln!("creating {target_dir:?}");
    fs::create_dir_all(&target_dir)?;

    for (crate_name, codec_name) in [
        ("bit-round-codec", "bit-round"),
        ("bit-transpose-codec", "bit-transpose"),
        ("identity-codec", "identity"),
        ("linear-quantize-codec", "linear-quantize"),
        ("log-codec", "log"),
        ("reinterpret-codec", "reinterpret"),
        ("sz3-codec", "sz3"),
        ("uniform-noise-codec", "uniform-noise"),
        ("zfp-codec", "zfp"),
        ("zlib-codec", "zlib"),
        ("zstd-codec", "zstd"),
    ] {
        let wasm = build_wasm_codec(&wasi_sdk_path, &target_dir, crate_name)?;
        add_change_dependencies(&wasm)?;
        let wasm = adapt_wasi_snapshot_to_preview2(&wasm, &adapter_path)?;
        copy_wasm_codec(&wasm, codec_name)?;
    }

    Ok(())
}

fn download_from_url(url: &str) -> io::Result<Vec<u8>> {
    // We need to use wget instead of reqwest here
    //  since building reqwest inside pyodide-build fails
    let mut cmd = Command::new("wget");
    cmd.arg("-qO-").arg(url);

    let output = cmd.output()?;
    if !output.status.success() {
        return Err(io::Error::new(
            io::ErrorKind::Other,
            format!(
                "wget exited with code {}:\n{}",
                output.status,
                String::from_utf8_lossy(&output.stderr),
            ),
        ));
    }

    Ok(output.stdout)
}

fn install_or_get_wasi_sdk_path(out_dir: &Path) -> io::Result<PathBuf> {
    let wasi_version_full = format!("{WASI_VERSION}.0");
    let wasi_sdk_path = out_dir.join(format!("wasi-sdk-{wasi_version_full}"));

    if wasi_sdk_path.exists() {
        return Ok(wasi_sdk_path);
    }

    let wasi_sdk_url = format!("https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-{WASI_VERSION}/wasi-sdk-{wasi_version_full}-linux.tar.gz");

    let tar_gz = download_from_url(&wasi_sdk_url)?;
    tar::Archive::new(flate2::read::GzDecoder::new(&mut &*tar_gz)).unpack(out_dir)?;

    Ok(wasi_sdk_path)
}

fn install_or_get_wasi_snapshot_preview1_adapter_path(out_dir: &Path) -> io::Result<PathBuf> {
    let adapter_path = out_dir.join("wasi_snapshot_preview1.reactor.wasm");

    if adapter_path.exists() {
        return Ok(adapter_path);
    }

    let adapter_url = format!("https://github.com/bytecodealliance/wasmtime/releases/download/v{WASMTIME_VERSION_FULL}/wasi_snapshot_preview1.reactor.wasm");
    let response = download_from_url(&adapter_url)?;

    fs::write(&adapter_path, response)?;

    Ok(adapter_path)
}

fn configure_cargo_cmd(wasi_sdk_path: &Path) -> io::Result<Command> {
    let cargo =
        PathBuf::from(std::env::var_os("CARGO").ok_or_else(|| {
            io::Error::new(io::ErrorKind::NotFound, "missing env variable `CARGO`")
        })?);

    // Special-case for compilation inside Pyodide, where we need to explicitly
    //  circumvent the cross-compilation wrapper
    let mut cmd = if cargo.ends_with("pywasmcross.py") {
        Command::new("cargo")
    } else {
        Command::new(cargo)
    };

    let bin_path = wasi_sdk_path.join("bin");
    let sysroot_path = wasi_sdk_path.join("share").join("wasi-sysroot");

    cmd.env("CC", bin_path.join("clang"));
    cmd.env("CXX", bin_path.join("clang++"));

    let lld = bin_path.join("lld");
    cmd.env("LLD", &lld);
    cmd.env("LD", lld);

    cmd.env("AR", bin_path.join("llvm-ar"));
    cmd.env("NM", bin_path.join("llvm-nm"));

    let mut bindgen_extra_clang_args = OsString::from("-fvisibility=default --sysroot=");
    bindgen_extra_clang_args.push(&sysroot_path);
    cmd.env("BINDGEN_EXTRA_CLANG_ARGS", &bindgen_extra_clang_args);

    let mut cflags = OsString::from("-D_WASI_EMULATED_PROCESS_CLOCKS --sysroot=");
    cflags.push(&sysroot_path);
    cmd.env("CFLAGS", &cflags);
    cmd.env("CXXFLAGS", cflags);

    cmd.env("LDFLAGS", "-lwasi-emulated-process-clocks");

    cmd.env("CXXSTDLIB", "c++");

    let mut rustflags = OsString::from("-C link-arg=-L");
    rustflags.push(sysroot_path.join("lib").join("wasm32-wasi"));
    rustflags.push(" -C strip=symbols");
    cmd.env("RUSTFLAGS", &rustflags);

    cmd.env_remove("CMAKE_TOOLCHAIN_FILE");

    Ok(cmd)
}

fn build_wasm_codec(
    wasi_sdk_path: &Path,
    target_dir: &Path,
    crate_name: &str,
) -> io::Result<PathBuf> {
    let mut cmd = configure_cargo_cmd(wasi_sdk_path)?;
    cmd.arg("build")
        .arg("--release")
        .arg("--target=wasm32-wasi")
        .arg("--package")
        .arg(crate_name)
        .env("CARGO_TARGET_DIR", target_dir);

    eprintln!("executing {cmd:?}");

    let status = cmd.status()?;
    if !status.success() {
        return Err(io::Error::new(
            io::ErrorKind::Other,
            format!("cargo exited with code {status}"),
        ));
    }

    Ok(target_dir
        .join("wasm32-wasi")
        .join("release")
        .join(crate_name.replace('-', "_"))
        .with_extension("wasm"))
}

fn add_change_dependencies(wasm: &Path) -> io::Result<()> {
    let dep_file = wasm.with_extension("d");

    eprintln!("reading {dep_file:?}");
    let deps = fs::read_to_string(dep_file)?;

    let Some((_, deps)) = deps.split_once(':') else {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "invalid deps file format",
        ));
    };

    for dep in deps.split_whitespace() {
        println!("cargo::rerun-if-changed={dep}");
    }

    Ok(())
}

fn adapt_wasi_snapshot_to_preview2(wasm: &Path, adapter: &Path) -> io::Result<PathBuf> {
    let wasm_preview2 = wasm.with_extension("preview2.wasm");

    eprintln!("reading from {wasm:?}");
    let wasm = fs::read(wasm)?;

    eprintln!("reading from {adapter:?}");
    let adapter = fs::read(adapter)?;

    let encoder = wit_component::ComponentEncoder::default()
        .module(&wasm)
        .map_err(|err| {
            io::Error::new(
                io::ErrorKind::Other,
                format!("wit_component::ComponentEncoder::module failed: {err}"),
            )
        })?
        .adapter("wasi_snapshot_preview1", &adapter)
        .map_err(|err| {
            io::Error::new(
                io::ErrorKind::Other,
                format!("wit_component::ComponentEncoder::adapter failed: {err}"),
            )
        })?;

    let wasm = encoder.encode().map_err(|err| {
        io::Error::new(
            io::ErrorKind::Other,
            format!("wit_component::ComponentEncoder::encode failed: {err}"),
        )
    })?;

    eprintln!("writing to {wasm_preview2:?}");
    fs::write(&wasm_preview2, wasm)?;

    Ok(wasm_preview2)
}

fn copy_wasm_codec(wasm: &Path, codec_name: &str) -> io::Result<()> {
    eprintln!("finding the wasm codec dir");
    let wasm_codec_dir = PathBuf::from("..")
        .join("..")
        .join("data")
        .join("codecs")
        .canonicalize()?;

    eprintln!("copying {wasm:?} into {wasm_codec_dir:?}");
    fs::copy(wasm, wasm_codec_dir.join(codec_name).with_extension("wasm"))?;

    Ok(())
}
