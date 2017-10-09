#!/usr/bin/env python3

# sudo chown -R :leds /sys/class/leds/pipuck_*/brightness
# sudo chmod g+w /sys/class/leds/pipuck_*/brightness

from time import sleep
import sys
import signal
from VL53L0X import VL53L0X

HOME    = u'\u001b[0;0H'
CLEAR   = u'\u001b[2J'
CLEARL  = u'\u001b[2K'
GREEN   = u'\u001b[32m'
YELLOW  = u'\u001b[33m'
RED     = u'\u001b[31m'
CYAN    = u'\u001b[36m'
GREENB  = u'\u001b[42m'
YELLOWB = u'\u001b[43m'
REDB    = u'\u001b[41m'
CYANB   = u'\u001b[46m'
RESET  = u'\u001b[0m'

def int_handler(signum, frame):
	write_led(led1, False)
	write_led(led2, False)
	write_led(led3, False)
	write_led(led4, False)
	write_led(ledn, False)
	tofl.stop_ranging()
	tofr.stop_ranging()
	adc_epuck.close()
	adc_pipuck.close()
	led1.close()
	led2.close()
	led3.close()
	led4.close()
	ledn.close()
	sys.stdout.write(HOME)
	sys.stdout.write(CLEAR)
	print()
	exit(0)
signal.signal(signal.SIGINT, int_handler)

def winch_handler(signum, frame):
	sys.stdout.write(CLEAR)
signal.signal(signal.SIGWINCH, winch_handler)

led1 = open('/sys/class/leds/pipuck_led1/brightness', 'w')
led2 = open('/sys/class/leds/pipuck_led2/brightness', 'w')
led3 = open('/sys/class/leds/pipuck_led3/brightness', 'w')
led4 = open('/sys/class/leds/pipuck_led4/brightness', 'w')
ledn = open('/sys/class/leds/pipuck_nav/brightness', 'w')

adc_epuck = open('/sys/class/hwmon/hwmon0/device/in4_input', 'r')
adc_pipuck = open('/sys/class/hwmon/hwmon0/device/in5_input', 'r')

tofl = VL53L0X.VL53L0X(address=5)
tofr = VL53L0X.VL53L0X(address=6)

def write_led(led, value):
	led.write('1' if value else '0')
	led.flush()

def read_adc_level(adc):
	adc.seek(0)
	strval = adc.read()
	intval = int(strval)
	return intval

def get_volts_epuck():
	batt = read_adc_level(adc_epuck)
	get_volts_epuck.volts += round((batt * 0.001333) + 0.08, 2)
	get_volts_epuck.volts = round(get_volts_epuck.volts / 2, 2)
	return get_volts_epuck.volts
get_volts_epuck.volts = 0

def get_volts_pipuck():
	batt = read_adc_level(adc_pipuck)
	get_volts_pipuck.volts += round((batt * 0.001333) + 0.16, 2)
	get_volts_pipuck.volts = round(get_volts_pipuck.volts / 2, 2)
	return get_volts_pipuck.volts
get_volts_pipuck.volts = 0

def draw_bar(fill, width):
	fill = max(1, min(25, int(fill)))
	colour = ''
	if fill < width / 5:
		colour = REDB
	elif fill < width / 3:
		colour = YELLOWB
	else:
		colour = GREENB
	print(' ╔' + '═' * width + '╗')
	print(' ║' + colour + ' ' * fill + RESET + ' ' * (width - fill) + '║')
	print(' ╚' + '═' * width + '╝')

def draw_double_bar(fill1, fill2, width):
	fill1 = max(1, min(width, int(fill1)))
	fill2 = max(1, min(width, int(fill2)))
	colour1 = ''
	colour2 = ''
	if fill1 < width / 5:
		colour1 = REDB
	elif fill1 < width / 3:
		colour1 = YELLOWB
	else:
		colour1 = GREENB
	if fill2 < width / 5:
		colour2 = REDB
	elif fill2 < width / 3:
		colour2 = YELLOWB
	else:
		colour2 = GREENB
	print(' ╔' + '═' * width + '╗    ╔' + '═' * width + '╗')
	print(' ║' + colour1 + ' ' * fill1 + RESET + ' ' * (width - fill1) + '║    ║' + colour2 + ' ' * fill2 + RESET + ' ' * (width - fill2) + '║')
	print(' ╚' + '═' * width + '╝    ╚' + '═' * width + '╝')

def draw_vbar(fill, height):
	fill = max(0.5, min(height, fill))
	intfill = int(fill)
	colour = ''
	if fill < height / 5:
		colour = RED
	elif fill < height / 3:
		colour = YELLOW
	else:
		colour = GREEN
	print(' ╔══╗')
	for i in range(0, height - intfill):
		print(' ║  ║')
	for i in range(0, intfill):
		if i == 0 and fill < height and (fill - intfill) < 0.5:
			print(' ║' + colour + '▄▄' + RESET + '║')
		else:
			print(' ║' + colour + '██' + RESET + '║')
	print(' ╚══╝')

def draw_vblock(pos, height):
	pos = max(0.5, min(height, pos+0.5))
	intpos = int(pos)
	colour = ''
	if pos < height / 5:
		colour = RED
	elif pos < height / 2:
		colour = YELLOW
	else:
		colour = GREEN
	print(' ╔═══╗')
	for i in range(0, height - intpos):
		print(' ║   ║')
	if pos < height and (pos - intpos) < 0.5:
		print(' ║' + colour + '▄▄▄' + RESET + '║')
	else:
		print(' ║' + colour + '▀▀▀' + RESET + '║')
	for i in range(0, intpos - 1):
		print(' ║   ║')
	print(' ╚═══╝')

def draw_double_vblock(pos1, pos2, height):
	pos1 = max(0.5, min(height, pos1+0.5))
	pos2 = max(0.5, min(height, pos2+0.5))
	intpos1 = int(pos1)
	intpos2 = int(pos2)
	colour1 = ''
	colour2 = ''
	if pos1 < height / 5:
		colour1 = RED
	elif pos1 < height / 2:
		colour1 = YELLOW
	else:
		colour1 = GREEN
	if pos2 < height / 5:
		colour2 = RED
	elif pos2 < height / 2:
		colour2 = YELLOW
	else:
		colour2 = GREEN
	print('  ╔════╗    ╔════╗')
	# for i in range(0, height - intpos):
	# 	print(' ║   ║    ║   ║')
	# if pos < height and (pos - intpos) < 0.5:
	# 	print(' ║' + colour + '▄▄▄' + RESET + '║')
	# else:
	# 	print(' ║' + colour + '▀▀▀' + RESET + '║')
	# for i in range(0, intpos - 1):
	# 	print(' ║   ║')
	for i in range(0, height):
		sys.stdout.write('  ║')
		if i == height - intpos1:
			if pos1 < height and (pos1 - intpos1) < 0.5:
				sys.stdout.write(colour1 + '▄▄▄▄' + RESET)
			else:
				sys.stdout.write(colour1 + '▀▀▀▀' + RESET)
		else:
			sys.stdout.write('    ')
		sys.stdout.write('║    ║')
		if i == height - intpos2:
			if pos2 < height and (pos2 - intpos2) < 0.5:
				sys.stdout.write(colour2 + '▄▄▄▄' + RESET)
			else:
				sys.stdout.write(colour2 + '▀▀▀▀' + RESET)
		else:
			sys.stdout.write('    ')
		print('║')
	print('  ╚════╝    ╚════╝')

def cycle_leds():
	cycle_leds.leds_state += 1
	if cycle_leds.leds_state > 5:
		cycle_leds.leds_state = 1
	write_led(led1, cycle_leds.leds_state == 1)
	write_led(led2, cycle_leds.leds_state == 2)
	write_led(led3, cycle_leds.leds_state == 3)
	write_led(led4, cycle_leds.leds_state == 4)
	write_led(ledn, cycle_leds.leds_state == 5)
cycle_leds.leds_state = 0

write_led(led1, False)
write_led(led2, False)
write_led(led3, False)
write_led(led4, False)
write_led(ledn, False)

tofl.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
tofr.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

sys.stdout.write(CLEAR)

while True:
	distancel = tofl.get_distance()
	distancer = tofr.get_distance()
	volts_epuck = get_volts_epuck()
	volts_pipuck = get_volts_pipuck()
	print(CLEARL)
	sys.stdout.write(HOME)
	print(CLEARL)
	print('  left      right')
	draw_double_vblock(distancel/50, distancer/50, 8)
	print('  {:4.0f}mm    {:4.0f}mm'.format(distancel, distancer))
	print(CLEARL)
	print(CLEARL)
	# print('  e-puck battery: {:1.2f}V'.format(volts_epuck))
	# draw_bar((volts_epuck - 3) * 20 + 1, 25)
	# print(CLEARL)
	# print('  Pi-puck battery: {:1.2f}V'.format(volts_pipuck))
	# draw_bar((volts_pipuck - 3) * 20 + 1, 25)
	print('  e-puck battery: {:1.2f}V          Pi-puck battery: {:1.2f}V'.format(volts_epuck, volts_pipuck))
	draw_double_bar((volts_epuck - 3) * 20 + 1, (volts_pipuck - 3) * 20 + 1, 25)
	print(CLEARL)
	cycle_leds()
	sleep(0.05)
	