#!/bin/sh

setusbconfig none
ifconfig lo up
lylinkui &
killall dhcpcd
env LYLINK_DATA_PATH=/oem/lylink lylinkapp &