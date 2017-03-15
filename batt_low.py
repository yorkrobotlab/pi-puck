#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

pin = 27

GPIO.setmode(GPIO.BCM)   # Use Broadcom (BCM) pin numbering
GPIO.setup(pin, GPIO.IN) # Input : listen for pin

GPIO.wait_for_edge(pin, GPIO.FALLING)
print("BATT_LOW shutdown request received")
os.system("shutdown -h now")   # Software system shutdown (commence immediately)

