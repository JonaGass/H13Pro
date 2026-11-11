#!/bin/sh

SDCARD_PATH=/dev/mmcblk2

echo Start fdisk SDCARD:${SDCARD}

umount $SDCARD_PATH

case "$1" in
	n)
		echo "new sdcard partition start..."
		echo -e  "n\np\n1\n\n\nw"  | fdisk $SDCARD_PATH
		;;
	d)
		echo "delete sdcard partition start..."
		echo -e  "d\n1\nw"  | fdisk $SDCARD_PATH
		echo -e  "d\n2\nw"  | fdisk $SDCARD_PATH
		echo -e  "d\n3\nw"  | fdisk $SDCARD_PATH
		echo -e  "d\n4\nw"  | fdisk $SDCARD_PATH
		;;
	*)
		echo "Usage: ./sdcard_fdisk.sh [n|d]"
		;;
esac

exit 0