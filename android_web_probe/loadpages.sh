#!/system/xbin/bash

LOG=loadpages.log

if [ "$#" -ne 2 ]; 
    then echo -e "Please specify a protocol and a URL file:\n$0 http|https urlfile"
    exit 1
fi

echo -e `date +%s`"\t========== Script Launched: $0 $@ ==========" >> $LOG
echo "First page loads in 30 seconds. Last page will be "`tail -1 $2`
sleep 30

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
		line=$1"://"$(echo $line | awk -F "://" '{print $2}')
	fi
	
	# Load page and wait
	echo -e `date +%s`"\t$line" >> $LOG
	am start -a android.intent.action.VIEW -d $line com.android.chrome
	sleep 15
done < $2

