# Supporting Files for the Pi-puck Extension Board

The Pi-puck is a [Raspberry Pi](https://www.raspberrypi.org) extension board for the [e-puck](http://www.gctronic.com/doc/index.php?title=E-Puck) and [e-puck2](http://www.gctronic.com/doc/index.php?title=e-puck2) robot platforms, designed and built as a collaboration between the [University of York](https://www.york.ac.uk/robot-lab/) and [GCtronic](http://www.gctronic.com).

Further documentation is available at https://pi-puck.readthedocs.io.

For more information about the Pi-puck, see:
- GCtronic wiki page - http://www.gctronic.com/doc/index.php?title=Pi-puck
- Pi-puck on the YRL website - https://www.york.ac.uk/robot-lab/pi-puck/
- IROS 2017 paper - https://eprints.whiterose.ac.uk/120310/

Additional software sources can be found in the following repositories:
- GCtronic Pi-puck repository - https://github.com/gctronic/Pi-puck
- Pi-puck Debian packages - https://github.com/yorkrobotlab/pi-puck-packages
- Pi-puck Raspbian distribution - https://github.com/yorkrobotlab/pi-gen


## Device Tree Overlay, etc.

**[device-tree/](device-tree/)**

Device tree overlay and associated `config.txt` for booting the Pi-puck.

The device tree overlay enables all the hardware on the board within Linux, with some configurable parameters. The `config.txt` options enable this device tree overlay and set up certain GPIO pins with required default values.


## Software Utilities

**[utilities/](utilities/)**

Linux utilities for configuring the Pi-puck hardware.


## Configuration Files

**[config/](config/)**

Various Linux configuration files for Pi-puck hardware.


## Software Examples

**[examples/](examples/)**

Linux examples for using the Pi-puck.


## e-puck1 Code

**[e-puck1/](e-puck1/)**

PIC firmware, bootloader and programming script for the e-puck1.


## FT903 Code

**[ft903/](ft903/)**

Firmware and DFU programming script for the FT903 chip.
