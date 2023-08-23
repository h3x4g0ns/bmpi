from setuptools import setup, Extension
import pybind11

jado_module = Extension(
    'jado',
    sources=['src/jado.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++'
)

setup(
    name='jado',
    version='0.1',
    ext_modules=[jado_module],
)
