# Aim

To compare throughput of Arbian legacy and mainline images

See the [reference](reference.md) for info on test methodology and advice when reading the graphs.

# Summary

The mainline image clearly outperforms the legacy image on identical hardware as clients are added. The legacy device reaches a tipping point at 7 clients, and additional clients degrade performance signficantly, while the mainline image offers consistent performance with these additional clients.

# Background

The two devices, Pilot1 and Pilot2 are 25-unit pilot devices (256mb NEO + HAT + unbranded RT5372).

Pilot2 is running an unmodified 20170809 mainline build.

Pilot1 is running a 20170714 legacy build with the same 802.11n fixes that landed in the 20170809 mainline build.

For these tests the ConnectBox devices were placed at a distance of 20ft from the clients, with a clear line-of-site. The ConnectBox devices were 3ft off the ground, on a wooden shelf.

# Test Results

Each client is attempting to stream at 480p.

## 7 Clients

Equivalent performance between legacy and mainline.

### Legacy

![legacy-7c7s]

### Mainline

![mainline-7c7s]

## 8 Clients

Mainline (pilot2) provides full throughput for the entire test. On the legacy device (pilot1) at least one client is receiving data at ~40% of the attempted throughput, which causes the test to run for a lot longer (even after the well performing clients have finished). Additionally, we see bursting above the desired throughput rate, which only happens when device is unevenly allocating bandwidth between clients.

### Legacy

![legacy-8c8s]

### Mainline

![mainline-8c8s]

## 9 Clients

Mainline (pilot2) provides full throughput for the entire test. On the legacy device (pilot1), 2 clients are receiving 70-100% attempted throughput and 2 clients are receiving below 70% of the throughput with one of those receiving ~20% of the attempted throughput. Again we see bursting, showing uneven allocation of bandwidth from the legacy device to its clients.

### Legacy

![legacy-9c9s]

### Mainline

![mainline-9c9s]


[legacy-7c7s]: legacy_and_mainline_images/pilot1-test_inventories_7c7s-480p-@20ft-pilot1-legacy-1708162135.png
[legacy-8c8s]: legacy_and_mainline_images/pilot1-test_inventories_8c8s-480p-@20ft-pilot1-legacy-1708162135.png
[legacy-9c9s]: legacy_and_mainline_images/pilot1-test_inventories_9c9s-480p-@20ft-pilot1-legacy-1708162135.png
[mainline-7c7s]: legacy_and_mainline_images/pilot2-test_inventories_7c7s-480p-@20ft-pilot1-legacy-1708162135.png
[mainline-8c8s]: legacy_and_mainline_images/pilot2-test_inventories_8c8s-480p-@20ft-pilot1-legacy-1708162135.png
[mainline-9c9s]: legacy_and_mainline_images/pilot2-test_inventories_9c9s-480p-@20ft-pilot1-legacy-1708162135.png
