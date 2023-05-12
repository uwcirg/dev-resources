#!/usr/bin/env python3
import click
import jwt
import os
import re

usage = """Generates JWT from PGRST_JWT_SECRET

Given PGRST_JWT_SECRET value, or path to file containing (i.e. logs.env)
construct a log server compliant JWT and echo in format ready for
client configuration file.
"""


def search(pattern, openfile):
    for line in openfile:
        found = re.search(pattern, line)
        if found:
            return found.groups()


def lookup_secret(key, filename):
    with open(filename, 'r') as f:
        key, val = search("^(PGRST_JWT_SECRET)=(.*)", f)
    return key, val


def construct_jwt(secret):
    """Build JWT as needed for logserver write access"""
    return jwt.encode({"role": "event_logger"}, secret, algorithm='HS256')


@click.command(help=usage)
@click.argument('input')
def generate_jwt(input):
    if os.path.exists(input):
        key, logs_secret = lookup_secret("PGRST_JWT_SECRET", input)
    else:
        logs_secret = input
    token = construct_jwt(logs_secret)
    print(f"LOGSERVER_TOKEN={token}")
    return


if __name__ == '__main__':
    generate_jwt()
