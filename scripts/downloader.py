#!/usr/bin/env python3

import argparse
from collections import Counter, OrderedDict
import logging
import math
import pathlib
import time
import socket
import sys
import random
import urllib.request
import unittest

# 1GB/sec
UNLIMITED_SPEED = 1000000000
#
TIMESLICE_SECS = 0.01
BYTES_TO_READ = 1024

LOGGER = logging.getLogger("downloader")


class TokenBucket(object):
    """Derived from Alec Thomas' ActiveState Code Recipe

    https://code.activestate.com/recipes/511490-implementation-of-the-token-bucket-algorithm/
    """
    def __init__(self,
                 capacity,
                 initial_tokens,
                 refill_amount_per_interval,
                 refill_interval_secs):
        # Initial token count == capacity, for arguments sake
        self.capacity = int(capacity)
        self.initial_tokens = initial_tokens
        self._tokens = max(self.capacity, float(initial_tokens))
        self.refill_amount_per_interval = float(refill_amount_per_interval)
        self.refill_interval_secs = float(refill_interval_secs)
        self.last_refill_time = time.time()

    def reset(self):
        self._tokens = self.initial_tokens
        self.last_refill_time = time.time()

    def consume(self, tokens_requested):
        # Can only consume whole numbers of tokens
        assert isinstance(tokens_requested, int)
        # Can only offer whole numbers of tokens
        available_tokens = math.floor(self.available_tokens())
        if tokens_requested > available_tokens:
            self._tokens -= available_tokens
            return available_tokens

        self._tokens -= tokens_requested
        return tokens_requested

    def available_tokens(self):
        if self._tokens < self.capacity:
            now = time.time()
            if (now - self.last_refill_time) >= self.refill_interval_secs:
                # Only do refills until we hit a complete refill period
                elapsed_interval_count = \
                    (now - self.last_refill_time) / self.refill_interval_secs
                new_tokens = \
                    self.refill_amount_per_interval * elapsed_interval_count
                # print("ROPI", self.refill_amount_per_interval, "eic",
                #      elapsed_interval_count, "New tokens: ", new_tokens)
                self._tokens = min(self.capacity, self._tokens + new_tokens)
                # print("Tokens now:", self._tokens)
                self.last_refill_time = now

        return self._tokens


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
        # bucket is refilled every TIMESLICE_SECS with the
        #  data rate at rate/sec * 1/TIMESLICE_SECS
        self.download_quota = TokenBucket(
            self.rate_bps, 0, self.rate_bps * TIMESLICE_SECS, TIMESLICE_SECS)
        self.test_identifier = "{0}_{1}".format(socket.getfqdn(),
                                                random.randint(0, pow(2, 24)))
        # Populated in run()
        self.remote_site = None

    def service_once(self):
        now_secs = int(time.time())
        if now_secs > self.last_timestamp:
            LOGGER.info("%s - %s received bytes: %s",
                        self.last_timestamp,
                        self.test_identifier,
                        self.recvd_bytes_at_timestamp[self.last_timestamp])
        max_bytes_to_read = self.download_quota.consume(BYTES_TO_READ)
        if max_bytes_to_read > 0:
            newly_read = self.remote_site.read(max_bytes_to_read)
            self.recvd_bytes_at_timestamp[now_secs] += len(newly_read)
            self.last_timestamp = now_secs
            return len(newly_read)

        return 0

    def run(self):
        self.remote_site = urllib.request.urlopen(self.url)
        # Reset the counter when the URL has actually been opened otherwise
        #  we accrue tokens while the connection is being established
        self.download_quota.reset()

        # XXX what happens if this is over a slow link?
        while self.remote_site.length > 0:
            bytes_read = self.service_once()
            if bytes_read == 0:
                time.sleep(TIMESLICE_SECS)

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
        "-d", "--output-file-dir",
        default="/tmp",
        help="the base directory used for storage of test measurements. "
             "- implies no storage and print results to stdout. "
             "(default: /tmp)")
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
    if args.output_file_dir == "-":
        stats_fd = sys.stdout
    else:
        output_path = pathlib.Path(args.output_file_dir,
                                   "{0}.csv".format(dler.test_identifier))
        stats_fd = open(str(output_path), "w")

    dler.report(stats_fd)


class TokenBucketTestCase(unittest.TestCase):
    def testDryBucket(self):
        tb = TokenBucket(0, 0, 0, 0)
        tokens = tb.consume(0)
        self.assertEqual(tokens, 0)
        # Wait, to demonstrate it doesn't refill
        time.sleep(1)
        tokens = tb.consume(0)
        self.assertEqual(tokens, 0)

    def testZeroCapacityBucket(self):
        tb = TokenBucket(0, 0, 1, 1)
        tokens = tb.consume(1)
        self.assertEqual(tokens, 0)
        # Wait, to demonstrate it doesn't refill
        time.sleep(1)
        tokens = tb.consume(0)
        self.assertEqual(tokens, 0)

    def testIntegerRefill(self):
        one_per_sec = TokenBucket(1, 1, 1, 1)
        tokens = one_per_sec.consume(1)
        self.assertEqual(tokens, 1)
        # refill (1 token per second)
        time.sleep(1)
        tokens = one_per_sec.consume(1)
        self.assertEqual(tokens, 1)

    def testFulfilPartialRequest(self):
        one_per_sec = TokenBucket(1, 1, 1, 1)
        tokens = one_per_sec.consume(2)
        self.assertEqual(tokens, 1)
        # refill (1 token per second)
        time.sleep(1)
        tokens = one_per_sec.consume(2)
        self.assertEqual(tokens, 1)

    def testFloatRefillRate(self):
        half_per_sec = TokenBucket(1, 1, 0.5, 1)
        # Consume initial capacity
        tokens = half_per_sec.consume(1)
        self.assertEqual(tokens, 1)
        # Confirm empty
        tokens = half_per_sec.consume(1)
        self.assertEqual(tokens, 0)
        # wait for a second for a refill
        time.sleep(1)
        tokens = half_per_sec.consume(1)
        # Can only distribute whole numbers of tokens
        self.assertEqual(tokens, 0)
        # Wait for a second so we have an integer number of tokens available
        time.sleep(1)
        tokens = half_per_sec.consume(1)
        self.assertEqual(tokens, 1)

    def testGT1secRefillRate(self):
        two_per_two_secs = TokenBucket(2, 2, 2, 2)
        # Consume initial capacity
        tokens = two_per_two_secs.consume(2)
        self.assertEqual(tokens, 2)
        # Confirm empty
        tokens = two_per_two_secs.consume(1)
        self.assertEqual(tokens, 0)
        # wait for a second
        time.sleep(1)
        # Confirm still empty (2 sec refill period)
        tokens = two_per_two_secs.consume(1)
        self.assertEqual(tokens, 0)
        # wait for a second
        time.sleep(1)
        # Confirm refill
        tokens = two_per_two_secs.consume(2)
        self.assertEqual(tokens, 2)


if __name__ == "__main__":
    main()
