#!/system/xbin/bash

LOG=loadvideo.log
PCAP=/data/local/tmp/video.pcap

source loadcommon.sh

DURATION=0
IFACE="rmnet0"
MOBILE=0
PAUSE_AFTER=0
CLOSE_AFTER=0


#
# SETUP (PARSE ARGS)
#
setup()
{
	local OPTARG=$2

	while getopts "mi:p:c:" opt; do
		case $opt in
			m)
				MOBILE=1
				;;
			i)
				IFACE=$OPTARG
				;;
			p)
				PAUSE_AFTER=$OPTARG
				;;
			c)
				CLOSE_AFTER=$OPTARG
				;;
			\?)
				printf "\nInvalid option: -$OPTARG\n" >&2
				help
				;;
		esac
	done
}


#
# MAIN
#
echo -e `date +%s`"\t========== Script Launched: $0 $@ ==========" >> $LOG

setup $@
shift $((OPTIND-1))

if [ "$#" -ne 2 ]; 
    then echo -e "Please specify a YouTube URL and a wait duration (in seconds):\n$0 url duration"
    exit 1
fi
URL=$1
DURATION=$2

echo "Video starts in 20 seconds."
sleep 20

signal_spikes
sleep 5

# Cleanup
am force-stop com.android.chrome  # stop Chrome
su -c "rm -rf /data/data/com.android.chrome/cache"  # clear Chrome cache
su -c "rm -rf /data/data/com.android.chrome/files"  # close Chrome tabs

# Start tcpdump
start_tcpdump $IFACE $PCAP

# Load page
echo -e `date +%s`"\t$URL" >> $LOG
am start -a android.intent.action.VIEW -d $URL com.android.chrome
sleep 20

# "click" to play video
if [ $MOBILE -eq 1 ]; then
	# mobile site
	input tap 200 250
else
	# desktop site
	input tap 10 335
	sleep 1
	input tap 25 300
	sleep 1
	input tap 10 335
	sleep 1
	input tap 25 300
fi

echo -e `date +%s`"\tClicked play" >> $LOG


# sleep until
#	1) we're done
#	2) we press pause  OR
#	3) we close the window
if [ $PAUSE_AFTER -gt 0 ]; then
	sleep $PAUSE_AFTER
	if [ $MOBILE -eq 1 ]; then
		# mobile site
		input tap 200 250
	else
		# desktop site
		input tap 10 335
		sleep 1
		input tap 25 300
		sleep 1
	fi
	sleep $(($DURATION - $PAUSE_AFTER))

elif [ $CLOSE_AFTER -gt 0 ]; then
	sleep $CLOSE_AFTER
	am force-stop com.android.chrome  # stop Chrome
	sleep $(($DURATION - $CLOSE_AFTER))

else
	sleep $DURATION
fi

# stop tcpdump
stop_tcpdump

# dummy CPU activity to cause spikes in power reading
sleep 5
signal_spikes
