# Calibrating devices

See the [reference](reference.md) for info on test methodology and advice when reading the graphs.

## Aim

To gauge the normal variance that we can expect from run to run.

## Summary

Performance may vary by up to 25% between identical configured devices using interleaved runs.

Performance has been seen to vary by up to 20% between identical runs on the same hardware.

## Background

The two devices, Pilot1 and Pilot2, are 25-unit pilot devices (256mb NEO + HAT + unbranded RT5372) running an unmodified 20170809 Mainline build.

These test results are the last in a series of tests. The two devices have identical hardware and so should have identical performance. To confirm that the results were not as a result of defective componentsor test environment, the following variations were performed, with similar results:

* swapping micro sd cards
* swapping usb wifi
* swapping power cable and supply
* swapping the Neo board + HAT
* removing the USB storage and instead serving the test file from micro sd.
* reversing device test location (placing device 1 where device 2 was, and vice versa)

For these tests the ConnectBox devices were placed at a distance of 20ft from the clients, with a clear line-of-site. The ConnectBox devices were 3ft off the ground, on a wooden shelf.

## Variance on the same device

Two identical tests, made within a few hours of each other, on the same hardware, with the same clients

Early Test (full throughput for all clients for the entirety of the test)

![p2-9c9s-early]

Late Test (full throughput for most clients, with some underperformers, and drop-off in throughput part-way through the test) 

![p2-9c9s-late]

And a subsequent test and repeat with one test showing showing near full throughput for the test, even though the test has 10 clients instead of 9. This also had a spacing of a few hours between runs.

![p2-10c10s-early]

![p2-10c10s-late]

## Variance between identical devices

Identical tests. Pilot1 provides full throughput for all clients for the entirety of the test but Pilot2 can only sustain 75-80% of full throughput.

![p1-10c10s-late]

![p2-10c10s-late]

Pilot2 is clearly slower in this test, despite identical hardware.

![p1-11c11s-late]

![p2-11c11s-late]

In most, but not all cases (including some not captured here) the pilot1 device performs better than pilot2.

[p1-8c8s-early]: calibration_images/pilot1_8c8s-480p-@20ft-1708130642.png "Pilot1 8x480p streams @20ft (early test)"
[p1-10c10s-early]:  calibration_images/pilot1_10c10s-480p-@20ft-1708130642.png "Pilot1 10x480p streams @20ft (early test)"
[p1-10c10s-late]:  calibration_images/pilot1_10c10s-480p-@20ft-1708130808.png "Pilot1 10x480p streams @20ft (late test)"
[p1-11c11s-late]:  calibration_images/pilot1_11c11s-480p-@20ft-1708130808.png "Pilot1 11x480p streams @20ft (late test)"
[p2-9c9s-early]: calibration_images/pilot2_9c9s-480p-@20ft-1708130642.png "Pilot2 9x480p streams @20ft (early test)"
[p2-9c9s-late]:  calibration_images/pilot2_9c9s-480p-@20ft-1708130808.png "Pilot2 9x480p streams @20ft (late test)"
[p2-10c10s-early]: calibration_images/pilot2_10c10s-480p-@20ft-1708130642.png "Pilot2 10x480p streams @20ft (early test)"
[p2-10c10s-late]:  calibration_images/pilot2_10c10s-480p-@20ft-1708130808.png "Pilot2 10x480p streams @20ft (late test)"
[p2-11c11s-late]:  calibration_images/pilot2_11c11s-480p-@20ft-1708130808.png "Pilot2 11x480p streams @20ft (late test)"
