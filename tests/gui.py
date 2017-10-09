#!/usr/bin/env python3

from time import sleep

led1 = open('/sys/class/leds/pipuck_led1/brightness', 'w')
led2 = open('/sys/class/leds/pipuck_led1/brightness', 'w')
led3 = open('/sys/class/leds/pipuck_led1/brightness', 'w')
led4 = open('/sys/class/leds/pipuck_led1/brightness', 'w')

while True:
	led1.write('1')
	led2.write('0')
	led3.write('0')
	led4.write('0')
	sleep(1)
	led1.write('0')
	led2.write('1')
	led3.write('0')
	led4.write('0')
	sleep(1)
	led1.write('0')
	led2.write('0')
	led3.write('1')
	led4.write('0')
	sleep(1)
	led1.write('0')
	led2.write('0')
	led3.write('0')
	led4.write('1')
	sleep(1)
