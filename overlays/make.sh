#!/bin/bash

../../linux/scripts/dtc/dtc -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-bottom.dtbo pi-puck-v3_0-bottom.dts
../../linux/scripts/dtc/dtc -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-top.dtbo pi-puck-v3_0-top.dts
../../linux/scripts/dtc/dtc -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-switchboard.dtbo pi-puck-v3_0-switchboard.dts
../../linux/scripts/dtc/dtc -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-sensorboards.dtbo pi-puck-v3_0-sensorboards.dts
