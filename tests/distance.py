#!/usr/bin/env python3

from time import sleep
import sys
import signal
from VL53L0X import VL53L0X

def handler(signum, frame):
	tofl.stop_ranging()
	tofr.stop_ranging()
	print()
	print()
	exit(0)

signal.signal(signal.SIGINT, handler)

tofl = VL53L0X.VL53L0X(address=5)
tofr = VL53L0X.VL53L0X(address=6)

tofl.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
tofr.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

while True:
	distancel = tofl.get_distance()
	distancer = tofr.get_distance()
	print(' left: {:4.0f}mm'.format(distancel))
	print('right: {:4.0f}mm'.format(distancer))
	sys.stdout.write(u"\u001b[1000D") # Move left
	sys.stdout.write(u"\u001b[2A") # Move up
	sleep(0.2)
