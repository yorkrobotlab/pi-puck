#!/bin/bash -e
#
# Systemd shutdown script to set Raspberry Pi GPIO pins for Pi-puck power-off.
# Install to '/lib/systemd/system-shutdown/pi-puck-power.sh'.
#

if [ "$1" == "reboot" ] || [ "$1" == "halt" ]; then
	# Rebooting or halting, so set pull-up to keep pin high (and power on) when CPU is halted
	gpio mode 21 up
elif [ "$1" == "poweroff" ]; then
	# Powering off, so set pull-down so pin goes low (and power off) when CPU is halted
	# But first, ensure pin stays high for now (so power stays on) by setting it to output 1
	gpio write 21 1
	gpio mode 21 out
	gpio mode 21 down
fi
