#!/bin/bash

logger -s -t run.sh "Starting test run"

WAIT_TIME_FOR_ASSOCIATION_SECS=20

now_secs=$(date +"%s")
test_start_time=$(( $now_secs+$WAIT_TIME_FOR_ASSOCIATION_SECS ))

# Only care about the first wlan device
wlan_device=$(ip -o link | awk -F: '$2 ~ /wl.*/ {print $2;}' | head -1);

random_wait=$(( $RANDOM % 5 ))
logger -s -t run.sh "Sleeping for $random_wait to avoid DHCP droppage"
sleep $random_wait

logger -s -t run.sh "Connecting to network under test"
ifdown ${wlan_device}; sleep 1; ifup ${wlan_device}
logger -s -t run.sh "Connected to network under test: $(iwconfig ${wlan_device} | head -1)"

# Work out whether we have connectivity based on whether we have any routes
#  on wlan0. If we haven't received a DHCP lease we won't have any routes.
num_wlan_routes=$(netstat -rn | grep -c "${wlan_device}$");

run_description=$(echo $@ | grep -o test-run-[0-9]*)
#tcpdump -i ${wlan_device} -w /root/wifi-test-results/pcap/$(hostname -s)-${run_description}.pcap > /root/wifi-test-results/pcap/$(hostname -s)-${run_description}.out 2>&1 &
#disown %-

# If we get 2 routes, then we couldn't get a DHCP offer and we've fallen
#  back to configuring wlan0:avahi too and we've actually got a route to
#  0.0.0.0 via wlan0 and 169.254.0.0 via wlan0.
if [ $num_wlan_routes -eq 1 ]; then
    logger -s -t run.sh "Successfully configured connectivity to target"
    COUNT=$1
    # Shift so we can pass the rest of the arguments to the test script
    shift

    # Wait for test start time (so all clients are starting simultaneously
    #  regardless of association time)
    sleep $(( $test_start_time-$(date +"%s") ))

    for i in $(seq 1 ${COUNT}); do
        # Do test stuff
        logger -s -t run.sh "running: python3 ./downloader.py $@";
        python3 ./downloader.py $@ &
    done
    wait
else
    logger -s -t run.sh "Failed to configure connectivity to target"
fi

pkill -f "tcpdump"

# Cleanup
logger -s -t run.sh "Disconnecting from network under test"
ifdown ${wlan_device}
logger -s -t run.sh "Disconnected from network under test: $(iwconfig ${wlan_device} | head -1)"

# Provide an exit code
if [ $num_wlan_routes -eq 1 ]; then
    # all good
    exit 0;
else
    # our networking was broken
    exit 1;
fi
