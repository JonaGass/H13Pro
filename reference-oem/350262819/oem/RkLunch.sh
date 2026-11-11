#!/bin/sh
#
#[ -f /etc/profile.d/enable_coredump.sh ] && source /etc/profile.d/enable_coredump.sh

echo "=====>cvr_app start"
export enable_encoder_debug=0
export LOCAL_IP_ADDRESS=192.168.10.1
export LYLINK_DATA_PATH=/oem/lylink
#export TZ=UTC-08:00
export CVR_APP_DEBUG_ENABLE=1
export PRODUCT_NAME=Smartscreen
export rt_vo_disable_vop=0
cvr_app &
/etc/init.d/S00appdriver start

/oem/thermal_test.sh &
/oem/meminfo.sh &

