# Device Tree Overlay and Boot Files for the Pi-puck

For more information about Linux device tree overlays on the Raspberry Pi, see https://www.raspberrypi.org/documentation/configuration/device-tree.md.

## Included Hardware

The device tree overlay enables the following hardware on the Pi-puck board:

- System LEDs
- Shutdown button _(optional)_
- UART/Bluetooth modifications _(optional)_
- I2C switch
  - On-board I2C bus
    - ADC
      - Battery level inputs
      - External ADC channels _(optional)_
  - e-puck I2C bus
  - Sensor board I2C buses (x6)
- Software I2C _(optional)_
- Audio output
- I2S microphone input


## Build Instructions

A compiled copy of the device tree overlay ([`pi-puck.dtbo`](pi-puck.dtbo)) is included . To recompile, use the following:
```
dtc -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck.dtbo pi-puck.dts
```

The `.dtbo` file should then be copied to `/boot/overlays/` on the Raspberry Pi.

To enable the overlay and other GPIO options necessary for booting the Pi-puck, copy [`pi-puck-config.txt`](pi-puck-config.txt) to `/boot/` on the Raspberry Pi, and add the following to the end of `/boot/config.txt`:

```
[all]
include pi-puck-config.txt
```


## Overlay Parameters

The device tree overlay allows certain features to be enabled, disabled or customised through parameters specified in [`pi-puck-config.txt`](pi-puck-config.txt).

- `shutdown_key_disable` disables using the aux on button as a Linux power key at a kernel level, allowing for scripts to use this button instead.
- `shutdown_key_debounce` sets up the debounce interval for the power button, effectively allowing a delay before shutdown is triggered (default `1000`, value in milliseconds).
- `bluetooth_disable` disables Raspberry Pi Bluetooth and instead switches the Pi-puck UART to the PL011 controller. This is the same as using `dtoverlay=pi3-disable-bt` - see [Raspberry Pi UART documentation](https://www.raspberrypi.org/documentation/configuration/uart.md).
- `ain2`/`ain3` or `ain2_soft_i2c`/`ain3_soft_i2c` enables the external AIN2/AIN3 inputs to the ADC (use `_soft_i2c` variants if also using `soft_i2c`).
- `ain2_gain`/`ain3_gain` sets the gain for the AIN2/AIN3 channels of the ADC (see [ads1015 documentation](https://github.com/raspberrypi/linux/blob/rpi-4.19.y/Documentation/devicetree/bindings/hwmon/ads1015.txt) for values) (default `2`).
- `ain2_datarate`/`ain3_datarate` sets the data rate for the AIN2/AIN3 channels of the ADC (see [ads1015 documentation](https://github.com/raspberrypi/linux/blob/rpi-4.19.y/Documentation/devicetree/bindings/hwmon/ads1015.txt) for values) (default `4`).
- `soft_i2c` disables the hardware I2C controller and enables a software I2C driver in its place. This can be useful for certain I2C devices that have timing issues, but causes additional CPU load when using I2C communication.
- `soft_i2c_gpio_delay_us` specifies the delay between GPIO operations (see [i2c-gpio documentation](https://github.com/raspberrypi/linux/blob/rpi-4.19.y/Documentation/devicetree/bindings/i2c/i2c-gpio.txt)) (default `2`).
