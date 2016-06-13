%define __jar_repack 0

Name:		artik-plugin
Summary:	ARTIK plugin files for fedora
Version:	0.2
Release:	1
Group:		System Environment/Base
License:	none

Requires:       systemd
Requires:       setup
Requires:       pulseaudio
Requires:       bluez
Requires:       connman
Requires:       dnsmasq
Requires:       java-1.8.0-openjdk

Source0:	%{name}-%{version}.tar.gz

%description
ARTIK plugin files for fedora

%prep
%setup -q

%install
rm -rf %{buildroot}

# determine arch and OS for rpm
mkdir -p %{buildroot}/etc/rpm
cp -f scripts/platform %{buildroot}/etc/rpm

mkdir -p %{buildroot}/etc/modules-load.d
cp scripts/modules-load.d/* %{buildroot}/etc/modules-load.d

mkdir -p %{buildroot}/usr/lib/systemd/system
cp scripts/units/bt-wifi-on.service %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/etc/modprobe.d
cp scripts/modprobe.d/dhd.conf %{buildroot}/etc/modprobe.d/

mkdir -p  %{buildroot}/etc/bluetooth
cp -r prebuilt/bluetooth/* %{buildroot}/etc/bluetooth

mkdir -p %{buildroot}/usr/lib/systemd/system
cp scripts/units/brcm-firmware.service %{buildroot}/usr/lib/systemd/system
cp scripts/units/rfkill-unblock.service %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/etc/udev/rules.d
cp scripts/rules/10-local.rules %{buildroot}/etc/udev/rules.d

mkdir -p %{buildroot}/etc/profile.d
cp scripts/open-jdk.sh %{buildroot}/etc/profile.d

# fstab
mkdir -p %{buildroot}/etc
cp prebuilt/fstab/fstab-* %{buildroot}/etc/

# network
mkdir -p %{buildroot}/etc/sysconfig/network-scripts
cp prebuilt/network/ifcfg-eth0 %{buildroot}/etc/sysconfig/network-scripts

mkdir -p %{buildroot}/usr/bin
cp prebuilt/network/zigbee_version %{buildroot}/usr/bin

cp -r prebuilt/connman/* %{buildroot}

# audio
mkdir -p %{buildroot}/usr/lib/systemd/system
cp scripts/units/pulseaudio.service %{buildroot}/usr/lib/systemd/system
cp scripts/units/audiosetting.service %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/usr/share/alsa
cp -r prebuilt/audio/* %{buildroot}/usr/bin

# wifi
mkdir -p %{buildroot}/etc/wifi
cp -r prebuilt/wifi/* %{buildroot}/etc/wifi

# adbd
mkdir -p %{buildroot}/usr/bin
cp -r prebuilt/adbd/%{TARGET}/* %{buildroot}/usr/bin
cp -r prebuilt/rndis/%{TARGET}/* %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/systemd/system
cp scripts/units/adbd.service %{buildroot}/usr/lib/systemd/system
cp scripts/units/rndis.service %{buildroot}/usr/lib/systemd/system
cp scripts/rules/99-adb-restart.rules %{buildroot}/etc/udev/rules.d

# CoAP californium
mkdir -p %{buildroot}/opt/californium
cp -r prebuilt/californium/* %{buildroot}/opt/californium/

# lwM2M leshan
mkdir -p %{buildroot}/opt/leshan
cp -r prebuilt/leshan/* %{buildroot}/opt/leshan/

# artik_release
mkdir -p %{buildroot}/etc
cp scripts/release/%{TARGET}/artik_release %{buildroot}/etc

# systemd module load service
mkdir -p %{buildroot}/etc/systemd/system
cp scripts/units/systemd-modules-load.service %{buildroot}/etc/systemd/system

# booting done service
mkdir -p %{buildroot}/usr/bin
cp scripts/booting-done.sh %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/systemd/system
cp scripts/units/booting-done.service %{buildroot}/usr/lib/systemd/system

%post
# Setting default runlevel to multi-user text mode
rm -f /etc/systemd/system/default.target
ln -s /lib/systemd/system/multi-user.target /etc/systemd/system/default.target

# Limit journal size
sed -i "s/#SystemMaxUse=/SystemMaxUse=10M/" /etc/systemd/journald.conf

# wpa_supplicant
sed -i 's/INTERFACES=\"\"/INTERFACES=\"-iwlan0\"/g' /etc/sysconfig/wpa_supplicant
sed -i 's/DRIVERS=\"\"/DRIVERS=\"-Dnl80211\"/g' /etc/sysconfig/wpa_supplicant

# Enable units
systemctl enable systemd-timesyncd.service
systemctl enable systemd-resolved.service
systemctl enable booting-done.service
systemctl enable rfkill-unblock.service

# systemd module load service
systemctl enable systemd-modules-load.service

# Dnsmasq setting
sed -i 's/\#except-interface=/except-interface=lo/g'  /etc/dnsmasq.conf

# Install java alternatives
/usr/sbin/alternatives --install /usr/bin/java java /usr/java/default/jre/bin/java 1
/usr/sbin/alternatives --install /usr/bin/javaws javaws /usr/java/default/jre/bin/javaws 1
/usr/sbin/alternatives --install /usr/bin/javac javac /usr/java/default/bin/javac 1
/usr/sbin/alternatives --install /usr/bin/jar jar /usr/java/default/bin/jar 1

# Sync after sshd key generation
echo "ExecStartPost=/usr/bin/sync" >> /usr/lib/systemd/system/sshd-keygen.service
sed -i 's/ConditionPathExists/ConditionFileNotEmpty/g' /usr/lib/systemd/system/sshd-keygen.service

###############################################################################
# artik-plugin

%files
%attr(0644,root,root) /etc/rpm/platform
%attr(0644,root,root) /etc/artik_release
%attr(0644,root,root) /etc/systemd/system/systemd-modules-load.service
%attr(0755,root,root) /usr/bin/booting-done.sh
%attr(0644,root,root) /usr/lib/systemd/system/booting-done.service
%attr(0644,root,root) /etc/profile.d/open-jdk.sh
%attr(0644,root,root) /usr/lib/systemd/system/rfkill-unblock.service

%attr(0755,root,root) /opt/californium/*.jar
%attr(0644,root,root) /opt/californium/lib/*.jar
%attr(0755,root,root) /opt/leshan/*.jar
%attr(0644,root,root) /opt/leshan/lib/*.jar

###############################################################################
# Bluetooth
# ARTIK common
%package bluetooth-common
Summary:    bluetooth
Group:		System
Requires:	bluez

%description bluetooth-common
Bluetooth

%post bluetooth-common
systemctl enable bluetooth.service

mv /etc/bluetooth/common/* /etc/bluetooth/*
rm -r /etc/bluetooth/common

%files bluetooth-common
%attr(0644,root,root) /etc/udev/rules.d/10-local.rules
/etc/bluetooth/common

# ARTIK5
%package bluetooth-artik5
Summary:    bluetooth
Group:		System
Requires:	bluez

%description bluetooth-artik5
Bluetooth

%post bluetooth-artik5
systemctl enable brcm-firmware.service
systemctl enable bluetooth.service

mv /etc/bluetooth/artik5/* /
rm -r /etc/bluetooth/artik5

%files bluetooth-artik5
%attr(0644,root,root) /etc/modules-load.d/dhd.conf
%attr(0644,root,root) /etc/modprobe.d/dhd.conf
%attr(0644,root,root) /usr/lib/systemd/system/brcm-firmware.service
/etc/bluetooth/artik5/*

# ARTIK10
%package bluetooth-artik10
Summary:    bluetooth
Group:		System
Requires:	bluez

%description bluetooth-artik10
Bluetooth

%post bluetooth-artik10
systemctl enable brcm-firmware.service
systemctl enable bluetooth.service

mv /etc/bluetooth/artik10/* /
rm -r /etc/bluetooth/artik10

%files bluetooth-artik10
%attr(0644,root,root) /etc/modules-load.d/dhd.conf
%attr(0644,root,root) /etc/modprobe.d/dhd.conf
%attr(0644,root,root) /usr/lib/systemd/system/brcm-firmware.service
/etc/bluetooth/artik10/*

# ARTIK530
%package bluetooth-artik530
Summary:    bluetooth
Group:		System
Requires:	bluez

%description bluetooth-artik530
Bluetooth

%post bluetooth-artik530
systemctl enable bluetooth.service
systemctl enable bt-wifi-on.service

mv /etc/bluetooth/artik530/* /
rm -r /etc/bluetooth/artik530

%files bluetooth-artik530
%attr(0644,root,root) /etc/modules-load.d/mrvl.conf
%attr(0644,root,root) /usr/lib/systemd/system/bt-wifi-on.service
/etc/bluetooth/artik530/*

# ARTIK710
%package bluetooth-artik710
Summary:    bluetooth
Group:		System
Requires:	bluez

%description bluetooth-artik710
Bluetooth

%post bluetooth-artik710
systemctl enable brcm-firmware.service
systemctl enable bluetooth.service

mv /etc/bluetooth/artik710/* /
rm -r /etc/bluetooth/artik710

%files bluetooth-artik710
%attr(0644,root,root) /etc/modules-load.d/dhd.conf
%attr(0644,root,root) /etc/modprobe.d/dhd.conf
%attr(0644,root,root) /usr/lib/systemd/system/brcm-firmware.service
/etc/bluetooth/artik710/*

###############################################################################
# fstab
# ARTIK5
%package fstab-artik5
Summary:    fstab
Group:		System

%description fstab-artik5
fstab

%post fstab-artik5
rm -f /etc/fstab
mv /etc/fstab-%{TARGET} /etc/fstab

%files fstab-artik5
%attr(0644,root,root) /etc/fstab-artik5

# ARTIK10
%package fstab-artik10
Summary:    fstab
Group:		System

%description fstab-artik10
fstab

%post fstab-artik10
rm -f /etc/fstab
mv /etc/fstab-%{TARGET} /etc/fstab

%files fstab-artik10
%attr(0644,root,root) /etc/fstab-artik10

# ARTIK530
%package fstab-artik530
Summary:    fstab
Group:		System

%description fstab-artik530
fstab

%post fstab-artik530
rm -f /etc/fstab
mv /etc/fstab-%{TARGET} /etc/fstab

%files fstab-artik530
%attr(0644,root,root) /etc/fstab-artik530

# ARTIK710
%package fstab-artik710
Summary:    fstab
Group:		System

%description fstab-artik710
fstab

%post fstab-artik710
rm -f /etc/fstab
mv /etc/fstab-%{TARGET} /etc/fstab

%files fstab-artik710
%attr(0644,root,root) /etc/fstab-artik710

###############################################################################
# network
# ARTIK common
%package network-common
Summary:    network
Group:		System

%description network-common
Network Driver and DHCP configuration

%post network-common
systemctl enable connman.service

%files network-common
%attr(0644,root,root) /etc/sysconfig/network-scripts/ifcfg-eth0
%attr(0755,root,root) /usr/bin/zigbee_version
%attr(0644,root,root) /etc/connman/main.conf
%attr(0644,root,root) /var/lib/connman/settings

# ARTIK5
%package network-artik5
Summary:    network
Group:		System

%description network-artik5
Network Driver and DHCP configuration

%files network-artik5
%attr(0644,root,root) /etc/modules-load.d/asix.conf
###############################################################################
# audio
# ARTIK common
%package audio-common
Summary:    audio
Group:		System
Requires:       pulseaudio

%description audio-common
audio

%post audio-common
systemctl enable pulseaudio.service
systemctl enable audiosetting.service

sed -i 's/load-module module-udev-detect/load-module module-udev-detect tsched=0/g' /etc/pulse/default.pa
echo "load-module module-switch-on-connect" >> /etc/pulse/default.pa
cp /etc/pulse/default.pa /etc/pulse/system.pa

/usr/sbin/usermod -G pulse-access root
/usr/sbin/usermod -a -G audio pulse

# pulseaudio settings for bluetooth a2dp_sink
set -i '/<allow own="org.pulseaudio.Server"\/>/a \ \ \ \ <allow send_interface="org.freedesktop.DBus.ObjectManager"/>' /etc/dbus-1/system.d/pulseaudio-system.conf
sed -i '/<allow own="org.pulseaudio.Server"\/>/a \ \ \ \ <allow send_destination="org.bluez"/>' /etc/dbus-1/system.d/pulseaudio-system.conf

sed -i '/<\/busconfig>/i \ \ <policy user="pulse">\n\ \ \ \ <allow send_destination="org.bluez"/>\n\ \ \ \ <allow send_interface="org.freedesktop.DBus.ObjectManager"/>\n\ \ <\/policy>\n'  /etc/dbus-1/system.d/bluetooth.conf

%files audio-common
%attr(0644,root,root) /usr/lib/systemd/system/pulseaudio.service
%attr(0644,root,root) /usr/lib/systemd/system/audiosetting.service

# ARTIK5
%package audio-artik5
Summary:    audio
Group:		System
Requires:       pulseaudio

%description audio-artik5
audio

%post audio-artik5
rm /usr/bin/audio_setting.sh
mv /usr/bin/artik5/audio_setting.sh /usr/bin
rm -r /usr/bin/artik5

%files audio-artik5
%attr(0755,root,root) /usr/bin/artik5/audio_setting.sh

# ARTIK10
%package audio-artik10
Summary:    audio
Group:		System
Requires:       pulseaudio

%description audio-artik10
audio

%post audio-artik10
rm /usr/bin/audio_setting.sh
mv /usr/bin/artik10/audio_setting.sh /usr/bin
rm -r /usr/bin/artik10

%files audio-artik10
%attr(0755,root,root) /usr/bin/artik10/audio_setting.sh

# ARTIK530
%package audio-artik530
Summary:    audio
Group:		System
Requires:       pulseaudio

%description audio-artik530
audio

%post audio-artik530
rm /usr/bin/audio_setting.sh
mv /usr/bin/artik530/audio_setting.sh /usr/bin
mv /usr/bin/artik530/alsa.conf /usr/share/alsa
rm -r /usr/bin/artik530

%files audio-artik530
%attr(0755,root,root) /usr/bin/artik530/audio_setting.sh
%attr(0644,root,root) /usr/bin/artik530/alsa.conf

# ARTIK710
%package audio-artik710
Summary:    audio
Group:		System
Requires:       pulseaudio

%description audio-artik710
audio

%post audio-artik710
rm /usr/bin/audio_setting.sh
mv /usr/bin/artik710/audio_setting.sh /usr/bin
mv /usr/bin/artik710/alsa.conf /usr/share/alsa
rm -r /usr/bin/artik710

%files audio-artik710
%attr(0755,root,root) /usr/bin/artik710/audio_setting.sh
%attr(0644,root,root) /usr/bin/artik710/alsa.conf

###############################################################################
# Wifi
# ARTIK5
%package wifi-artik5
Summary:    wifi
Group:		System

%description wifi-artik5
wifi

%post wifi-artik5
mv /etc/wifi/artik5/* /etc/wifi
rm -r /etc/wifi/artik10

%files wifi-artik5
/etc/wifi/artik5/*

# ARTIK10
%package wifi-artik10
Summary:    wifi
Group:		System

%description wifi-artik10
wifi

%post wifi-artik10
mv /etc/wifi/artik10/* /etc/wifi
rm -r /etc/wifi/artik10

%files wifi-artik10
/etc/wifi/artik10/*

# ARTIK530
%package wifi-artik530
Summary:    wifi
Group:		System

%description wifi-artik530
wifi

%post wifi-artik530
mkdir -p /usr/lib/firmware
mv /etc/wifi/artik530/* /usr/lib/firmware
rm -r /etc/wifi/artik530

%files wifi-artik530
/etc/wifi/artik530/*

# ARTIK710
%package wifi-artik710
Summary:    wifi
Group:		System

%description wifi-artik710
wifi

%post wifi-artik710
mv /etc/wifi/artik710/* /etc/wifi
rm -r /etc/wifi/artik710

%files wifi-artik710
/etc/wifi/artik710/*
###############################################################################
# usb gadget
%package usb-common
Summary:    usb
Group:		System

%description usb-common
usb

%files usb-common
%attr(0755,root,root) /usr/bin/adbd
%attr(0755,root,root) /usr/bin/start_adbd.sh
%attr(0755,root,root) /usr/bin/start_rndis.sh
%attr(0644,root,root) /usr/lib/systemd/system/adbd.service
%attr(0644,root,root) /usr/lib/systemd/system/rndis.service
%attr(0644,root,root) /etc/udev/rules.d/99-adb-restart.rules
