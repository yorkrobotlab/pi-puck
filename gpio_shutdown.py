#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

pin = 26

GPIO.setmode(GPIO.BCM)   # Use Broadcom (BCM) pin numbering
GPIO.setup(pin, GPIO.IN) # Input : listen for pin

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
