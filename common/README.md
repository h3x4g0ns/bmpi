bazel build --crosstool_top=//:arm_toolchain //src:video_rtp

bazel build --crosstool_top=//:arm_toolchain //tasks/video_rtp:video_rtp