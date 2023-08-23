extern "C" {
  pub fn JADO_new() -> *mut libc::c_void;
  pub fn JADO_set(j: *mut libc::c_void, key: *const libc::c_char, value: *const libc::c_char);
  pub fn JADO_get(j: *mut libc::c_void, key: *const libc::c_char) -> *const libc::c_char;
  pub fn JADO_delete(j: *mut libc::c_void);
}

pub struct Jado {
  ptr: *mut libc::c_void,
}

impl Jado {
  pub fn new() -> Self {
    Jado {
      ptr: unsafe { JADO_new() },
    }
  }

  pub fn set(&mut self, key: &str, value: &str) {
    unsafe {
      JADO_set(
        self.ptr,
        key.as_ptr() as *const libc::c_char,
        value.as_ptr() as *const libc::c_char,
      )
    }
  }

  pub fn get(&self, key: &str) -> Option<String> {
    unsafe {
      let result = JADO_get(self.ptr, key.as_ptr() as *const libc::c_char);
      if result.is_null() {
        None
      } else {
        Some(CStr::from_ptr(result).to_string_lossy().into_owned())
      }
    }
  }
}

impl Drop for Jado {
  fn drop(&mut self) {
    unsafe { JADO_delete(self.ptr) }
  }
}
