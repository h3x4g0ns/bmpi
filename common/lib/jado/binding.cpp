#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "data_struct.h"

namespace py = pybind11;

class Jado {
public:
    Jado() : data(nullptr) {}

    // Setter and Getter for Integer
    void set_int(int value) {
        cleanup();
        data = createIntData(value);
    }

    int get_int() const {
        if (data && data->type == INTEGER) {
            return data->value.intValue;
        }
        throw std::runtime_error("Data is not an integer type.");
    }

    // Setter and Getter for String
    void set_string(const std::string& value) {
        cleanup();
        data = createStringData(const_cast<char*>(value.c_str()));
    }

    std::string get_string() const {
        if (data && data->type == STRING) {
            return std::string(data->value.stringValue);
        }
        throw std::runtime_error("Data is not a string type.");
    }

    // Setter and Getter for Nested
    void set_nested(const Jado& nestedData) {
        cleanup();
        data = createNestedData(nestedData.data);
    }

    Jado get_nested() const {
        if (data && data->type == NESTED) {
            Jado result;
            result.data = data->value.nestedData;
            return result;
        }
        throw std::runtime_error("Data is not a nested type.");
    }

    // Setter and Getters for Array
    std::vector<Jado> get_array() const {
        if (!data || data->type != ARRAY) {
            throw std::runtime_error("Data is not an array type.");
        }

        std::vector<Jado> result;
        for (size_t i = 0; i < data->value.dataArray.length; i++) {
            Jado item;
            item.data = data->value.dataArray.items[i];
            result.push_back(item);
        }
        return result;
    }

    void set_array(std::vector<Jado> &vec) {
        struct Data** items = (struct Data**) malloc(sizeof(struct Data*) * vec.size());
        for (size_t i = 0; i < vec.size(); i++) {
            items[i] = vec[i].data;
        }
        data = createArrayData(items, vec.size());
    }

    // Destructor
    ~Jado() {
        cleanup();
    }

private:
    // Cleanup previously allocated data if any
    void cleanup() {
        if (data) {
            freeData(data);
            data = nullptr;
        }
    }

    struct Data* data;
};

PYBIND11_MODULE(Jado, m) {
    m.doc() = "pybind11 jado plugin";

    py::class_<Jado>(m, "Jado")
        .def(py::init<>())
        .def("set_int", &Jado::set_int)
        .def("get_int", &Jado::get_int)
        .def("set_string", &Jado::set_string)
        .def("get_string", &Jado::get_string)
        .def("set_nested", &Jado::set_nested)
        .def("get_nested", &Jado::get_nested)
        .def("set_array", &Jado::set_array)
        .def("get_array", &Jado::get_array)
        ;
}
