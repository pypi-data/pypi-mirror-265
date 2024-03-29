#!/usr/bin/env python
import os
import sys
import subprocess
import argparse


def fastping() -> bool:
    """Check if a host is reachable.
    Args:
        host (str): hostname or IP address
    """
    parser = argparse.ArgumentParser(description='Ping a host.')
    parser.add_argument('host', type=str, help='hostname or IP address')
    parser.add_argument('-c', '--count', type=int, default=9,
                        help='number of packets to send')
    args = parser.parse_args()
    cmd = "ping -c {} -i 0.1 -W 1 {}".format(args.count, args.host)
    response = os.system(cmd)
    return response == 0
