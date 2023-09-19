use std::{env, fs};
use std::path::Path;

fn main() {
    let out_dir = env::var_os("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("flag.rs");
    let flag = "058ea44b964d3df5ffb2";
    let chunks = flag
        .as_bytes()
        .chunks(4)
        .map(|chunk| crc::Crc::<u32>::new(&crc::CRC_32_ISO_HDLC).checksum(chunk))
        .collect::<Vec<u32>>();
    let arr = chunks.iter().map(|c| c.to_string()).collect::<Vec<String>>().join(", ");
    fs::write(
        &dest_path,
        format!("pub const FLAG_CHUNKS: [u32; 5] = [{}];", arr)
    ).unwrap();
    println!("cargo:rerun-if-changed=build.rs");
}