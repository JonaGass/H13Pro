#!/bin/sh
###############################################################################
DEVICE_NAME=""
DRIVER_PATH=
DRIVER_PATH1=
DRIVER_PATH2=
CONFIG_PATH=
WORK_MODE=
OPERATE=
AIRPLAY=
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
	rk915)
		DRIVER_PATH=/system/lib/modules/rk915.ko
		echo "Device:${DEVICE_NAME}, ${DRIVER_PATH}"
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


ap_load ()
{
	case ${DEVICE_NAME} in
	rtl8821cs)
		#insmod ${DRIVER_PATH}
		usleep 2000
		ifconfig wlan0 up
		usleep 2000
		ifconfig wlan0 192.168.10.1 netmask 255.255.255.0
		usleep 2000
		route add default gw 192.168.10.1
		usleep 2000
		if [[ ${AIRPLAY} == "airplay" ]];then	
			/usr/bin/hostapd -B /oem/etc/rkadk/hostapd-airplay.conf &
			echo "ap_ctrl.sh file to airplay 8821"
		else
			/usr/bin/hostapd -B /oem/etc/rkadk/hostapd.conf &
			echo "ap_ctrl.sh file to carplay 8821"
		fi		
		;;
	aic8800D)
		# insmod ${DRIVER_PATH}/aic8800_bsp/aic8800_bsp.ko
		# insmod ${DRIVER_PATH}/aic8800_fdrv/aic8800_fdrv.ko
		usleep 2000
		ifconfig wlan0 up
		usleep 2000
		ifconfig wlan0 192.168.10.1 netmask 255.255.255.0
		usleep 2000
		route add default gw 192.168.10.1
		usleep 2000
		if [[ ${AIRPLAY} == "airplay" ]];then	
			/usr/sbin/hostapd -B /oem/etc/rkadk/hostapd-airplay.conf &
			echo "ap_ctrl.sh file to airplay 8800"
		else
			/usr/sbin/hostapd -B /oem/etc/rkadk/hostapd.conf &
		fi

		;;
	rk915)
		insmod ${DRIVER_PATH}
		sleep 5
		ifconfig wlan0 up
		usleep 2000
		ifconfig wlan0 192.168.10.1 netmask 255.255.255.0
		usleep 2000
		route add default gw 192.168.10.1
		usleep 2000
		/usr/bin/hostapd -B /oem/etc/rkadk/hostapd-rk915.conf &
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"
		exit -1;
		;;
	esac
}


ap_unload ()
{
	case ${DEVICE_NAME} in
	rtl8821cs)
		killall hostapd
		;;
	aic8800D)
		killall hostapd
		usleep 6000
		# rmmod aic8800_fdrv
		# rmmod aic8800_bsp
		#usleep 6000
		;;
	rk915)
		ifconfig wlan0 down
		usleep 6000
		rmmod ${DRIVER_PATH}
		usleep 2000
		;;
	*)
		echo "Device:${DEVICE_NAME} is not supported!"

		exit -1;
		;;
	esac
}


ap_operate ()
{
	ini_check_param;
	
	case ${OPERATE} in
	load)
		ap_load
		;;
	unload)
		ap_unload
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
	echo "    device    -  wifi device name. .e.g rtl8821cs rk915 aic8800D"
	echo "    operate   -  such as load, unload"
	echo "Example:"
	echo "  ./$self rtl8821cs load or ./$self rtl8821cs load airplay "
	echo "  ./$self rtl8821cs unload"
	exit 0
}

###############################################################################
if [ $# = 2 ]; then
	DEVICE_NAME="$1"
	OPERATE="$2"
	echo "====$2===++++++aaa++++++++++++++="
	ap_operate
elif [ $# = 3 ];then
	DEVICE_NAME="$1"
	OPERATE="$2"
	AIRPLAY="$3"
	echo "====$3===++++++++ccc++++++++++++="
	ap_operate
else
	do_help
fi
