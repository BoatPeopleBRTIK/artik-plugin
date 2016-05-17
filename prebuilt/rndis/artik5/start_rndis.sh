#!/bin/sh

GADGET_DIR=/sys/class/android_usb/android0
FUNCTIONS=rndis

if [ "`cat ${GADGET_DIR}/enable`" == "1" ]; then
	echo 0 > ${GADGET_DIR}/enable
fi

if [ "`cat ${GADGET_DIR}/functions | grep adb`" != "" ]; then
	FUNCTIONS=${FUNCTIONS},adb
fi

echo $FUNCTIONS > ${GADGET_DIR}/functions
echo 1 > ${GADGET_DIR}/enable

/sbin/ifconfig rndis0 192.168.129.3 up
/sbin/route add -net 192.168.129.0 netmask 255.255.255.0 dev rndis0
