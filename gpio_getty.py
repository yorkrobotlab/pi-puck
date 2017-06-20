#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

# Change this number if using a different GPIO pin
pin = 19

# Try to find the primary UART (could be ttyAMA0 or ttyS0), and exit if not found
tty = ''
if os.path.exists('/dev/serial0'):
	ttyPath = os.path.realpath('/dev/serial0')
	tty = ttyPath.split('/')[-1]
else:
	exit(0)

# Set up switch pin for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

# Either start or stop the getty service, then wait for switch to change
while True:
	if GPIO.input(pin):
		print('Starting getty service on ' + tty)
		os.system("sudo systemctl start serial-getty@{0}.service".format(tty))
	else:
		print('Stopping getty service on ' + tty)
		os.system("sudo systemctl stop serial-getty@{0}.service".format(tty))
	time.sleep(0.1)
	GPIO.wait_for_edge(pin, GPIO.BOTH)
