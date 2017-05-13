#!/bin/bash

wifi_network_under_test=$(awk -F " = " '$1 = /wifi_network_under_test/ { print $2; }' /etc/wifi_test_framework.conf)
wifi_network_default_name=$(awk -F " = " '$1 = /wifi_network_default_name/ { print $2; }' /etc/wifi_test_framework.conf)
wifi_network_default_password=$(awk -F " = " '$1 = /wifi_network_default_password/ { print $2; }' /etc/wifi_test_framework.conf)

# Disconnect previous connection
nmcli device disconnect wlan0

# Connect to the network under test
nmcli device wifi connect "${wifi_network_under_test}" ifname wlan0

echo $@
# Do test stuff
#python3 /tmp/downloader.py $@

# Disconnect from the network under test
nmcli device disconnect wlan0

# Reconnect to the default network
nmcli device wifi connect "${wifi_network_default_name}" password "${wifi_network_default_password}" ifname wlan0

