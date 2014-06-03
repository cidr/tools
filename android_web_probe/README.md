Android Page Load Probes
========================

This directory contains scripts that load a list of URLs on an Android device.
There are two variants: the first, designed to measure page load time, runs on
the computer and communicates with the phone using ADB; the second, designed to
measure energy consumption, runs on the device.


Page Load Time
--------------

The python script `probe.py` takes in a list of URLs, which it loads on an
Android phone via ADB. It captures pcap traces, which it can then analyze to
extract page load times and number of bytes transferred. Use it in three
stages:

1.	Capture Traces

	To capture traces, use either the `-l` flag followed by a list of URLs on
	the command line or the `-f` flag followed by a file containing a list of
	URLs, one per line.

		./probe.py -l <url1> <url2> ...
		./probe.py -f <urlfile>

2.	Analyze Traces
	
	To extract page load times and byte counts from the traces, use the `-t`
	option to point to the directory of traces created in step 1. The results
	are pickled and saved to disk (results.pickle), for use in step 3.

		./probe.py -t <tracedir>

3.	Plot Results
	
	To plot the results of one or more set of traces, use `-r` followed by a
	list of pickled results.pickle files created in step 2.

		./probe.py -r <results1> <results2> ...


Multiple instances of the probe can run at once if multiple devices are
connected. To see a list of connected devices IDs, use `adb devices`:

	$ adb devices
	List of devices attached
	0019fd9c28207e  device
	001921431bab7e  device

Then use the `-s` option to instruct the probe to use a specific device:

	./probe.py -f <urlfile> -s 0019fd9c28207e

For more options/help, run `./probe.py -h`.


Energy Usage
------------

TODO

### pt4 File Analysis

The Monsoon Power Monitor saves logs in the `.pt4` format. In order to avoid
CSV files (they take more space and take longer to export), we process the
original .pt4 binary data. To do this, we use a [tool developed by
Brown](https://github.com/brownsys/pt4utils). To download pt4utils:

	git submodule init
	git submodule update
