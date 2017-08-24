# Aim

To compare device throughput when the high-throughput capabilities (ht_capab) of the rt5372 wifi chipset are activated in hostapd.

See the [reference](reference.md) for info on test methodology and advice when reading the graphs.

# Summary

Activating the high-throughput capabilities (ht_capab) of the rt5372 wifi chipset permits more simultaneous clients to be served at full-speed.

# Background

The two devices, Pilot1 and Pilot2 are 25-unit pilot devices (256mb NEO + HAT + unbranded RT5372).

Both devices are running with a 20170809 mainline build. In the first set of experiments, Pilot2 is running with rt5372 high-throughput capabilities while Pilot1 has an unmodified build. In the second set of experiments, Pilot1 is running with rt5372 high-throughput capabilities and Pilot2 has an unmodified build.

For these tests the ConnectBox devices were placed at a distance of 20ft from the clients, with a clear line-of-site. The ConnectBox devices were 3ft off the ground, on a wooden shelf.

# Test Results

Each client is attempting to stream at 480p. Because the results are close, we switch the hardware to make sure the results are consistent

## Experiment 1: 10 Clients

Both devices can serve data at full speed to the clients.

### Pilot 1 (default config)

![pilot1-default-10c10s]

### Pilot 2 (ht_capab active)

![pilot2-htcapab-10c10s]

## Experiment 1: 12 Clients

Pilot2, with high-thoughput capabilities active, outperforms Pilot1

### Pilot 1 (default config)

![pilot1-default-12c12s]

### Pilot 2 (ht_capab active)

![pilot2-htcapab-12c12s]

## Experiment 2: 12 Clients

Both devices can serve data at full speed to the clients.

### Pilot 1 (ht_capab active)

![pilot1-htcapab-12c12s]

### Pilot 2 (default config)

![pilot2-default-12c12s]

## Experiment 2: 13 Clients

Pilot1, with high-throughput capabilities active, outperforms Pilot2

### Pilot 1 (ht_capab active)

![pilot1-htcapab-13c13s]

### Pilot 2 (default config)

![pilot2-default-13c13s]

## Experiment 2: 14 Clients

Neither device can serve data at full speed to the clients, though Pilot1 with high throughput capabilities active, is still able to serve 75% of clients at full speed where as Pilot2 shows more dramatic degradation.

### Pilot 1 (ht_capab active)

![pilot1-htcapab-14c14s]

### Pilot 2 (default config)

![pilot2-default-14c14s]


[pilot1-default-10c10s]: htcapab_images/pilot1-test_inventories_10c10s-480p-@20ft-pilot2-htcapab-1708171941.png
[pilot1-default-12c12s]: htcapab_images/pilot1-test_inventories_12c12s-480p-@20ft-pilot2-htcapab-1708171941.png
[pilot2-htcapab-10c10s]: htcapab_images/pilot2-test_inventories_10c10s-480p-@20ft-pilot2-htcapab-1708171941.png
[pilot2-htcapab-12c12s]: htcapab_images/pilot2-test_inventories_12c12s-480p-@20ft-pilot2-htcapab-1708171941.png
[pilot1-htcapab-12c12s]: htcapab_images/pilot1-test_inventories_12c12s-480p-@20ft-pilot1-capab-1708240542.png
[pilot1-htcapab-13c13s]: htcapab_images/pilot1-test_inventories_13c13s-480p-@20ft-pilot1-capab-1708240542.png
[pilot1-htcapab-14c14s]: htcapab_images/pilot1-test_inventories_14c14s-480p-@20ft-pilot1-capab-1708240542.png
[pilot2-default-12c12s]: htcapab_images/pilot2-test_inventories_12c12s-480p-@20ft-pilot1-capab-1708240542.png
[pilot2-default-13c13s]: htcapab_images/pilot2-test_inventories_13c13s-480p-@20ft-pilot1-capab-1708240542.png
[pilot2-default-14c14s]: htcapab_images/pilot2-test_inventories_14c14s-480p-@20ft-pilot1-capab-1708240542.png
