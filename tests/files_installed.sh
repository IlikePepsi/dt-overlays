#!/usr/bin/bash

SERVICEPATH = /usr/lib/systemd/system
SCRIPTPATH = /usr/src
RULESPATH = /etc/udev/rules.d
FIRMWARE = /lib/firmware
CAPEMGR = /sys/devices/platform/bone_capemgr

case $1 in
	installed)
	;;
	uninstalled)
	;;
esac

