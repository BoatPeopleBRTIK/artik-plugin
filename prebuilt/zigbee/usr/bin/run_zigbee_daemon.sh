#!/bin/sh
ARTIK5=`cat /proc/cpuinfo | grep -i EXYNOS3`
ARTIK530=`cat /proc/cpuinfo | grep -i s5p4418`
ARTIK10=`cat /proc/cpuinfo | grep -i EXYNOS5`

if [ "$ARTIK5" != "" ]; then
	echo ZIGBEE_TTY="-p ttySAC1" > /tmp/zigbee_tty
elif [ "$ARTIK530" != "" ]; then
	echo ZIGBEE_TTY="-p ttyAMA1" > /tmp/zigbee_tty
elif [ "$ARTIK10" != "" ]; then
	echo ZIGBEE_TTY="-p ttySAC0" > /tmp/zigbee_tty
else
	echo ZIGBEE_TTY="-n 1 -p ttySAC0" > /tmp/zigbee_tty
fi
