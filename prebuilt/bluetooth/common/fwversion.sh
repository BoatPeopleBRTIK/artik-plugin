#!/bin/sh
btmon &
sleep 1
hcitool cmd 04 01
pkill btmon
