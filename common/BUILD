package(default_visibility = ["//visibility:public"])

cc_toolchain_suite(
    name = "arm_toolchain",
    toolchains = {
        "armeabi-v7a|compiler": ":cc_toolchain_config",
    },
)

load("//:arm_toolchain_config.bzl", "arm_toolchain_config")

arm_toolchain_config(
    name = "cc_toolchain_config",
)
