load("@io_bazel_rules_go//go:def.bzl", "go_library", "go_binary")
load("@rules_rust//rust:rust.bzl", "rust_library")

cc_library(
  name = "jado_cc",
  srcs = ["jado.cpp"],
  hdrs = ["jado.h"],
  linkshared = 1,
  alwayslink = 1,
)

# Go Bindings
go_library(
  name = "jado_go",
  srcs = ["jado.go"],
  cdeps = [":jado_cc"],
  importpath = "jado-go",
)

# Rust Bindings
rust_library(
  name = "jado_rs",
  srcs = ["lib.rs"],
  deps = [":jado_cc"],
)

genrule(
  name = "jado_py",
  srcs = ["setup.py"], # You can also include other necessary source files if needed
  outs = ["output_jado_py.whl"], # or any other output, like a dist directory
  cmd = "python3 $(location setup.py) bdist_wheel --dist-dir $(@D)",
  tools = ["setup.py"],
)
