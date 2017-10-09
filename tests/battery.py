#!/usr/bin/env python3

from time import sleep
import sys
import signal

GREEN  = u'\u001b[32m'
YELLOW = u'\u001b[33m'
RED    = u'\u001b[31m'
CYAN   = u"\u001b[36m"
RESET  = u'\u001b[0m'

def handler(signum, frame):
	adc_epuck.close()
	adc_pipuck.close()
	print('\n' * 10)
	exit(0)

signal.signal(signal.SIGINT, handler)

adc_epuck = open('/sys/class/hwmon/hwmon0/device/in4_input', 'r')
adc_pipuck = open('/sys/class/hwmon/hwmon0/device/in5_input', 'r')

def read_adc_level(adc):
	adc.seek(0)
	strval = adc.read()
	intval = int(strval)
	return intval

def get_volts_epuck():
	get_volts_epuck.batt += read_adc_level(adc_epuck)
	get_volts_epuck.batt /= 2
	volts = (get_volts_epuck.batt * 0.001333) + 0.08
	return volts
get_volts_epuck.batt = 0

def get_volts_pipuck():
	get_volts_pipuck.batt += read_adc_level(adc_pipuck)
	get_volts_pipuck.batt /= 2
	volts = (get_volts_pipuck.batt * 0.001333) + 0.16
	return volts
get_volts_pipuck.batt = 0

def draw_bar(fill, width):
	fill = max(1, min(25, int(fill)))
	colour = ''
	if fill < 5:
		colour = RED
	elif fill < 10:
		colour = YELLOW
	else:
		colour = GREEN
	print('╔' + '═' * width + '╗')
	print('║' + colour + '█' * fill + ' ' * (width - fill) + RESET + '║')
	print('╚' + '═' * width + '╝')


print()

while True:
	volts_epuck = get_volts_epuck()
	volts_pipuck = get_volts_pipuck()
	print(' e-puck battery: {:1.2f}V'.format(volts_epuck))
	draw_bar((volts_epuck - 3) * 20 + 1, 25)
	print()
	print('Pi-puck battery: {:1.2f}V'.format(volts_pipuck))
	draw_bar((volts_pipuck - 3) * 20 + 1, 25)
	print()
	sys.stdout.write(u'\u001b[1000D') # Move left
	sys.stdout.write(u'\u001b[10A') # Move up
	sleep(0.2)
