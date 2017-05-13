#!/bin/bash

wifi_network_under_test=$(awk -F " = " '$1 = /wifi_network_under_test/ { print $2; }' /etc/wifi_test_framework.conf)
wifi_network_default_name=$(awk -F " = " '$1 = /wifi_network_default_name/ { print $2; }' /etc/wifi_test_framework.conf)
wifi_network_default_password=$(awk -F " = " '$1 = /wifi_network_default_password/ { print $2; }' /etc/wifi_test_framework.conf)

current_wifi=$(iwconfig wlan0 | head -1 | cut -d'"' -f2)

echo "Before"
iwconfig wlan0 | head -1

# XXX if multiple clients might need to wait if it's unassociated at this stage (while loop?)
if [ "${current_wifi}" != "${wifi_network_under_test}" ]; then
    echo "Disconnecting from ${current_wifi} and connecting to ${wifi_network_under_test}"
    # Disconnect previous connection
    nmcli device disconnect wlan0
    # Connect to the network under test
    nmcli device wifi connect "${wifi_network_under_test}" \
        ifname wlan0
fi

echo "During"
iwconfig wlan0 | head -1

# Do test stuff
python3 /tmp/downloader.py $@

current_wifi=$(iwconfig wlan0 | head -1 | cut -d'"' -f2)

# XXX if multiple clients might need to wait if it's unassociated at this stage (while loop?)

if [ "${current_wifi}" != "${wifi_network_default_name}" ]; then
    echo "Disconnecting from ${current_wifi} and connecting to ${wifi_network_default_name}"
    # Disconnect from the network under test
    nmcli device disconnect wlan0
    # Reconnect to the default network
    nmcli device wifi \
        connect "${wifi_network_default_name}" \
        password "${wifi_network_default_password}" \
        ifname wlan0
fi

echo "After"
iwconfig wlan0 | head -1
