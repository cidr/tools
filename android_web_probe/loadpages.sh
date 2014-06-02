#!/system/xbin/bash

LOG=loadpages.log

if [ "$#" -ne 2 ]; 
    then echo -e "Please specify a protocol and a URL file:\n$0 http|https urlfile"
    exit 1
fi

echo -e `date +%s`"\t========== Script Launched: $0 $@ ==========" >> $LOG
echo "First page loads in 20 seconds. Last page will be "`tail -1 $2`
sleep 20

# dummy CPU activity to cause spikes in power reading
for i in {0..2}
do
	for i in {0..9999}
	do
		echo $((13**99)) 1>/dev/null 2>&1
	done
	sleep 2
done
sleep 5

while read line
do
	# Cleanup
	am kill-all   # kill all background procs
	am force-stop com.android.chrome  # stop Chrome
	su -c "rm -rf /data/data/com.android.chrome/cache"  # clear Chrome cache
	su -c "rm -rf /data/data/com.android.chrome/files"  # close Chrome tabs

	# Build URL
	if [[ $line == *://* ]]
	then
		line=$(echo $line | awk -F "://" '{print $2}')
	fi
	line=$1"://"$line
	
	# Load page and wait
	echo -e `date +%s`"\t$line" >> $LOG
	am start -a android.intent.action.VIEW -d $line com.android.chrome
	sleep 20
done < $2


# dummy CPU activity to cause spikes in power reading
sleep 5
for i in {0..2}
do
	for i in {0..9999}
	do
		echo $((13**99)) 1>/dev/null 2>&1
	done
	sleep 2
done
