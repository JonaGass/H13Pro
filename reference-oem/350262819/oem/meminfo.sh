WORK_FILE="/mnt/sdcard/ddr_avai.log"

sleep 20

if [ -f ${WORK_FILE} ];then
	echo "${WORK_FILE} exist, continue."
else
	echo "${WORK_FILE} not exist, exit."
	exit
fi

while true
do
    date >> /mnt/sdcard/ddr_avai.log
    cat /proc/meminfo | grep MemAvailable >> /mnt/sdcard/ddr_avai.log
    sleep 60
done