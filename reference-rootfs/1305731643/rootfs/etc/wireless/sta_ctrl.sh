#!/bin/sh

DEVICE_NAME=""
DRIVER_PATH=
CONFIG_PATH=
WORK_MODE=
OPERATE=
WIFI_NAME=
WIFI_PASSWORD=

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
		#insmod ${DRIVER_PATH}
		ifconfig wlan0 up
		sleep 1
		wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf &
		sleep 5
		wpa_cli -iwlan0 scan
		sleep 1
		wpa_cli -iwlan0 scan_results
		sleep 1
		wpa_cli -iwlan0 add_network
		wpa_cli -iwlan0 set_network 0 ssid \"$WIFI_NAME\"
		wpa_cli -iwlan0 set_network 0 psk \"$WIFI_PASSWORD\"
		wpa_cli -iwlan0 select_network 0
		wpa_cli -iwlan0 save_config
		udhcpc -b -i wlan0
		;;
	aic8800D)
		# insmod ${DRIVER_PATH}/aic8800_bsp/aic8800_bsp.ko
		# insmod ${DRIVER_PATH}/aic8800_fdrv/aic8800_fdrv.ko
		ifconfig wlan0 up
		sleep 1
		wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf &
		sleep 5
		wpa_cli -iwlan0 scan
		sleep 1
		wpa_cli -iwlan0 scan_results
		sleep 1
		wpa_cli -iwlan0 add_network
		wpa_cli -iwlan0 set_network 0 ssid \"$WIFI_NAME\"
		wpa_cli -iwlan0 set_network 0 psk \"$WIFI_PASSWORD\"
		wpa_cli -iwlan0 select_network 0
		wpa_cli -iwlan0 save_config
		udhcpc -b -i wlan0
		;;
	rk915)
		insmod ${DRIVER_PATH}
		sleep 5
		ifconfig wlan0 up
		sleep 1
		wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf &
		sleep 5
		wpa_cli -iwlan0 scan
		sleep 1
		wpa_cli -iwlan0 scan_results
		sleep 1
		wpa_cli -iwlan0 add_network
		wpa_cli -iwlan0 set_network 0 ssid \"$WIFI_NAME\"
		wpa_cli -iwlan0 set_network 0 psk \"$WIFI_PASSWORD\"
		wpa_cli -iwlan0 select_network 0
		wpa_cli -iwlan0 save_config
		udhcpc -b -i wlan0
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
		wpa_cli -i wlan0 disable_network 0
		usleep 8000
		wpa_cli -i wlan0 remove_network 0
		usleep 8000
		wpa_cli -i wlan0 save_config
		usleep 8000
		killall udhcpc > /dev/null
		usleep 8000
		killall wpa_supplicant > /dev/null
		usleep 8000
		ifconfig wlan0 down
		usleep 8000
		ifconfig usb0 down
		#rmmod ${DRIVER_PATH}
		usleep 2000
		;;
	aic8800D)
		wpa_cli -i wlan0 disable_network 0
		usleep 8000
		wpa_cli -i wlan0 remove_network 0
		usleep 8000
		wpa_cli -i wlan0 save_config
		usleep 8000
		killall udhcpc > /dev/null
		usleep 8000
		killall wpa_supplicant > /dev/null
		usleep 8000
		ifconfig wlan0 down
		usleep 8000
		ifconfig usb0 down
		usleep 2000
		# rmmod aic8800_fdrv
		# rmmod aic8800_bsp
		#usleep 2000
		;;
	rk915)
		wpa_cli -i wlan0 disable_network 0
		usleep 8000
		wpa_cli -i wlan0 remove_network 0
		usleep 8000
		wpa_cli -i wlan0 save_config
		usleep 8000
		killall udhcpc > /dev/null
		usleep 8000
		killall wpa_supplicant > /dev/null
		usleep 8000
		ifconfig wlan0 down
		usleep 8000
		ifconfig usb0 down
		rmmod ${DRIVER_PATH}
		usleep 2000
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
	echo "    device    -  wifi device name. .e.g rtl8821cs rk915 aic8800D" 
	echo "    operate   -  such as load, unload"
	echo "Example:"
	echo "  ./$self rtl8821cs load boss-5G QCKJ8888"
	echo "  ./$self rtl8821cs unload boss-5G QCKJ8888"
	exit 0
}

###############################################################################
if [ $# = 4 ]; then
	DEVICE_NAME="$1"
	OPERATE="$2"
	WIFI_NAME="$3"
	WIFI_PASSWORD="$4"
	sta_operate
else
	do_help
fi
