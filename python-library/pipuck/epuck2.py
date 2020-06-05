from pipuck import epuck

_EPUCK2_I2C_CHANNEL = 4
_EPUCK2_I2C_ADDRESS = 0x1f


class EPuck2(epuck.EPuck):
	"""Class for interfacing with an e-puck2 robot"""

	def __init__(self, i2c_bus=_EPUCK2_I2C_CHANNEL, i2c_address=_EPUCK2_I2C_ADDRESS):
		super().__init__(i2c_bus, i2c_address)
		print("e-puck2 not yet implemented")
