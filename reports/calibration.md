# Calibrating devices

See the [reference](reference.md) for info on test methodology and advice when reading the graphs.

## Aim

To gauge the normal variance that we can expect from run to run.

## Background

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


variance between devices

how to test



[p1-8c8s-early]: calibration_images/pilot1_8c8s-480p-@20ft-1708130642.png "Pilot1 8x480p streams @20ft (early test)"
[p2-9c9s-early]: calibration_images/pilot2_9c9s-480p-@20ft-1708130642.png "Pilot1 9x480p streams @20ft (early test)"
[p2-9c9s-late]:  calibration_images/pilot2_9c9s-480p-@20ft-1708130808.png "Pilot1 9x480p streams @20ft (late test)"
