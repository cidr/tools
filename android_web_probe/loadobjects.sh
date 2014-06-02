#!/system/xbin/bash

LOG=loadobjects.log
CURL=/data/local/tmp/curl

if [ "$#" -ne 2 ]; 
    then echo -e "Please specify a protocol and a URL file:\n$0 http|https urlfile"
    exit 1
fi

echo -e `date +%s`"\t========== Script Launched: $0 $@ ==========" >> $LOG
echo "First object loads in 30 seconds. Last object will be "`tail -1 $2`
sleep 30

while read line
do
	# Cleanup
	am kill-all   # kill all background procs

	# Build URL
	if [[ $line == *://* ]]
	then
		line=$1"://"$(echo $line | awk -F "://" '{print $2}')
	fi
	
	# Load object
	echo -e `date +%s`"\t$line" >> $LOG
	$CURL --cacert /data/local/ssl/certs/ca-bundle.crt -o /dev/null $line
done < $2
