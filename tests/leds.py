#!/usr/bin/env python3

# sudo chown -R :leds /sys/class/leds/pipuck_*/brightness
# sudo chmod g+w /sys/class/leds/pipuck_*/brightness

from time import sleep
import signal

def handler(signum, frame):
	led1.close()
	led2.close()
	led3.close()
	led4.close()
	ledn.close()
	print()
	exit(0)

signal.signal(signal.SIGINT, handler)

led1 = open('/sys/class/leds/pipuck_led1/brightness', 'w')
led2 = open('/sys/class/leds/pipuck_led2/brightness', 'w')
led3 = open('/sys/class/leds/pipuck_led3/brightness', 'w')
led4 = open('/sys/class/leds/pipuck_led4/brightness', 'w')
ledn = open('/sys/class/leds/pipuck_nav/brightness', 'w')

def write_led(led, value):
	led.write('1' if value else '0')
	led.flush()

write_led(led1, False)
write_led(led2, False)
write_led(led3, False)
write_led(led4, False)
write_led(ledn, False)

while True:
	write_led(led1, True)
	write_led(led2, False)
	write_led(led3, False)
	write_led(led4, False)
	write_led(ledn, True)
	sleep(0.5)
	write_led(led1, False)
	write_led(led2, True)
	write_led(led3, False)
	write_led(led4, False)
	write_led(ledn, False)
	sleep(0.5)
	write_led(led1, False)
	write_led(led2, False)
	write_led(led3, True)
	write_led(led4, False)
	write_led(ledn, True)
	sleep(0.5)
	write_led(led1, False)
	write_led(led2, False)
	write_led(led3, False)
	write_led(led4, True)
	write_led(ledn, False)
	sleep(0.5)
