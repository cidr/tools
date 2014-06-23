#!/system/xbin/bash

LOG=loadvideo.log
PCAP=/data/local/tmp/video.pcap

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
am force-stop com.android.chrome  # stop Chrome
su -c "rm -rf /data/data/com.android.chrome/cache"  # clear Chrome cache
su -c "rm -rf /data/data/com.android.chrome/files"  # close Chrome tabs

# Start tcpdump
start_tcpdump $PCAP

# Load page
echo -e `date +%s`"\t$1" >> $LOG
am start -a android.intent.action.VIEW -d $1 com.android.chrome
sleep 20

# "click" to play video
input tap 10 335
sleep 1
input tap 25 300
sleep 1
input tap 10 335
sleep 1
input tap 25 300
echo -e `date +%s`"\tClicked play" >> $LOG
sleep 65

# stop tcpdump
stop_tcpdump

# dummy CPU activity to cause spikes in power reading
sleep 5
signal_spikes
