#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <map>
#include "jado.h"

namespace py = pybind11;

class JADO {
private:
  std::map<std::string, py::object> data;

public:
  void set(const std::string &key, const py::object &value) {
    if (py::isinstance<py::dict>(value)) {
      JADO obj;
      py::dict dict_value = value.cast<py::dict>();
      for (auto item : dict_value) {
          obj.set(item.first.cast<std::string>(), item.second);
      }
        data[key] = py::cast(obj);
    } else {
      data[key] = value;
    }
  }

  py::object get(const std::string &key) const {
    auto it = data.find(key);
    if (it != data.end()) {
        return it->second;
    }
    return py::none();
  }

  static JADO from_dict(const py::dict &dict_value) {
    JADO obj;
    for (auto item : dict_value) {
        obj.set(item.first.cast<std::string>(), item.second);
    }
    return obj;
  }

};

PYBIND11_MODULE(jado, m) {
  py::class_<JADO>(m, "JADO")
    .def(py::init<>())
    .def("__setattr__", &JADO::set)
    .def("__getattr__", &JADO::get)
    .def_static("from_dict", &JADO::from_dict);
}

// Implement C API functions
JADO JADO_new() {
    return new JADO();
}

void JADO_set(JADO j, const char* key, const char* value) {
    reinterpret_cast<JADO*>(j)->set(key, value);
}

const char* JADO_get(JADO j, const char* key) {
    return reinterpret_cast<JADO*>(j)->get(key).c_str();
}

void JADO_delete(JADO j) {
    delete reinterpret_cast<JADO*>(j);
}
