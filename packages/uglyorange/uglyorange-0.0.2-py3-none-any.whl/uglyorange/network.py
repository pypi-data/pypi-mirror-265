#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
from .utils import get_system_info


class FastPing(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='Ping a host.')
        self.add_argument('host', type=str, help='hostname or IP address')
        self.add_argument('-c', '--count', type=int, default=9,
                          help='number of packets to send')

    @property
    def os(self):
        return get_system_info()['system']

    @property
    def cmd(self):
        args = self.parse_args()
        os_name = self.os.lower()
        if 'darwin' in os_name:
            return "ping -c {} -i 0.1 -W 1 {}".format(args.count, args.host)
        elif 'linux' in os_name:
            return "ping -c {} -4 -i 0.1 -W 1 {}".format(args.count, args.host)

    @staticmethod
    def entrypoint():
        response = os.system(FastPing().cmd)
        return response == 0


class Cufo(object):
    @staticmethod
    def entrypoint():
        return os.system(
            "curl cufo.cc"
        )
