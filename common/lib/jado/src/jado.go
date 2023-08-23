package jado

/*
#cgo CXXFLAGS: -std=c++14
#cgo LDFLAGS: -L. -ljado

#include "jado.h"
*/
import "C"

type JADO struct {
	ptr C.JADO
}

func NewJADO() *JADO {
	return &JADO{ptr: C.JADO_new()}
}

func (j *JADO) Set(key, value string) {
	C.JADO_set(j.ptr, C.CString(key), C.CString(value))
}

func (j *JADO) Get(key string) string {
	cstr := C.JADO_get(j.ptr, C.CString(key))
	return C.GoString(cstr)
}

func (j *JADO) Delete() {
	C.JADO_delete(j.ptr)
}
