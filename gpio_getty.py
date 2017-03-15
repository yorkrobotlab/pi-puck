#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

pin = 19

GPIO.setmode(GPIO.BCM)   # Use Broadcom (BCM) pin numbering
GPIO.setup(pin, GPIO.IN) # Input : listen for pin

if GPIO.input(pin):
	print('Starting getty service on ttyAMA0')
	os.system("sudo systemctl start serial-getty@ttyAMA0.service")
else:
	print('Stopping getty service on ttyAMA0')
	os.system("sudo systemctl stop serial-getty@ttyAMA0.service")

while True:

	GPIO.wait_for_edge(pin, GPIO.BOTH)

	if GPIO.input(pin):
		print('Starting getty service on ttyAMA0')
		os.system("sudo systemctl start serial-getty@ttyAMA0.service")
	else:
		print('Stopping getty service on ttyAMA0')
		os.system("sudo systemctl stop serial-getty@ttyAMA0.service")
