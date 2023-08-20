# BMPI Tasks

These are full packages that can be deployed on target devices as binaries.

## Setup

```sh
rustup add target arm-unknown-linux-gnueabihf
git clone https://github.com/raspberrypi/tools $HOME/rpi_tools
vim ~/.cargo/config

# add the following
[target.arm-unknown-linux-gnueabihf]
linker = "/rpi_tools/arm-bcm2708/arm-rpi-4.9.3-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc"
```
