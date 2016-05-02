#!/bin/sh

if [ -n "$1" ]
then
echo "build $1"
else
echo "build.sh [TARGET]"
exit
fi

rm -rf ~/rpmbuild/*

mkdir ~/rpmbuild/BUILD
mkdir ~/rpmbuild/BUILDROOT
mkdir ~/rpmbuild/SOURCES

mkdir -p ./artik-plugin-0.1
cp -rf ./prebuilt/* artik-plugin-0.1
cp -rf ./units/* artik-plugin-0.1
cp -rf ./scripts/* artik-plugin-0.1
cp -rf ./configs/* artik-plugin-0.1
cp -rf ./rules/* artik-plugin-0.1

tar zcvf ~/rpmbuild/SOURCES/artik-plugin-0.1.tar.gz ./artik-plugin-0.1
rm -rf artik-plugin-0.1
rpmbuild --target=armv7hl -ba --define "TARGET $1" ./packaging/artik-plugin.spec
