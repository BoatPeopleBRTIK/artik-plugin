Name:		artik-plugin
Summary:	ARTIK plugin files for fedora
Version:	0.1
Release:	1
Group:		System Environment/Base
License:	none

Requires:       systemd
Requires:       setup
Requires:       pulseaudio
Requires:       bluez
Requires:       connman

Source0:	%{name}-%{version}.tar.gz

%description
ARTIK plugin files for fedora

%prep
%setup -q

%install
rm -rf %{buildroot}

# determine arch and OS for rpm
mkdir -p %{buildroot}/etc/rpm
cp -rf %{_builddir}/%{name}-%{version}/platform %{buildroot}/etc/rpm

# Bluetooth
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/etc/modules-load.d
cp %{_builddir}/%{name}-%{version}/modules-load.d/dhd.conf %{buildroot}/etc/modules-load.d
mkdir -p %{buildroot}/etc/modprobe.d
cp %{_builddir}/%{name}-%{version}/modprobe.d/dhd.conf %{buildroot}/etc/modprobe.d/

mkdir -p %{buildroot}/usr/lib/systemd/system
cp %{_builddir}/%{name}-%{version}/brcm-firmware.service %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/etc/udev/rules.d
cp %{_builddir}/%{name}-%{version}/10-local.rules %{buildroot}/etc/udev/rules.d

mkdir -p  %{buildroot}/etc/bluetooth
cp -r %{_builddir}/%{name}-%{version}/bluetooth/%{TARGET}/* %{buildroot}/etc/bluetooth

# fstab
mkdir -p %{buildroot}/etc
cp %{_builddir}/%{name}-%{version}/fstab/fstab-%{TARGET} %{buildroot}/etc/fstab

# network
mkdir -p %{buildroot}/etc/sysconfig/network-scripts
cp %{_builddir}/%{name}-%{version}/network/ifcfg-eth0 %{buildroot}/etc/sysconfig/network-scripts

if [ %{TARGET} = "artik5" ]; then
cp %{_builddir}/%{name}-%{version}/modules-load.d/asix.conf %{buildroot}/etc/modules-load.d
fi

# rfkill
mkdir -p %{buildroot}/usr/lib/systemd/system
cp %{_builddir}/%{name}-%{version}/rfkill-unblock.service %{buildroot}/usr/lib/systemd/system

# audio
mkdir -p %{buildroot}/usr/lib/systemd/system
cp %{_builddir}/%{name}-%{version}/pulseaudio.service %{buildroot}/usr/lib/systemd/system
cp %{_builddir}/%{name}-%{version}/audiosetting.service %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/usr/bin
cp %{_builddir}/%{name}-%{version}/audio/%{TARGET}/audio_setting.sh %{buildroot}/usr/bin

if [ %{TARGET} = "artik710" ]; then
echo "target is artik710"
mkdir -p %{buildroot}/usr/share/alsa
cp %{_builddir}/%{name}-%{version}/audio/%{TARGET}/alsa.conf %{buildroot}/usr/share/alsa
fi

# wifi
mkdir -p %{buildroot}/etc/wifi
cp %{_builddir}/%{name}-%{version}/wifi/%{TARGET}/* %{buildroot}/etc/wifi

# adbd
mkdir -p %{buildroot}/usr/bin
cp -r %{_builddir}/%{name}-%{version}/adbd/%{TARGET}/* %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/systemd/system
cp %{_builddir}/%{name}-%{version}/adbd.service %{buildroot}/usr/lib/systemd/system

# connman
cp -r %{_builddir}/%{name}-%{version}/connman/* %{buildroot}

# Open JDK
mkdir -p %{buildroot}/etc/profile.d
cp %{_builddir}/%{name}-%{version}/open-jdk.sh %{buildroot}/etc/profile.d

# CoAP californium
mkdir -p %{buildroot}/opt/californium
cp -r %{_builddir}/%{name}-%{version}/californium/* %{buildroot}/opt/californium/

# lwM2M leshan
mkdir -p %{buildroot}/opt/leshan
cp -r %{_builddir}/%{name}-%{version}/leshan/* %{buildroot}/opt/leshan/

# artik_release
mkdir -p %{buildroot}/etc
cp %{_builddir}/%{name}-%{version}/release/%{TARGET}/artik_release %{buildroot}/etc

# systemd module load service
mkdir -p %{buildroot}/etc/systemd/system
cp %{_builddir}/%{name}-%{version}/systemd-modules-load.service %{buildroot}/etc/systemd/system

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

###############################################################################
# Bluetooth
%package bluetooth
Summary:    bluetooth
Group:		System

%description bluetooth
Bluetooth

%post bluetooth
systemctl enable brcm-firmware.service
systemctl enable bluetooth.service

%files bluetooth
%attr(0644,root,root) /etc/modules-load.d/dhd.conf
%attr(0644,root,root) /etc/modprobe.d/dhd.conf
# auto-load bcm4354 bt firmware
%attr(0644,root,root) /usr/lib/systemd/system/brcm-firmware.service
%attr(0644,root,root) /etc/udev/rules.d/10-local.rules
/etc/bluetooth/*

###############################################################################
# fstab
%package fstab
Summary:    fstab
Group:		System

%description fstab
fstab

%files fstab
%attr(0644,root,root) /etc/fstab

###############################################################################
# network
%package network
Summary:    network
Group:		System

%description network
Network Driver and DHCP configuration

%files network
%attr(0644,root,root) /etc/sysconfig/network-scripts/ifcfg-eth0
%if "%{TARGET}" == "artik5"
%attr(0644,root,root) /etc/modules-load.d/asix.conf
%endif

###############################################################################
# rfkill
%package rfkill
Summary:    rfkill
Group:		System

%description rfkill
rfkill, unblock all

%post rfkill
systemctl daemon-reload
systemctl enable rfkill-unblock.service

%files rfkill
%attr(0644,root,root) /usr/lib/systemd/system/rfkill-unblock.service

###############################################################################
# audio
%package audio
Summary:    audio
Group:		System

%description audio
audio

%post audio
systemctl daemon-reload
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

%files audio
%attr(0644,root,root) /usr/lib/systemd/system/pulseaudio.service
%attr(0755,root,root) /usr/bin/audio_setting.sh
%attr(0644,root,root) /usr/lib/systemd/system/audiosetting.service

%if "%{TARGET}" == "artik710"
%attr(0644,root,root) /usr/share/alsa/alsa.conf
%endif

###############################################################################
# Wifi
%package wifi
Summary:    wifi
Group:		System

%description wifi
wifi

%files wifi
/etc/wifi/*

###############################################################################
# adbd
%package adbd
Summary:    adbd
Group:		System

%description adbd
adbd

%files adbd
%attr(0755,root,root) /usr/bin/adbd
%attr(0755,root,root) /usr/bin/start_adbd.sh
%attr(0644,root,root) /usr/lib/systemd/system/adbd.service

###############################################################################
# connman
%package connman
Summary:	connman
Group:		System

%description connman
connman

%post connman
systemctl enable connman.service

%files connman
%attr(0644,root,root) /etc/connman/main.conf
%attr(0644,root,root) /var/lib/connman/settings

###############################################################################
# Open JDK
%package openjdk
Summary:	openjdk
Group:		System

%description openjdk
Open JDK

%files openjdk
%attr(0644,root,root) /etc/profile.d/open-jdk.sh

###############################################################################
# californium
%package californium
Summary:	CoAP californium demonstration application
Group:		Application

%description californium
californium

%files californium
%attr(0755,root,root) /opt/californium/*.jar
%attr(0644,root,root) /opt/californium/lib/*.jar

###############################################################################
# leshan
%package leshan
Summary:	lwM2M leshan demonstration application
Group:		Application

%description leshan
leshan

%files leshan
%attr(0755,root,root) /opt/leshan/*.jar
%attr(0644,root,root) /opt/leshan/lib/*.jar
