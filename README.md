# dt-overlays

1. About
2. Overlays
3. Scripts

## About
This project uses device-tree overlays to enable specific hardware devices on the **Beaglebone Black** platform. Furthermore I tried to make some effort to automate the build and install steps of the device tree overlays. This can be seen by the Makefile hierarchy within the project. The top-level Makefile has targets as simple to use as a an on/off switch to install and uninstall the overlays. The magic happens in the deeper levels of the source tree.

> **UPDATE:**
> Some users (including myself) experienced some weird behavior when removing the device tree overlays. Results maybe kernel "OOPS" messages or a frozen system. The recommended procedure is to do another install cycle and reboot the system.

All sources within this repository are licensed under the terms and conditions of the [GPLv2](https://www.gnu.org/licenses/gpl-2.0.html#SEC1).

## Overlays

Curretnly there are 2 overlays available. Each overlay directory contains the appropriate device tree source (.dts) file as well as a Makefile and udev-rules to simplify device usage. The access rights for the devices are set to "0666" which gives read and write access to every user. If that's not what you intend please go ahead and modify the udev-rules accordingly.

### I2C
Every modification done by the provided device tree source file is put into a separate `fragment` section to make it easily adaptable. Current modifications are.
- Create a pingroup __*i2c1\_pins*__ with proper pinmodes and add it to the pinmux controller __*am33xx\_pinmux*__
- Activate the __*i2c1*__ controller and set the clock frequency to 100kHz
- Add two devices to the I2C bus:
	- A real time clock on bus address **0x68** using the ds1307 driver
	- A Nintendo Wii nunchuck on bus address **0x52** using a custom driver that is not part of this repository

#### Real time clock (RTC)
The real time clock subdirectory contains an udev-rules file that sets file permissions for `/dev/rtcX` to "0666". Furthermore there are a systemd service file and a bash script which may be used to set or read the real time clock according to the defined conditions.

### SPI
The SPI overlay doesn't do too much. It contains two fragments that define a pingroup __*spi0\_pins*__ and activate the SPI controller __*spi0*__. The pingroup is assigned to that controller.

## Scripts
The python scripts do some of the heavy lifting when applying the device tree overlays. `read_slots.py` yields information from __*sysfs*__ and determines if an overlay is installed and to which slot. `set_uenv.py` is used to append/remove the name of the created overlays to the `uEnv.txt` variable `optargs`. I don't know if the syntax used is suitable for other operating systems than [archlinuxarm](https://archlinuxarm.org).
