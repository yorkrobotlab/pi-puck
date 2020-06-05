"""Python module for controlling the Pi-puck."""

from smbus import SMBus
from typing import Sequence, Optional, Union, Tuple

import RPi.GPIO as GPIO

from .ft903 import FT903
from .epuck import EPuck
from .epuck1 import EPuck1
from .epuck2 import EPuck2
from .tof_sensor import ToFSensor
from .yrl_expansion import YRLExpansion


_BOARD_I2C_CHANNEL = 3
_SPEAKER_ENABLE_PIN = 15
_BATTERY_CHARGE_DETECT_PIN = 33
_BATTERY_MIN_VOLTAGE = 3.3
_BATTERY_MAX_VOLTAGE = 4.138
_BATTERY_CHARGE_MIN_VOLTAGE = 3.778
_BATTERY_CHARGE_MAX_VOLTAGE = 4.198
_BATTERY_VOLTAGE_RANGE = _BATTERY_MAX_VOLTAGE - _BATTERY_MIN_VOLTAGE
_BATTERY_CHARGE_RANGE = _BATTERY_CHARGE_MAX_VOLTAGE - _BATTERY_CHARGE_MIN_VOLTAGE
_EPUCK_BATTERY_PATH = "/sys/bus/i2c/drivers/ads1015/3-0048/in4_input"
_AUX_BATTERY_PATH = "/sys/bus/i2c/drivers/ads1015/3-0048/in5_input"

_led_colours = {
	'off': 0x00,
	'black': 0x00,
	'red': 0x01,
	'green': 0x02,
	'yellow': 0x03,
	'blue': 0x04,
	'magenta': 0x05,
	'cyan': 0x06,
	'white': 0x07
}


class PiPuck:
	"""Main Pi-puck controller class."""

	#: main Pi-puck board SMBus interface, instance of :class:`smbus.SMBus`
	_board_bus: SMBus
	#: FT903 microcontroller controller, instance of :class:`pipuck.ft903.FT903`
	ft903: FT903
	#: e-puck robot controller, either :obj:`None` or instance of :class:`pipuck.epuck.EPuck`
	epuck: Union[EPuck, EPuck1, EPuck2, None]
	#: time-of-flight sensor controllers, 6-tuple of either :class:`pipuck.tof_sensor.ToFSensor` instances or :obj:`None`
	tof_sensors: Tuple[Optional[ToFSensor], Optional[ToFSensor], Optional[ToFSensor],
	                   Optional[ToFSensor], Optional[ToFSensor], Optional[ToFSensor]]
	#: expansion board controller, either :obj:`None` or instance of :class:`pipuck.yrl_expansion.YRLExpansion`
	expansion: Optional[YRLExpansion]

	def __init__(self, epuck_version: Optional[int] = None,
	             tof_sensors: Sequence[bool] = (False, False, False, False, False, False),
	             yrl_expansion: bool = False) -> None:
		"""
		:param epuck_version: version of the base e-puck robot (either 1 or 2)
		:param tof_sensors: time-of-flight sensor boards attached (6 element tuple/list of :class:`bool` values)
		:param yrl_expansion: YRL Expansion Board attached
		"""
		self._board_bus = SMBus(_BOARD_I2C_CHANNEL)
		self.ft903 = FT903(self._board_bus)

		if epuck_version == 1:
			self.epuck = EPuck1()
		elif epuck_version == 2:
			self.epuck = EPuck2()
		else:
			self.epuck = None

		self.tof_sensors = (
			ToFSensor(0) if tof_sensors[0] else None,
			ToFSensor(1) if tof_sensors[1] else None,
			ToFSensor(2) if tof_sensors[2] else None,
			ToFSensor(3) if tof_sensors[3] else None,
			ToFSensor(4) if tof_sensors[4] else None,
			ToFSensor(5) if tof_sensors[5] else None
		)

		if yrl_expansion:
			self.expansion = YRLExpansion(self._board_bus)
		else:
			self.expansion = None

		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(_SPEAKER_ENABLE_PIN, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(_BATTERY_CHARGE_DETECT_PIN, GPIO.IN)

	def __del__(self):
		GPIO.cleanup((_SPEAKER_ENABLE_PIN, _BATTERY_CHARGE_DETECT_PIN))

	def set_led_raw(self, led: int, value: int) -> None:
		"""Set a single RGB LED colour.

		:param led: the LED to set (0-2)
		:param value: raw data byte value (``0b00000BGR``)
		"""
		self.ft903.write_data_8(led, value)

	def set_led_rgb(self, led: int, red: bool, green: bool, blue: bool) -> None:
		"""Set a single RGB LED colour.

		:param led: the LED to set (0-2)
		:param red: red value (on/off)
		:param green: green value (on/off)
		:param blue: blue value (on/off)
		"""
		if 0 <= led <= 2:
			colour = 0x00
			if red:
				colour += 0x01
			if green:
				colour += 0x02
			if blue:
				colour += 0x04
			self.set_led_raw(led, colour)

	def set_leds_rgb(self, red: bool, green: bool, blue: bool) -> None:
		"""Set all RGB LEDs to the same colour.

		:param red: red value (on/off)
		:param green: green value (on/off)
		:param blue: blue value (on/off)
		"""
		self.set_led_rgb(0, red, green, blue)
		self.set_led_rgb(1, red, green, blue)
		self.set_led_rgb(2, red, green, blue)

	def set_led_colour(self, led, colour: str) -> None:
		"""Set a single RGB LED colour.

		:param led: the LED to set (0-2)
		:param colour: colour value (off/black/red/green/yellow/blue/magenta/cyan/white)
		"""
		value = _led_colours[colour]
		self.set_led_raw(led, value)

	def set_leds_colour(self, colour: str) -> None:
		"""Set all RGB LEDs to the same colour.

		:param colour: colour value (off/black/red/green/yellow/blue/magenta/cyan/white)
		"""
		value = _led_colours[colour]
		self.set_led_raw(0, value)
		self.set_led_raw(1, value)
		self.set_led_raw(2, value)

	def set_leds_colours(self, colour1: str, colour2: str, colour3: str) -> None:
		"""Set RGB LEDs to the specified colours.

		:param colour1: LED1 colour (off/black/red/green/yellow/blue/magenta/cyan/white)
		:param colour2: LED2 colour (off/black/red/green/yellow/blue/magenta/cyan/white)
		:param colour3: LED3 colour (off/black/red/green/yellow/blue/magenta/cyan/white)
		"""
		self.set_led_raw(0, _led_colours[colour1])
		self.set_led_raw(1, _led_colours[colour2])
		self.set_led_raw(2, _led_colours[colour3])

	@staticmethod
	def speaker_enable(state: bool) -> None:
		"""Enable or disable the Pi-puck speaker audio amplifier.

		:param state: :obj:`True` to enable or :obj:`False` to disable
		"""
		if state:
			GPIO.output(_SPEAKER_ENABLE_PIN, GPIO.HIGH)
		else:
			GPIO.output(_SPEAKER_ENABLE_PIN, GPIO.LOW)

	@property
	def battery_is_charging(self) -> bool:
		"""Whether the robot is connected to a charger (either through USB or the charging contacts).

		:return: :obj:`True` if charging, otherwise :obj:`False`
		"""
		return GPIO.input(_BATTERY_CHARGE_DETECT_PIN) == GPIO.HIGH

	@staticmethod
	def convert_adc_to_voltage(adc_value: str) -> float:
		"""Convert ADC reading to voltage.

		:param adc_value: raw value from ADC file (in mV)
		:return: current measured battery voltage (in V)
		"""
		return float(adc_value) / 500.0

	def get_battery_state(self, battery_type: str = 'epuck') -> Tuple[bool, float, float]:
		"""Get current battery state.

		:param battery_type: battery type to check (either 'epuck' or 'aux')
		:return: tuple of (charging state, battery voltage, approximate battery percentage)
		"""
		charging = self.battery_is_charging
		if battery_type == 'epuck':
			battery_path = _EPUCK_BATTERY_PATH
		elif battery_type == 'aux':
			battery_path = _AUX_BATTERY_PATH
		else:
			return charging, 0.0, 0.0
		with open(battery_path, "r") as battery_file:
			voltage = self.convert_adc_to_voltage(battery_file.read())
		# Attempt to determine the charge/discharge level using some measured constants
		if charging:
			percentage = (voltage - _BATTERY_CHARGE_MIN_VOLTAGE) / _BATTERY_CHARGE_RANGE
		else:
			percentage = (voltage - _BATTERY_MIN_VOLTAGE) / _BATTERY_VOLTAGE_RANGE
		if percentage < 0.0:
			percentage = 0.0
		elif percentage > 1.0:
			percentage = 1.0
		return charging, voltage, percentage
