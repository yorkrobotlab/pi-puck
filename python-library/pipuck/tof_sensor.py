from VL53L1X import VL53L1X


TOF_I2C_CHANNELS = (13, 14, 15, 16, 17, 18)
TOF_LEGACY_I2C_CHANNELS = (5, 6, 7, 8, 9, 10)
TOF_I2C_ADDRESS = 0x29


class ToFSensor(VL53L1X):

	def __init__(self, number, i2c_address=TOF_I2C_ADDRESS):
		try:
			super().__init__(TOF_I2C_CHANNELS[number], i2c_address)
		except FileNotFoundError:
			super().__init__(TOF_LEGACY_I2C_CHANNELS[number], i2c_address)
