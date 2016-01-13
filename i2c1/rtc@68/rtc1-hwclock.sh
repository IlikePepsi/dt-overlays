#!/usr/bin/bash

SERVICE=systemd-timesyncd.service

readonly SCRIPT_NAME=$(basename $0)

log() {
	echo "$@"
	logger -p user.notice -t $SCRIPT_NAME "$@"
}

err() {
	echo "$@" >&2
	logger -p user.error -t $SCRIPT_NAME "$@"
}

has_failed() {
	if [ $1 = 'active' ]; then
		return 0
	else
		return 1
	fi
}

case $1 in
	start)
		hwclock -r &>/dev/null
		if [ $? != 0 ]; then
			err "hwclock not accessible.."
			exit 1
		fi
		has_failed $(systemctl status $SERVICE | awk '/Active:[[:space:]]/ {print $2}')
		if [ $? != 0 ]; then
			# timesyncd is not running, read system time from hwclock
			err "systemd-timesyncd is not running, adjusting system clock"
			hwclock --hctosys --utc
			if [ $? != 0 ]; then
				err "unexpected error, could not read hwclock"
				exit 1
			else
				log "system clock set to $(date)"
				exit 0
			fi
		else
			# timesyncd is running, leave everything as it is
			log "systemd-timesyncd is running, no action needed"
			exit 0
		fi
	;;
	stop)
		hwclock -r &>/dev/null
		if [ $? != 0 ]; then
			err "hwclock not accessible.."
			exit 1
		fi
		has_failed $(systemctl status $SERVICE | awk '/Active:[[:space:]]/ {print $2}')
		if [ $? != 0 ]; then
			# timesynd is not running, leave everything as it is
			log "systemd-timesyncd is not running, no action needed"
			exit 0
		else
			# timesyncd is running, write system time to hwclock
			log "systemd-timesyncd is running, adjusting hwclock"
			hwclock --systohc --utc
			if [ $? != 0 ]; then
				err "unexpected error, could not write to hwclock"
				exit 1
			else
				log "hwclock set to $(hwclock -r)"
				exit 0
			fi
		fi
	;;
	esac
