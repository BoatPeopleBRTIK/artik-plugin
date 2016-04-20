#Mount ConfigFS and create Gadget
mount -t configfs none /sys/kernel/config
mkdir /sys/kernel/config/usb_gadget/g1
cd /sys/kernel/config/usb_gadget/g1

#Set default Vendor and Product IDs for now
echo 0x18D1 > idVendor
echo 0x0001 > idProduct

#Create English strings and add random deviceID
mkdir strings/0x409
echo 0123459876 > strings/0x409/serialnumber

#Update following if you want to
echo "Samsung" > strings/0x409/manufacturer
echo "Artik" > strings/0x409/product

#Create gadget configuration
mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo "Conf 1" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

#Create Adb FunctionFS function
#And link it to the gadget configuration
killall adbd
mkdir functions/ffs.adb
ln -s /sys/kernel/config/usb_gadget/g1/functions/ffs.adb /sys/kernel/config/usb_gadget/g1/configs/c.1/ffs.adb

#Start adbd application
mkdir -p /dev/usb-ffs/adb
mount -o uid=2000,gid=2000 -t functionfs adb /dev/usb-ffs/adb
/usr/bin/adbd&
sleep 1
echo c0040000.dwc2otg > /sys/kernel/config/usb_gadget/g1/UDC
