#!/bin/sh
set -e

if [ `id -u` -eq 0 ]; then
	/usr/share/system-config-lvm/system-config-lvm.py;
else
	su-to-root -X -c "/usr/bin/system-config-lvm";
fi
