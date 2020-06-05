from time import sleep
from argparse import ArgumentParser

from pipuck.pipuck import PiPuck


def cycle_led(device, led=None):
	for colour in ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white', 'off'):
		if led is None:
			device.set_led_colour(colour)
		else:
			device.set_led_colour(led, colour)
		print(colour, end=" ")
		sleep(0.4)
	print()


def wait_for_switch(pipuck, direction):
	print("Waiting for", direction, "...", end=" ")
	while pipuck.expansion.get_nav_direction() != direction:
		sleep(0.1)
	print("OK")


def main():
	parser = ArgumentParser(description="Pi-puck Python Library Test")
	parser.add_argument("-e", "--epuck", type=int, default=0, help="e-puck version to test")
	parser.add_argument("-x", "--expansion", action="store_true", help="test YRL expansion board features")
	parser.add_argument("-t", "--tof", action="store_true", help="test time-of-flight sensors")
	args = parser.parse_args()
	epuck_version = args.epuck
	test_expansion = args.expansion
	test_tof = args.tof

	print("Pi-puck Python Library Test")

	pipuck = PiPuck(epuck_version, [test_tof] * 6, test_expansion)

	print()
	print("Cycling RGB LEDs...")
	print(" front-left: ", end="")
	cycle_led(pipuck, 2)
	print("front-right: ", end="")
	cycle_led(pipuck, 1)
	print("       rear: ", end="")
	cycle_led(pipuck, 0)

	if pipuck.epuck is not None:
		print()
		print("Cycling e-puck LEDs...")
		for i in range(8):
			print(i + 1, end=" ")
			pipuck.epuck.set_outer_leds_byte(0x01 << i)
			sleep(0.4)
		pipuck.epuck.set_outer_leds_byte(0x00)
		print("front", end=" ")
		pipuck.epuck.set_inner_leds(True, False)
		sleep(0.8)
		print("body")
		pipuck.epuck.set_inner_leds(False, True)
		sleep(0.8)
		pipuck.epuck.set_inner_leds(False, False)

		print()
		print("Reading e-puck infrared values...")
		pipuck.epuck.enable_ir_sensors(True)
		sleep(0.1)
		print("  Ambient:", list(pipuck.epuck.ir_ambient))
		print("Reflected:", list(pipuck.epuck.ir_reflected))
		pipuck.epuck.enable_ir_sensors(False)

	if test_expansion:
		print()
		print("Cycling expansion board RGB LED...")
		cycle_led(pipuck.expansion)

		print()
		print("Testing expansion board navigation switch inputs (press control-c to skip)...")
		try:
			for direction in ('up', 'down', 'left', 'right', 'centre'):
				wait_for_switch(pipuck, direction)
		except KeyboardInterrupt:
			pass

		print()
		print("Reading expansion board IMU data...")
		print("Acceleration:", list(pipuck.expansion.imu.acceleration))
		print("    Magnetic:", list(pipuck.expansion.imu.magnetic))
		print("        Gyro:", list(pipuck.expansion.imu.gyro))
		print(" Temperature:", pipuck.expansion.imu.temperature)

	if test_tof:
		print()
		print("Reading ToF sensor distances...")
		for tof in pipuck.tof_sensors:
			tof.open()
		for i, tof in enumerate(pipuck.tof_sensors):
			tof.start_ranging()
			distance = tof.get_distance()
			tof.stop_ranging()
			print("Distance {}: {}mm".format(i + 1, distance))
		for tof in pipuck.tof_sensors:
			tof.close()


if __name__ == "__main__":
	main()
