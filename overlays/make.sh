#!/bin/bash

DTC=../../linux/scripts/dtc/dtc

$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v1_0.dtbo pi-puck-v1_0.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v2_0.dtbo pi-puck-v2_0.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0_proto.dtbo pi-puck-v3_0_proto.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-bottom.dtbo pi-puck-v3_0-bottom.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-top.dtbo pi-puck-v3_0-top.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-switchboard.dtbo pi-puck-v3_0-switchboard.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_0-sensorboards.dtbo pi-puck-v3_0-sensorboards.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v3_1_cameratestboard.dtbo pi-puck-v3_1_cameratestboard.dts
$DTC -@ -I dts -O dtb -W no-unit_address_vs_reg -o pi-puck-v4_0.dtbo pi-puck-v4_0.dts
