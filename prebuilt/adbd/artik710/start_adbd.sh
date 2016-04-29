#!/bin/sh

GADGET_DIR=/sys/kernel/config/usb_gadget/g1

#Mount ConfigFS and create Gadget
mkdir ${GADGET_DIR}

#Set default Vendor and Product IDs for now
echo 0x18D1 > ${GADGET_DIR}/idVendor
echo 0x0001 > ${GADGET_DIR}/idProduct

#Create English strings and add random deviceID
mkdir ${GADGET_DIR}/strings/0x409
echo 0123456789 > ${GADGET_DIR}/strings/0x409/serialnumber

#Update following if you want to
echo "Samsung" > ${GADGET_DIR}/strings/0x409/manufacturer
echo "Artik" > ${GADGET_DIR}/strings/0x409/product

#Create gadget configuration
mkdir ${GADGET_DIR}/configs/c.1
mkdir ${GADGET_DIR}/configs/c.1/strings/0x409
echo "Conf 1" > ${GADGET_DIR}/configs/c.1/strings/0x409/configuration
echo 120 > ${GADGET_DIR}/configs/c.1/MaxPower

#Create Adb FunctionFS function
#And link it to the gadget configuration
mkdir ${GADGET_DIR}/functions/ffs.adb
ln -s ${GADGET_DIR}/functions/ffs.adb ${GADGET_DIR}/configs/c.1/ffs.adb

mkdir -p /dev/usb-ffs/adb
mount -o uid=2000,gid=2000 -t functionfs adb /dev/usb-ffs/adb

#Start adbd application
/usr/bin/adbd&
echo $! > /run/adbd.pid
sleep 0.2
echo c0040000.dwc2otg > ${GADGET_DIR}/UDC
