#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

# Change this number if using a different GPIO pin
pin = 26

# Set up switch pin for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

while True:
	# Wait indefinitely for a rising edge
	GPIO.wait_for_edge(pin, GPIO.RISING)
	print("Switch turned on, waiting for timeout...")
	
	# Wait for up to 5 seconds for a falling edge (timeout is in milliseconds)
	result = GPIO.wait_for_edge(pin, GPIO.FALLING, timeout=5000)
	
	if result is None and GPIO.input(pin):
		print('Switch is still on, time to shutdown...')
		os.system("shutdown -h now")
	else:
		print('Switch turned off, shutdown cancelled.')
	
	time.sleep(0.1)
