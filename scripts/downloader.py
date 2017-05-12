#!/usr/bin/env python3

import argparse
from collections import Counter, OrderedDict
import logging
import pathlib
import time
from subprocess import Popen, PIPE
import sys

LOGGER = logging.getLogger("downloader")


# class OrderedCounter(Counter, OrderedDict):
class OrderedCounter(OrderedDict, Counter):
    "Counter that remembers the order elements are first encountered"

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)


class Downloader(object):
    def __init__(self, url, rate_bps):
        self.first_timestamp = int(time.time())
        self.last_timestamp = int(time.time())
        self.url = url
        self.rate_bps = rate_bps
        self.recvd_bytes_at_timestamp = OrderedCounter()
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
            LOGGER.info("%s - Received bytes: %s",
                        self.last_timestamp,
                        self.recvd_bytes_at_timestamp[self.last_timestamp])
        newly_read = self.downloading_proc.stdout.read(1024)
        self.recvd_bytes_at_timestamp[now_secs] += len(newly_read)
        self.last_timestamp = now_secs

    def run(self):
        while self.downloading_proc.returncode is None:
            self.service_once()

    def report(self, stats_fd):
        if self.recvd_bytes_at_timestamp[self.last_timestamp] == 0:
            # It was a zero-byte read at the end... discard
            del self.recvd_bytes_at_timestamp[self.last_timestamp]
            self.last_timestamp -= 1

        # Even if we We always have at least 1 second
        elapsed_secs = 1 + self.last_timestamp - self.first_timestamp
        recvd_bytes_total = sum(
            self.recvd_bytes_at_timestamp.values())
        LOGGER.info("Received %s bytes in %s secs at %s bytes per sec",
                    recvd_bytes_total,
                    elapsed_secs,
                    int(recvd_bytes_total/elapsed_secs))
        for timestamp, byte_count in self.recvd_bytes_at_timestamp.items():
            stats_fd.write("{0:d},{1:d}\n".format(timestamp, byte_count))


def main():
    parser = argparse.ArgumentParser()
    # 250000 bytes/sec = 2Mbit/sec = max 480p
    parser.add_argument(
        "-b", "--bps",
        type=int,
        default=250000,
        help="the speed of the connection bytes per sec (default: 250000)")
    parser.add_argument(
        "-o", "--output-file",
        help="the destination file for test measurements")
    parser.add_argument(
        "-s", "--sleep",
        type=int,
        default=0,
        help="the number of seconds to sleep before starting the test")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true"
    )
    parser.add_argument(
        "url",
        help="the url to download")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    if args.sleep:
        LOGGER.debug("Sleeping for %s seconds before starting test",
                     args.sleep)
        time.sleep(args.sleep)
    else:
        LOGGER.debug("Starting test immediately (no sleeping)")

    if args.output_file:
        stats_fd = open(pathlib.Path(args.output_file), "w")
    else:
        stats_fd = sys.stdout

    dler = Downloader(args.url, args.bps)
    dler.run()
    dler.report(stats_fd)


if __name__ == "__main__":
    main()
