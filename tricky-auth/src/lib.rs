use pamsm::{PamServiceModule, Pam, PamFlags, PamError, pam_module, PamLibExt, PamMsgStyle};
use libc::{PROT_READ, PROT_WRITE, PROT_EXEC, MAP_PRIVATE, MAP_ANON};
use std::ptr::null_mut;
use seccomp::{Context, Rule, Action};

struct PamAuthModule;

impl PamServiceModule for PamAuthModule {
    fn open_session(_: Pam, _: PamFlags, _: Vec<String>) -> PamError {
        PamError::SUCCESS
    }

    fn close_session(_: Pam, _: PamFlags, _: Vec<String>) -> PamError {
        PamError::SUCCESS
    }

    fn authenticate(pamh: Pam, _: PamFlags, _: Vec<String>) -> PamError {
        // check user
        let user = pamh.get_user(None).unwrap().unwrap().to_str().unwrap();
        assert_eq!(user, "user");

        // ask for password
        let answ = pamh.conv(Some("Enter password: "), PamMsgStyle::PROMPT_ECHO_ON).unwrap().unwrap().to_str().unwrap();
        let code = hex::decode(answ).unwrap();
        let f: fn() = unsafe {
            let rwx = libc::mmap(null_mut(), code.len(), PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_ANON, -1, 0) as *mut u8;
            std::ptr::copy(code.as_ptr(), rwx, code.len());
            std::mem::transmute(rwx)
        };

        // apply seccomp rules
        let mut ctx = Context::default(Action::Errno(libc::EPERM)).unwrap();
        ctx.add_rule(Rule::new(0x00,None,Action::Allow)).unwrap();
        ctx.add_rule(Rule::new(0x01,None,Action::Allow)).unwrap();
        ctx.load().unwrap();

        f();

        PamError::AUTH_ERR
    }

    fn setcred(_: Pam, _: PamFlags, _: Vec<String>) -> PamError {
        PamError::SUCCESS
    }

    fn acct_mgmt(_: Pam, _: PamFlags, _: Vec<String>) -> PamError {
        PamError::SUCCESS
    }

    fn chauthtok(_: Pam, _: PamFlags, _: Vec<String>) -> PamError {
        PamError::SUCCESS
    }
}

pam_module!(PamAuthModule);