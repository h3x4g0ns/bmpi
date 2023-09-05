load("@bazel_tools//tools/cpp:cc_toolchain_config.bzl", "cc_toolchain_config")

def _impl(ctx):
    tool_paths = {
        'ar_executable': '/usr/bin/arm-linux-gnueabihf-ar',
        'compiler_executable': '/usr/bin/arm-linux-gnueabihf-g++',
        'preprocessor_executable': '/usr/bin/arm-linux-gnueabihf-gcc',
        'nm_executable': '/usr/bin/arm-linux-gnueabihf-nm',
        'objcopy_executable': '/usr/bin/arm-linux-gnueabihf-objcopy',
        'strip_executable': '/usr/bin/arm-linux-gnueabihf-strip',
    }

    return cc_toolchain_config(
        ctx = ctx,
        toolchain_identifier = 'arm-linux-gnueabihf',
        host_system_name = 'local',
        target_system_name = 'arm-linux-gnueabihf',
        target_cpu = 'armeabi-v7a',
        target_libc = 'gnu',
        compiler = 'gcc',
        abi_version = 'unknown',
        abi_libc_version = 'unknown',
        tool_paths = tool_paths,
    )

arm_toolchain_config = rule(
    implementation = _impl,
    attrs = {},
    provides = [CcToolchainConfigInfo],
)
