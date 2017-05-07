#!/usr/bin/env python3

import collections
import time
from subprocess import Popen, PIPE


class Downloader(object):
    def __init__(self, url, rate_bps):
        self.first_timestamp = int(time.time())
        self.last_timestamp = int(time.time())
        self.url = url
        self.rate_bps = rate_bps
        self.recvd_bytes_at_timestamp = collections.Counter()
        self.downloading_proc = Popen(self.get_cmd(), stdout=PIPE, bufsize=0)

    def get_cmd(self):
        return ["wget",
                "--quiet",
                "--output-document=-",
                "--limit-rate=%s" % (self.rate_bps,),
                self.url]

    def service_once(self):
        now_secs = int(time.time())
        if now_secs > self.last_timestamp:
            self.downloading_proc.poll()
            print(self.last_timestamp,
                  "Received bytes:",
                  self.recvd_bytes_at_timestamp[self.last_timestamp])
        newly_read = self.downloading_proc.stdout.read(1024)
        self.recvd_bytes_at_timestamp[now_secs] += len(newly_read)
        self.last_timestamp = now_secs

    def run(self):
        while self.downloading_proc.returncode is None:
            self.service_once()

    def report(self):
        elapsed_secs = self.last_timestamp - self.first_timestamp
        recvd_bytes_total = sum(
            self.recvd_bytes_at_timestamp.values())
        print("Received", recvd_bytes_total,
              "bytes in", elapsed_secs, "secs at",
              int(recvd_bytes_total/elapsed_secs),
              "bytes per sec")

# 250000 bytes/sec = 2Mbit/sec = max 480p
d = Downloader("http://connectbox.rpi3/content/10MB.bin", 250000)
# d = Downloader("http://connectbox.rpi3/content/10MB.bin", 2500000)
d.run()
d.report()
