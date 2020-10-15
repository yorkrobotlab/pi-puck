#!/usr/bin/env python3

# 0x00 - reflected light, left IR sensor - high byte
# 0x01 - reflected light, left IR sensor - low byte

# 0x02 - reflected light, center IR sensor - high byte
# 0x03 - reflected light, center IR sensor - low byte

# 0x04 - reflected light, right IR sensor - high byte
# 0x05 - reflected light, right IR sensor - low byte

# 0x06 - ambient light, left IR sensor - high byte
# 0x07 - ambient light, left IR sensor - low byte

# 0x08 - ambient light, center IR sensor - high byte
# 0x09 - ambient light, center IR sensor - low byte

# 0x0A - ambient light, right IR sensor - high byte
# 0x0B - ambient light, right IR sensor - low byte

# 0x0C - software revision number

import time
import smbus

I2C_CHANNEL = 12
LEGACY_I2C_CHANNEL = 4
I2C_ADDR = 0x60

try:
	bus = smbus.SMBus(I2C_CHANNEL)
except FileNotFoundError:
	bus = smbus.SMBus(LEGACY_I2C_CHANNEL)

software_revision = bus.read_byte_data(I2C_ADDR, 0x0C)
print("Software revision:", software_revision)

while True:
	left_reflected_high = bus.read_byte_data(I2C_ADDR, 0x00)
	left_reflected_low = bus.read_byte_data(I2C_ADDR, 0x01)

	centre_reflected_high = bus.read_byte_data(I2C_ADDR, 0x02)
	centre_reflected_low = bus.read_byte_data(I2C_ADDR, 0x03)

	right_reflected_high = bus.read_byte_data(I2C_ADDR, 0x04)
	right_reflected_low = bus.read_byte_data(I2C_ADDR, 0x05)

	left_ambient_high = bus.read_byte_data(I2C_ADDR, 0x06)
	left_ambient_low = bus.read_byte_data(I2C_ADDR, 0x07)

	centre_ambient_high = bus.read_byte_data(I2C_ADDR, 0x08)
	centre_ambient_low = bus.read_byte_data(I2C_ADDR, 0x09)

	right_ambient_high = bus.read_byte_data(I2C_ADDR, 0x0A)
	right_ambient_low = bus.read_byte_data(I2C_ADDR, 0x0B)

	left_reflected = (left_reflected_high << 8) | left_reflected_low
	centre_reflected = (centre_reflected_high << 8) | centre_reflected_low
	right_reflected = (right_reflected_high << 8) | right_reflected_low

	print(left_reflected, centre_reflected, right_reflected)

	# Wait 100 ms before sampling again
	time.sleep(0.1)
