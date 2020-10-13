from typing import Optional
from smbus import SMBus
import RPi.GPIO as GPIO
from time import sleep


_EPUCK_I2C_CHANNEL = 12
_EPUCK_LEGACY_I2C_CHANNEL = 4
_EPUCK_I2C_ADDRESS = 0x1f
_EPUCK_RESET_PIN = 18


class EPuck:
	"""Class for interfacing with a generic e-puck robot."""

	def __init__(self, i2c_bus: Optional[int] = None, i2c_address: Optional[int] = None):
		if i2c_bus is not None:
			self._bus = SMBus(i2c_bus)
		else:
			try:
				self._bus = SMBus(_EPUCK_I2C_CHANNEL)
			except FileNotFoundError:
				self._bus = SMBus(_EPUCK_LEGACY_I2C_CHANNEL)

		if i2c_address is not None:
			self._i2c_address = i2c_address
		else:
			self._i2c_address = _EPUCK_I2C_ADDRESS

		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(_EPUCK_RESET_PIN, GPIO.OUT, initial=GPIO.HIGH)

	def __del__(self):
		GPIO.cleanup(_EPUCK_RESET_PIN)

	def _write_data_8(self, address, data):
		self._bus.write_byte_data(self._i2c_address, address, data)

	def _write_data_16(self, address, data):
		self._bus.write_word_data(self._i2c_address, address, data)

	def _read_data_8(self, address):
		return self._bus.read_byte_data(self._i2c_address, address)

	def _read_data_16(self, address):
		return self._bus.read_word_data(self._i2c_address, address)

	@staticmethod
	def reset_robot():
		GPIO.output(_EPUCK_RESET_PIN, GPIO.LOW)
		sleep(0.1)
		GPIO.output(_EPUCK_RESET_PIN, GPIO.HIGH)
