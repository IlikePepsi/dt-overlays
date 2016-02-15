# dt-overlays

1. Wtf?
2. Overlays
3. Scripts

## Wtf?
This project uses device-tree overlays to enable specific hardware devices on the Beaglebone-Black platform.
Furthermore I tried to make some effort to automate the build and install steps of the device tree overlays.
This can be seen by the Makefile hierarchy within the project. The top-level Makefile has targets as simple to
use as a an on/off switch to install and uninstall the overlays. The magic happens in the deeper levels of 
the source tree.

## Overlays

Curretnly there are 2 overlays available. Each overlay directory contains the appropriate device tree source (.dts) 
file as well as a Makefile and udev-rules.

### I2C

#### Real time clock (RTC)


### SPI


## Scripts
