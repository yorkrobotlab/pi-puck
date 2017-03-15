# rpi-epuck

## Device Tree Overlays

Each Device Tree Source (DTS) file must first be compiled into Device Tree Blob (DTB) as follows:

```
dtc -@ -I dts -O dtb -o rpi-puck-leds.dtbo rpi-puck-leds.dts
dtc -@ -I dts -O dtb -o rpi-puck-switches.dtbo rpi-puck-switches.dts
```

The resulting `.dtbo` files should then be copied to `/boot/overlays/` on the Raspberry Pi. To enable them, add the following lines to `/boot/config.txt`:

```
dtoverlay=rpi-puck-leds
dtoverlay=rpi-puck-switches
```

## Python scripts

First, install `supervisord` by running `sudo apt-get install supervisor`. Then, copy the Python scripts to `/usr/local/bin/`, and use `chmod +x` to make them executable. Finally, copy the `.conf` files to `/etc/supervisor/conf.d/`, and reboot the Raspberry Pi.

Note that the `rpi-puck-switches` Device Tree Overlay must be disabled for `gpio_shutdown.py` and `gpio_getty.py` to work.
