#!/usr/bin/env python3
import click
import re
import sys
import uuid

usage = """Echos all lines from input file to stdout or output file,
appending unique generated secrets when expected patterns are found"""


def match(line):
    """Returns true if line matches configured patterns"""
    m = re.search("^__KEYCLOAK_.*_SECRET=", line)
    return m


def single_line(line):
    """Given single line of input, return possibly improved output"""
    if not match(line):
        return line
    return improve(line)


def improve(line):
    # chop newline, improve, and add back on
    return f"{line.rstrip()}{uuid.uuid4()}\n"


@click.command(help=usage)
@click.argument('input')
@click.option('-o', '--output', help="writable file, stdout by default")
def generate_secrets(input, output):
    if not output:
        ofile = sys.stdout
    else:
        ofile = open(output, 'w')

    with open(input, 'r') as ifile:
        for line in ifile:
            if not match(line):
                ofile.write(line)
            else:
                ofile.write(improve(line))


if __name__ == '__main__':
    generate_secrets()
