#!/bin/sh
#

/etc/init.d/S10udev start
/etc/init.d/S40network start
echo usb_adb_en > /tmp/.usb_config
/etc/init.d/S50usbdevice start

echo 7 > /proc/sys/kernel/printk



