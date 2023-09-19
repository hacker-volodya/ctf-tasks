#![no_std]
#![no_main]
#![feature(abi_efiapi)]
#![feature(lang_items)]

use core::panic::PanicInfo;
use uefi::prelude::*;
use core::fmt::{Write, Display, Formatter};
use uefi::proto::console::text::Key;

mod flag {
    include!(concat!(env!("OUT_DIR"), "/flag.rs"));
}

extern crate rlibc;

struct Password([u8; 20]);

impl Display for Password {
    fn fmt(&self, f: &mut Formatter<'_>) -> core::fmt::Result {
        for c in self.0 {
            write!(f, "{}", c as char)?;
        }
        Ok(())
    }
}

#[entry]
fn efi_main(_: Handle, st: SystemTable<Boot>) -> Status {
    let pass = get_password(&st);
    write!(st.stdout(), "Checking... ");
    if !check_password(&pass) {
        writeln!(st.stdout(), "error!");
    }
    else {
        writeln!(st.stdout(), "ok");
        show_flag(&st, &pass);
    }
    loop {}
}

fn check_password(pass: &Password) -> bool {
    pass.0
        .chunks(4)
        .zip(flag::FLAG_CHUNKS)
        .all(|(a, b)| {
            let crc32 = crc::Crc::<u32>::new(&crc::CRC_32_ISO_HDLC);
            crc32.checksum(a) == b
        })
}

fn get_password(st: &SystemTable<Boot>) -> Password {
    let mut pass = Password([0; 20]);
    let mut counter = 0;
    st.stdout().write_str("Enter password: ");
    loop {
        if let Key::Printable(c) = read_key(st) {
            if !char::from(c).is_ascii_hexdigit() {
                continue;
            }
            if !char::from(c).is_ascii_digit() && !char::from(c).is_ascii_lowercase() {
                continue;
            }
            write!(st.stdout(), "{}", c);
            pass.0[counter] = char::from(c) as u8;
            counter += 1;
            if counter == 20 {
                st.stdout().write_char('\n');
                return pass
            }
        }
    }
}

fn read_key(st: &SystemTable<Boot>) -> Key {
    st.boot_services().wait_for_event(&mut [st.stdin().wait_for_key_event()]).unwrap();
    st.stdin().read_key().unwrap().unwrap().unwrap()
}

fn show_flag(st: &SystemTable<Boot>, pass: &Password) {
    writeln!(st.stdout(), "Access granted. Flag is HV{{{}}}", pass);
}

#[no_mangle]
pub fn abort() -> ! {
    loop {}
}

#[no_mangle]
pub fn breakpoint() -> ! {
    loop {}
}

#[no_mangle]
pub extern "C" fn _Unwind_Resume() -> ! {
    loop {}
}

#[lang = "eh_personality"]
#[no_mangle]
pub extern fn rust_eh_personality() {}

#[panic_handler]
#[no_mangle]
pub extern fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
