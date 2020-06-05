from .lsm9ds1 import LSM9DS1
from .mcp23017 import MCP23017

_NAV_U = 8
_NAV_D = 9
_NAV_L = 10
_NAV_R = 11
_NAV_C = 12
_LED_B = 13
_LED_G = 14
_LED_R = 15

_pi_header_pin_map = {
	7: 3,
	11: 2,
	12: 4,
	13: 1,
	15: 0,
	16: 5,
	18: 6,
	22: 7
}

_led_colours = {
	'off': (False, False, False),
	'black': (False, False, False),
	'red': (True, False, False),
	'green': (False, True, False),
	'yellow': (True, True, False),
	'blue': (False, False, True),
	'magenta': (True, False, True),
	'cyan': (False, True, True),
	'white': (True, True, True)
}


class YRLExpansion:

	def __init__(self, bus):
		self._i2c_bus = bus
		self.imu = LSM9DS1(bus)
		self._gpio = MCP23017(bus, 0x21)
		self.led_r = self._gpio.get_pin(_LED_R)
		self.led_g = self._gpio.get_pin(_LED_G)
		self.led_b = self._gpio.get_pin(_LED_B)
		self.nav_u = self._gpio.get_pin(_NAV_U)
		self.nav_d = self._gpio.get_pin(_NAV_D)
		self.nav_l = self._gpio.get_pin(_NAV_L)
		self.nav_r = self._gpio.get_pin(_NAV_R)
		self.nav_c = self._gpio.get_pin(_NAV_C)
		self.led_r.switch_to_output(True)
		self.led_g.switch_to_output(True)
		self.led_b.switch_to_output(True)
		self.nav_u.switch_to_input()
		self.nav_d.switch_to_input()
		self.nav_l.switch_to_input()
		self.nav_r.switch_to_input()
		self.nav_c.switch_to_input()

		self.pi_header = {}
		for pi_pin, gpio_pin in _pi_header_pin_map.items():
			self.pi_header[pi_pin] = self._gpio.get_pin(gpio_pin)
			self.pi_header[pi_pin].switch_to_input()

	def set_led_rgb(self, red, green, blue):
		self.led_r.value = not red
		self.led_g.value = not green
		self.led_b.value = not blue

	def set_led_colour(self, colour):
		values = _led_colours[colour]
		self.set_led_rgb(values[0], values[1], values[2])

	def get_nav_direction(self):
		if not self.nav_u.value:
			return 'up'
		elif not self.nav_d.value:
			return 'down'
		elif not self.nav_l.value:
			return 'left'
		elif not self.nav_r.value:
			return 'right'
		elif not self.nav_c.value:
			return 'centre'
		else:
			return None
