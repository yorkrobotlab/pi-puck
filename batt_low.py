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
	os.system("wall 'BATT_LOW signal asserted. Powering off in 2 seconds...'")
	
	# Wait for up to 2 seconds for a rising edge (timeout is in milliseconds)
	result = GPIO.wait_for_edge(pin, GPIO.RISING, timeout=2000)
	
	if result is None and not GPIO.input(pin):
		print('BATT_LOW still asserted, time to shutdown...')
		os.system("wall 'BATT_LOW signal still asserted. Powering off now...'")
		os.system("shutdown -h now")
	else:
		print('BATT_LOW signal changed, shutdown cancelled.')
		os.system("wall 'BATT_LOW signal de-asserted. Power off cancelled.'")
	
	time.sleep(0.1)
