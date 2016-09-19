#!/bin/sh

set +e

#Preparing log dump file
timestamp=$(date +"%Y%m%d_%H%M%S")
timezone=$(ls -al /etc/localtime)
log_dir="/var/log/logdump"
mkdir -p $log_dir/$timestamp
log_file="$log_dir/$timestamp/logdump_$timestamp.log"
revision=$(cat /proc/device-tree/revision)
if [ -f "$serial" ]; then
        serial=$(cat /proc/device-tree/serial-number)
else
        serial=None
fi

#Append logs one by one
echo -e >> $log_file
echo "=== Release Info" >> $log_file
cat /etc/artik_release >> $log_file
cat /etc/system-release >> $log_file

echo -e >> $log_file
echo "=== H/W Info" >> $log_file
echo "Serial : $serial" >> $log_file
echo "H/W Revision : $revision" >> $log_file

echo -e >> $log_file
echo "=== Kernel Version" >> $log_file
cat /proc/version >> $log_file >> $log_file

echo -e >> $log_file
echo "=== Cmdline Info" >> $log_file
cat /proc/cmdline >> $log_file

echo -e >> $log_file
echo "=== System Info" >> $log_file
cat /proc/cpuinfo >> $log_file

echo -e >> $log_file
echo "=== System Uptime" >> $log_file
cat /proc/uptime >> $log_file

echo -e >> $log_file
echo "=== System Stat" >> $log_file
cat /proc/stat >> $log_file

echo -e >> $log_file
echo "=== Device Info" >> $log_file
cat /proc/devices >> $log_file

echo -e >> $log_file
echo "=== Timezone Info" >> $log_file
echo "$timezone" >> $log_file

echo -e >> $log_file
echo "=== Process Info" >> $log_file
echo "$(/usr/bin/ps auxfw)" >> $log_file

echo -e >> $log_file
echo "=== System Usage" >> $log_file
echo "$(/usr/bin/top -bcH -n 1)" >> $log_file

echo -e >> $log_file
echo "=== Memory Info" >> $log_file
cat /proc/meminfo >> $log_file

echo -e >> $log_file
echo "=== VM Stat" >> $log_file
cat /proc/vmstat >> $log_file

echo -e >> $log_file
echo "=== Vmalloc Stat" >> $log_file
cat /proc/vmallocinfo >> $log_file

echo -e >> $log_file
echo "=== Slab Info" >> $log_file
cat /proc/slabinfo >> $log_file

echo -e >> $log_file
echo "=== Zone Info" >> $log_file
cat /proc/zoneinfo >> $log_file

echo -e >> $log_file
echo "=== Pagetype Info" >> $log_file
cat /proc/pagetypeinfo >> $log_file

echo -e >> $log_file
echo "=== Buddy Info" >> $log_file
cat /proc/buddyinfo >> $log_file

echo -e >> $log_file
echo "=== Disk Stat" >> $log_file
cat /proc/diskstats >> $log_file

echo -e >> $log_file
echo "=== Disk Usage" >> $log_file
echo "$(/usr/bin/df -h)" >> $log_file

echo -e >> $log_file
echo "=== eMMC EXT_CSD" >> $log_file
cat /sys/kernel/debug/mmc0/mmc0\:0001/ext_csd >> $log_file

echo -e >> $log_file
echo "=== eMMC Info" >> $log_file
cat /sys/block/mmcblk0/stat >> $log_file

echo -e >> $log_file
echo "=== Journal Log" >> $log_file
journal=$(journalctl --list-boot --no-pager)
num=${journal:0:2}
if [ "$num" != " 0" ]
then
        num=-1
fi
echo "$(/usr/bin/journalctl --no-pager -b $num)" >> $log_file

#copy external logs into dump
cp /var/log/wpa_supplicant.log "$log_dir/$timestamp/" &> /dev/null
cp /var/log/dnsmasq.log "$log_dir/$timestamp/" &> /dev/null
cp -r /var/log/journal "$log_dir/$timestamp/" &> /dev/null

#compress with tar.gz and remove source directory
tar zcvfP "$log_dir/$timestamp.tar.gz" -C "$log_dir/" "$timestamp/." &> /dev/null
rm -rf "$log_dir/$timestamp"

set -e

echo "The log has been stored in $log_dir/$timestamp.tar.gz"
