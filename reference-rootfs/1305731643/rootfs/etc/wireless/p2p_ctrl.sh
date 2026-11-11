#!/bin/sh
###############################################################################
DEVICE_NAME=""
DRIVER_PATH=
DRIVER_PATH1=
DRIVER_PATH2=
CONFIG_PATH=
WORK_MODE=
OPERATE=
###############################################################################

ini_check_param ()
{
	case ${DEVICE_NAME} in
    rtl8821cs)
		echo "Device:${DEVICE_NAME} is buildin kernel."
        ;;
    aic8800D)
		echo "Device:${DEVICE_NAME} is modules."
		DRIVER_PATH=/lib/modules/4.19.111/kernel/drivers/net/wireless/aic8800
        ;;
	*)
		echo "Device:${DEVICE_NAME} is not support!"
		exit -1;
		;;
	esac
	
	case ${OPERATE} in
	load)
		;;
	unload)
		;;
	*)
		echo "Don't support this:${OPERATE} operate!"
		exit -1;
		;;
	esac
	
}


p2p_load ()
{
	case ${DEVICE_NAME} in
	rtl8821cs)
		ifconfig wlan0 192.168.10.1
		usleep 200
		route add 192.168.10.1 wlan0
		usleep 200
		/usr/bin/wpa_supplicant -i wlan0 -c /oem/etc/rkadk/p2p.conf -B
		usleep 2000
		wpa_cli p2p_group_add freq=5180
		usleep 2000
		;;
	aic8800D)
		# insmod ${DRIVER_PATH}/aic8800_bsp/aic8800_bsp.ko
		# insmod ${DRIVER_PATH}/aic8800_fdrv/aic8800_fdrv.ko
		ifconfig p2p0 192.168.10.1
		usleep 200
		route add 192.168.10.1 p2p0
		usleep 200
		/usr/bin/wpa_supplicant -i p2p0 -c /oem/etc/rkadk/p2p.conf -B
		usleep 2000
		wpa_cli -ip2p0 p2p_group_add freq=5180
		usleep 2000
		wpa_cli wps_pbc
		udhcpd /etc/udhcpd.conf
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"
		exit -1;
		;;
	esac
}


p2p_unload ()
{
	case ${DEVICE_NAME} in
	rtl8821cs)
		killall wpa_cli
		killall wpa_supplicant
		usleep 200000
		;;
	aic8800D)
		killall wpa_cli
		killall wpa_supplicant
		usleep 6000
		# rmmod aic8800_fdrv
		# rmmod aic8800_bsp
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"

		exit -1;
		;;
	esac
}


p2p_operate ()
{
	ini_check_param;
	
	case ${OPERATE} in
	load)
		p2p_load
		;;
	unload)
		p2p_unload
		;;
	*)
		echo "Don't support this:${OPERATE} operate!"
		exit -1;
		;;
	esac
}


do_help ()
{
	self=`basename $0`
	echo "Usage:"
	echo "  ./$self device operate"
	echo "    device    -  wifi device name. .e.g rtl8821cs aic8800D"
	echo "    operate   -  such as load, unload"
	echo "Example:"
	echo "  ./$self rtl8821cs load"
	echo "  ./$self rtl8821cs unload"
	exit 0
}

###############################################################################
if [ $# = 2 ]; then
	DEVICE_NAME="$1"
	OPERATE="$2"
	p2p_operate
else
	do_help
fi
