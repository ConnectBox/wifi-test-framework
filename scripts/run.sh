#!/bin/bash

logger -s -t run.sh "Starting test run"

WAIT_TIME_FOR_ASSOCIATION_SECS=20

now_secs=$(date +"%s")
test_start_time=$(( $now_secs+$WAIT_TIME_FOR_ASSOCIATION_SECS ))

# Only care about the first wlan device
wlan_device=$(ip -o link | awk -F: '$2 ~ /wl.*/ {print $2;}' | head -1);

logger -s -t run.sh "Connecting to network under test"
ifdown ${wlan_device}; sleep 1; ifup ${wlan_device}

logger -s -t run.sh "Connected to network under test: $(iwconfig ${wlan_device} | head -1)"

COUNT=$1
# Shift so we can pass the rest of the arguments to the test script
shift

# Wait for test start time (so all clients are starting simultaneously
#  regardless of association time)
sleep $(( $test_start_time-$(date +"%s") ))

for i in $(seq 1 ${COUNT}); do
    # Do test stuff
    python3 ./downloader.py $@ &
done

wait

logger -s -t run.sh "Disconnecting from network under test"
ifdown ${wlan_device}

logger -s -t run.sh "Disconnected from network under test: $(iwconfig ${wlan_device} | head -1)"

