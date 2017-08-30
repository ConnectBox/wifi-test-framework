# Aim

To compare device throughput between an RT5372 dongle with an external 2db antenna and one with an internal antenna.

# Summary

When tested on identical hardware, at a distance of 20ft, the RT5372 wifi dongle with an internal antenna provides around 70% of the throughput of the RT5372 wifi dongle with an external 2db antenna.

# Background

The two devices, Pilot1 and Pilot2 are 25-unit pilot devices (256mb NEO + HAT). One of the devices has the unbranded RT5372 with a 2db external antenna that came with the pilot device ([similar model](https://www.alibaba.com/product-detail/Ralink-RT5372-Chipset-USB-Wireless-Adapter_60377343002.html)), and the other has a RT5372 with an internal antenna ([similar model](https://www.alibaba.com/product-detail/RT5372-N300-WIFI-USB-Adapter-with_1075634065.html?spm=a2700.7724838.2017115.36.3c93b095WIevhn))

Both devices appear as the same device to `lsusb`:

`Bus 004 Device 002: ID 148f:5372 Ralink Technology, Corp. RT5372 Wireless Adapter`:w

Both devices are running with a 20170827 mainline build. In the first set of experiments, Pilot1 has the dongle with the external antenna and Pilot2 has the dongle with the internal antenna. To confirm that hardware is not a factor, we ran a second set of experiments where Pilot1 has the dongle with the internal antenna and Pilot2 has the dongle with the external antenna.

For these tests the ConnectBox devices were placed at a distance of 20ft from the clients, with a clear line-of-site. The ConnectBox devices were 3ft off the ground, on a wooden shelf.

# Test Results

## Experiment 1: 8 Clients

Even with this low client count, the device with the internal antenna is unable to provide data at full speed to the clients. Noting the near-full throughput test result with 12 clients, this suggests that the internal antenna is at best able to provide 66% (8/12) of the throughput of the external antenna. The number may be lower as there was no testing done below 8 clients.

### Pilot 1 (external antenna)

![pilot1-external-8c8s]

### Pilot 2 (internal antenna)

![pilot2-internal-8c8s]

## Experiment 1: 12 Clients (480p)

The trend is even clearer with a higher client count. It is noteworthy that this experiment shows a slight degradation in performance on the device with the external antenna, even though previous tests have shown sustained full throughput for 13 clients. This shows that environmental conditions do influence test outcomes.

### Pilot 1 (external antenna)

![pilot1-external-12c12s]

### Pilot 2 (internal antenna)

![pilot2-internal-12c12s]

## Experiment 2: 12 clients (480p)

We see that performance is significantly reduced with an internal antenna, even when the hardware is swapped

### Pilot 1 (internal antenna)

![pilot1-internal-12c12s]

### Pilot 2 (external antenna)

![pilot2-external-12c12s]

## Experiment 2: 17 clients (360p)

17 clients is the expected maximum throughput in this experiment on a device with an external antenna. We see that the device with the internal antenna cannot provide this throughput, though degradation is less pronounced than the 480p tests.

### Pilot 1 (external antenna)

![pilot1-external-17c17s]

### Pilot 2 (internal antenna)

![pilot2-internal-17c17s]

## Experiment 2: 14 clients (360p)

Throughput starts to drop for the internal antenna device at 13 or 14 clients (it can maintain full throughput for 12 clients). This is 75% (13/17) of the throughput of the device with the external antenna.

### Pilot 1 (external antenna)

![pilot1-external-14c14s]

### Pilot 2 (internal antenna)

![pilot2-internal-14c14s]

[pilot1-external-8c8s]: antenna_images/pilot1-test_inventories_8c8s-480p-@20ft-pilot2-no-antenna-1708281931.png
[pilot2-internal-8c8s]: antenna_images/pilot2-test_inventories_8c8s-480p-@20ft-pilot2-no-antenna-1708281931.png
[pilot1-external-12c12s]: antenna_images/pilot1-test_inventories_12c12s-480p-@20ft-pilot2-no-antenna-1708281931.png
[pilot2-internal-12c12s]: antenna_images/pilot2-test_inventories_12c12s-480p-@20ft-pilot2-no-antenna-1708281931.png
[pilot1-internal-12c12s]: antenna_images/pilot1-test_inventories_12c12s-480p-@20ft-pilot1-no-antenna-1708272046.png
[pilot2-external-12c12s]: antenna_images/pilot2-test_inventories_12c12s-480p-@20ft-pilot1-no-antenna-1708272046.png
[pilot1-external-14c14s]: antenna_images/pilot1-test_inventories_14c14s-360p-@20ft-pilot2-no-antenna-1708281931.png
[pilot2-internal-14c14s]: antenna_images/pilot2-test_inventories_14c14s-360p-@20ft-pilot2-no-antenna-1708281931.png
[pilot1-external-17c17s]: antenna_images/pilot1-test_inventories_17c17s-360p-@20ft-pilot2-no-antenna-1708281931.png
[pilot2-internal-17c17s]: antenna_images/pilot2-test_inventories_17c17s-360p-@20ft-pilot2-no-antenna-1708281931.png
