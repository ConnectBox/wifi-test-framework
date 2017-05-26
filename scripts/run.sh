#!/bin/bash

WAIT_TIME_FOR_ASSOCIATION_SECS=20

now_secs=$(date +"%s")
test_start_time=$(( $now_secs+$WAIT_TIME_FOR_ASSOCIATION_SECS ))

wifi_network_under_test=$(awk -F " = " '$1 = /wifi_network_under_test/ { print $2; }' /etc/wifi_test_framework.conf)
wifi_network_default_name=$(awk -F " = " '$1 = /wifi_network_default_name/ { print $2; }' /etc/wifi_test_framework.conf)
wifi_network_default_password=$(awk -F " = " '$1 = /wifi_network_default_password/ { print $2; }' /etc/wifi_test_framework.conf)

# Only care about the first wlan device
wlan_device=$(ip -o link | awk -F: '$2 ~ /wl.*/ {print $2;}' | head -1);

echo -n "Before: "
iwconfig ${wlan_device} | head -1
current_wifi=$(iwconfig ${wlan_device} | head -1 | cut -d'"' -f2)

if [ "${current_wifi}" != "${wifi_network_under_test}" ]; then
    echo "Disconnecting from ${current_wifi} and connecting to ${wifi_network_under_test}"
    # Disconnect previous connection
    nmcli device disconnect ${wlan_device}
    # Connect to the network under test
    nmcli device wifi connect "${wifi_network_under_test}" \
        ifname ${wlan_device}
fi

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

if [ "${current_wifi}" != "${wifi_network_default_name}" ]; then
    echo "Disconnecting from ${current_wifi} and connecting to ${wifi_network_default_name}"
    # Disconnect from the network under test
    nmcli device disconnect ${wlan_device}
    # Reconnect to the default network
    nmcli device wifi \
        connect "${wifi_network_default_name}" \
        password "${wifi_network_default_password}" \
        ifname ${wlan_device}
fi

echo -n "After: "
iwconfig ${wlan_device} | head -1
