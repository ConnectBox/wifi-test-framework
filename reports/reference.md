# Methodology

Tests are interleaved and run multiple times in succession.

e.g. a typical test scenario comparing device A against device B will run the test suite 20 times, ABABAB etc . This means that we increase the chance that localised changes to the test environment are reflected equally for both devices.

The test involves clients downloading a 10MB file of completely random data from the ConnectBox webserver with the ConnectBox at a fixed distance from the clients. The test will be specifically crafted as line-of-site or with certain obstacles.

# Throughput testing

Fixed-rate throughput tests are performed by the clients self-throttling to the required download rate. In practice, iOS and Android devices do not constantly download at a fixed rate but instead perform burst downloads (followed by periods of download inactivity). iOS downloads more aggressively than Android. The tests do not attempt to reproduce this behaviour. The tests are still useful in determining the maximum number of devices at a required download rate because as the device gets closer to its maximum throughput, the client devices will be able to burst less, and so converge on a behaviour resembling downloading at a fixed rate.

# Converting bitrates to video resolution

Using [YouTube's live encoder bitrates](https://support.google.com/youtube/answer/2853702?hl=en) we refer to the following bitrates and resolutions:

* 360p: 125000 bytes/sec
* 480p: 250000 bytes/sec
* 720p: 500000 bytes/sec

We have taken Youtube's maximum values, so often the bitrate will be lower that these figures.

# How To Read The Graphs

![example]

This is a representative graph for these reports. These _box and whisker_ graphs aggregate multiple identical runs (in this example, aggregation of 20 runs) and show the distribution of results at each 1 second period in the test.

* The median of the readings for that 1 second period is marked by a green bar within the _box_
* The lower and upper boundaries of the _box_ represent the 25th and 75th percentile of the readings for the 1 second period, respectively.
* The black bar at the end of the upper whisker marks the 95th percentile data point. Similarly the lower whisker marks the 5th percentile data point.
* Any data points beyond the whiskers are considered outliers and are not shown
* For graphs where the desired bitrate is 360p, 480p or 720p, a horizontal line is shown at this bitrate.

Examples:
* If all the runs had a throughput of 250000 bytes/sec at a particular time, the graph will collapse into a single data-point, as is the case at t=70. (note that some clients may have completed their download by this time, and will not be considered in the aggregate for this time point.
* At t=20, the median (the green mark) is at 250000 bytes/sec and there are no marks above this rate. Assuming all 9 clients are active at this point, this means at least 4 clients are downloading at the attempted speed.
* At t=20, the 25th percentile is at 220000 bytes/sec, so 2 or 3 additional clients are downloading at close to the attempted speed.
* At t=20, the 5th percentile is at 150000 bytes/sec indicating the slowest client is downloading at 150000 bytes/sec.

For 360p and 480p tests, all clients are usually active at t=20, so this time serves as a good single-point summary of performance. The corresponding time for 720p tests is around t=10 to t=15 (a full-speed download of the 10MB sample file completes in 20 seconds at 720p rates, 40 seconds at 480p and 80 seconds at 360p) 

[example]: calibration_images/pilot2_9c9s-480p-@20ft-1708130808.png "Example"
