#!/bin/sh

GADGET_DIR=/sys/class/android_usb/android0
FUNCTIONS=adb

if [ "`cat ${GADGET_DIR}/enable`" == "1" ]; then
	echo 0 > ${GADGET_DIR}/enable
fi

if [ "`cat ${GADGET_DIR}/functions | grep rndis`" != "" ]; then
	FUNCTIONS=${FUNCTIONS},rndis
fi

echo ${FUNCTIONS} > ${GADGET_DIR}/functions
echo 1 > ${GADGET_DIR}/enable

/usr/bin/adbd&
echo $! > /run/adbd.pid
