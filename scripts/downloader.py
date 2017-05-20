#!/usr/bin/env python3

import argparse
from collections import Counter, OrderedDict
import logging
import pathlib
import time
import socket
from subprocess import Popen, PIPE
import sys

UNLIMITED_SPEED = -1

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
        # Populated during run()
        self.downloading_proc = None
        # Populated during run()
        self.test_identifier = None

    def get_cmd(self):
        cmd = ["wget",
               "--quiet",
               "--output-document=-",
               self.url]

        if self.rate_bps != UNLIMITED_SPEED:
            # Insert as the first argument (right after the command)
            cmd.insert(1, "--limit-rate={0:d}".format(self.rate_bps))

        return cmd

    def service_once(self):
        now_secs = int(time.time())
        if now_secs > self.last_timestamp:
            self.downloading_proc.poll()
            LOGGER.info("%s - %s received bytes: %s",
                        self.last_timestamp,
                        self.test_identifier,
                        self.recvd_bytes_at_timestamp[self.last_timestamp])
        newly_read = self.downloading_proc.stdout.read(1024)
        self.recvd_bytes_at_timestamp[now_secs] += len(newly_read)
        self.last_timestamp = now_secs

    def run(self):
        self.downloading_proc = Popen(self.get_cmd(), stdout=PIPE, bufsize=0)
        LOGGER.debug("Process running with PID: %s", self.downloading_proc.pid)
        self.test_identifier = "{0}_{1}".format(socket.getfqdn(),
                                                self.downloading_proc.pid)

        while self.downloading_proc.returncode is None:
            self.service_once()

    def report(self, stats_fd):
        LOGGER.debug("Writing stats to %s", stats_fd.name)
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
        stats_fd.write("#client_test_id,timestamp,bytes_per_sec\n")
        for timestamp, byte_count in self.recvd_bytes_at_timestamp.items():
            stats_fd.write("{0},{1:d},{2:d}\n".format(
                self.test_identifier,
                timestamp,
                byte_count))


def main():
    parser = argparse.ArgumentParser()
    # 250000 bytes/sec = 2Mbit/sec = max 480p
    parser.add_argument(
        "-b", "--bps",
        type=int,
        default=UNLIMITED_SPEED,
        help="the speed of the connection bytes per sec (default: unlimited)")
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

    dler = Downloader(args.url, args.bps)
    dler.run()

    # The default output file requires the test id, which is only available
    #  once the test has run, so we process these arguments late.
    if args.output_file:
        if args.output_file == "-":
            stats_fd = sys.stdout
        else:
            output_path = pathlib.Path(args.output_file)
            stats_fd = open(str(output_path), "w")
    else:
        output_path = pathlib.Path("{0}.csv".format(dler.test_identifier))
        stats_fd = open(str(output_path), "w")

    dler.report(stats_fd)


if __name__ == "__main__":
    main()
