#!/usr/bin/env python3

import time
import sys
import smbus

I2C_CHANNEL = 3
FT903_I2C_ADDR = 0x1C

print('Pi-puck RGB LEDs example')

print('Initialising I2C...')

bus = smbus.SMBus(I2C_CHANNEL)

print('Cycling LEDs...')

bus.write_byte_data(FT903_I2C_ADDR, 0x00, 0x01) # Set LED1 to red
bus.write_byte_data(FT903_I2C_ADDR, 0x01, 0x02) # Set LED2 to green
bus.write_byte_data(FT903_I2C_ADDR, 0x02, 0x04) # Set LED3 to blue

time.sleep(1)

bus.write_byte_data(FT903_I2C_ADDR, 0x00, 0x02) # Set LED1 to green
bus.write_byte_data(FT903_I2C_ADDR, 0x01, 0x04) # Set LED2 to blue
bus.write_byte_data(FT903_I2C_ADDR, 0x02, 0x01) # Set LED3 to red

time.sleep(1)

bus.write_byte_data(FT903_I2C_ADDR, 0x00, 0x04) # Set LED1 to blue
bus.write_byte_data(FT903_I2C_ADDR, 0x01, 0x01) # Set LED2 to red
bus.write_byte_data(FT903_I2C_ADDR, 0x02, 0x02) # Set LED3 to green

time.sleep(1)

bus.write_byte_data(FT903_I2C_ADDR, 0x00, 0x07) # Set LED1 to white
bus.write_byte_data(FT903_I2C_ADDR, 0x01, 0x07) # Set LED2 to white
bus.write_byte_data(FT903_I2C_ADDR, 0x02, 0x07) # Set LED3 to white

time.sleep(1)

bus.write_byte_data(FT903_I2C_ADDR, 0x00, 0x00) # Set LED1 to off
bus.write_byte_data(FT903_I2C_ADDR, 0x01, 0x00) # Set LED2 to off
bus.write_byte_data(FT903_I2C_ADDR, 0x02, 0x00) # Set LED3 to off
