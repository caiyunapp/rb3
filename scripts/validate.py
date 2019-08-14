"""Script to validate rb3.

Make sure Python3's rb3 could work with Python2' rb,
with zlib's compress/decompress and UTF-8 encoding/decoding.

rb:  getsentry's repo, https://github.com/getsentry/rb
rb3: caiyunapp's fork, https://github.com/caiyunapp/rb3

Usage:

    pip2 install fire, rb
    pip3 install fire, rb3

    # Python3 save and Python2 read
    python3 validate.py --action=set;python2 validate.py --action=get

    # Python2 save and Python3 read
    python2 validate.py --action=set;python3 validate.py --action=get


Author: ringsaturn
Email: <ringsaturn.me@gmail.com>
GitHub: https://github.com/ringsaturn

Create: 2019-08-14
"""

from __future__ import print_function

import json
import zlib

import fire
from rb import Cluster

cluster = Cluster({
    0: {'port': 6379},
    # 1: {'port': 6380},
    # 2: {'port': 6381},
    # 3: {'port': 6382},
}, host_defaults={
    'host': '127.0.0.1',
}, pool_options={"decode_responses": False})

cache_client = cluster.get_routing_client()


def single_set(k, v):
    cache_client.set(k, v)


def single_get(k):
    return cache_client.get(k)


def do_set(data):
    for k in data.keys():
        expect_value = json.dumps(data[k])
        saved_value = zlib.compress(expect_value.encode('utf-8'))
        single_set(k, saved_value)


def do_get(data):
    for k in data.keys():
        expect_value = json.dumps(data[k])
        saved_value = single_get(k)
        if zlib.decompress(saved_value).decode('utf-8') == expect_value:
            pass
        else:
            print("error", k, expect_value, zlib.decompress(
                saved_value).decode('utf-8'))


def main(action=None):
    data = {
        "fds": {"1": 432, "432": 3216},
        "321432": {"21": "463728"}
    }
    if action == 'get':
        do_get(data)
    elif action == 'set':
        do_set(data)
    else:
        print("invalid action")


if __name__ == "__main__":
    fire.Fire(main)
