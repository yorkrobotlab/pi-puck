#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

# Change this number if using a different GPIO pin
pin = 27

# Set up switch pin for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

while True:
	# Wait indefinitely for a falling edge
	GPIO.wait_for_edge(pin, GPIO.FALLING)
	print("BATT_LOW shutdown request received")
	
	# Wait for up to 2 seconds for a rising edge (timeout is in milliseconds)
	result = GPIO.wait_for_edge(pin, GPIO.RISING, timeout=2000)
	
	if result is None and not GPIO.input(pin):
		print('BATT_LOW still asserted, time to shutdown...')
		os.system("shutdown -h now")
	else:
		print('BATT_LOW signal changed, shutdown cancelled.')
	
	time.sleep(0.1)
