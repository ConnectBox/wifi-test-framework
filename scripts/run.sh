#!/bin/bash

WAIT_TIME_FOR_ASSOCIATION_SECS=20

now_secs=$(date +"%s")
test_start_time=$(( $now_secs+$WAIT_TIME_FOR_ASSOCIATION_SECS ))

# Only care about the first wlan device
wlan_device=$(ip -o link | awk -F: '$2 ~ /wl.*/ {print $2;}' | head -1);

echo "Connecting to network under test"
ifdown ${wlan_device}; sleep 1; ifup ${wlan_device}

echo -n "During: "
iwconfig ${wlan_device} | head -1
current_wifi=$(iwconfig ${wlan_device} | head -1 | cut -d'"' -f2)

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

echo "Disconnecting from network under test"
ifdown ${wlan_device}

echo -n "After: "
iwconfig ${wlan_device} | head -1

