#!/system/xbin/bash

LOG=loadvideo.log

source loadcommon.sh


#
# MAIN
#

if [ "$#" -ne 1 ]; 
    then echo -e "Please specify a YouTube URL:\n$0 url"
    exit 1
fi

echo -e `date +%s`"\t========== Script Launched: $0 $@ ==========" >> $LOG
echo "Video starts in 20 seconds."
sleep 20

signal_spikes
sleep 5

# Cleanup
am kill-all   # kill all background procs
am force-stop com.android.chrome  # stop Chrome
su -c "rm -rf /data/data/com.android.chrome/cache"  # clear Chrome cache
su -c "rm -rf /data/data/com.android.chrome/files"  # close Chrome tabs

# Load page
echo -e `date +%s`"\t$1" >> $LOG
am start -a android.intent.action.VIEW -d $1 com.android.chrome
sleep 15

# "click" to play video
echo -e `date +%s`"Clicked play" >> $LOG
input tap 200 240
sleep 95

# dummy CPU activity to cause spikes in power reading
sleep 5
signal_spikes
