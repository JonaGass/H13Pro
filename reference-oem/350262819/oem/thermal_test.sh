#!/bin/sh
#

THERMAL_FILE="/mnt/sdcard/thermal.sh"
WORK_FILE="/mnt/sdcard/temperature.txt"
WORK_DIR="/mnt/sdcard"

echo "thermal test start------------>"
sleep 20

if [ -d ${WORK_DIR} ];then
	echo "${WORK_DIR} exist, continue."
else
	echo "${WORK_DIR} not exist, exit."
	exit		
fi

if [ -f ${WORK_FILE} ];then
    echo "change old ${WORK_FILE}"
	# rm ${WORK_FILE}
	cd ${WORK_DIR}
	echo $RANDOM | cut -c 5-15
	mv ${WORK_FILE} temperature_$RANDOM.txt
	touch temperature.txt
else
	echo "${WORK_FILE} not exist, exit."
	exit
fi

if [ -f ${WORK_FILE} ];then
        echo "${WORK_FILE} exist, continue."
else
        echo "${WORK_FILE} not exist, exit."
        exit
fi
a=0

while true
do
	a=$(($a+1))
	#time=`date +%H:%M:%S`
	tmp=$(cat /sys/class/thermal/thermal_zone0/temp)
	tmp1=$(cat /sys/class/thermal/thermal_zone1/temp)

	#echo "${time} ---> ${tmp}"  >> ${WORK_FILE}
	echo "$a ---- [0]CPU=${tmp}  [1]GPU=${tmp1}"  >> ${WORK_FILE}
	sleep 10
done


