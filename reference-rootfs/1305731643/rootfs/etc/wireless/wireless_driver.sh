#!/bin/sh

DEVICE_NAME=""
DRIVER_PATH=
CONFIG_PATH=
WORK_MODE=
OPERATE=

ini_check_param ()
{
	case ${DEVICE_NAME} in
	rtl8821cs)
		#DRIVER_PATH=/lib/modules/$(uname -r)/xradio_mac.ko
		#DRIVER_PATH1=/lib/modules/$(uname -r)/xradio_core.ko
		#DRIVER_PATH2=/lib/modules/$(uname -r)/xradio_wlan.ko
		#CONFIG_PATH="etc/firmware/xr819/"
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"
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


sta_load ()
{

	case ${DEVICE_NAME} in
	rtl8821cs)
		insmod $MODULES_DIR/4.19.111/kernel/drivers/net/wireless/rockchip_wlan/rtl8821cs/8821cs.ko
		sleep 2
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv4/ip_tunnel.ko
		usleep 8000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv4/tunnel4.ko
		usleep 8000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv6/ipv6.ko
		usleep 8000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv6/mip6.ko
		usleep 8000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv6/sit.ko
		usleep 8000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv6/xfrm6_mode_beet.ko
		usleep 1000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv6/xfrm6_mode_transport.ko
		usleep 1000
		insmod $MODULES_DIR/4.19.111/kernel/net/ipv6/xfrm6_mode_tunnel.ko
		usleep 1000
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"
		exit -1;
		;;
	esac
}


sta_unload ()
{
	case ${DEVICE_NAME} in
	rtl8821cs)
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv6/xfrm6_mode_beet.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv6/xfrm6_mode_transport.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv6/xfrm6_mode_tunnel.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv6/sit.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv6/mip6.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv6/ipv6.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv4/ip_tunnel.ko
		rmmod $MODULES_DIR/4.19.111/kernel/net/ipv4/tunnel4.ko
		rmmod $MODULES_DIR/4.19.111/kernel/drivers/net/wireless/rockchip_wlan/rtl8821cs/8821cs.ko
		sleep 2
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"
		exit -1;
		;;
	esac
}


sta_operate ()
{
	ini_check_param;
	
	case ${OPERATE} in
	load)
		sta_load
		;;
	unload)
		sta_unload
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
	echo "    device    -  wifi device name. .e.g rtl8821cs"
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
	sta_operate
else
	do_help
fi
