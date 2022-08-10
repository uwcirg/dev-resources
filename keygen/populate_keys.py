#!/usr/bin/env python3
import click
import re
import sys
import uuid

usage = """Echos all lines from input file to stdout or output file,
appending unique generated secrets when expected patterns are found"""


def match(line, ignore_existing):
    """Returns true if line matches configured patterns"""
    m = re.search("^(__KEYCLOAK_.*_SECRET=)(.*)", line)
    if not m:
        return False

    key, value = m.groups()
    if not ignore_existing:
        # when retaining existing values, don't consider a match if
        # existing value exists
        if value:
            return False

    # return only the first group for overwrite, extension
    return m and m.groups()[0]


def single_line(line, replace):
    """Given single line of input, return possibly improved output"""
    m = match(line, ignore_existing=replace)
    if not m:
        return line
    return improve(m)


def improve(line):
    # chop newline, improve, and add back on
    return f"{line.rstrip()}{uuid.uuid4()}\n"


@click.command(help=usage)
@click.argument('input')
@click.option('-o', '--output', help="writable file, stdout by default")
@click.option('-r', '--replace', default=False, help="replace existing values")
def generate_secrets(input, output, replace):
    if not output:
        ofile = sys.stdout
    else:
        ofile = open(output, 'w')

    with open(input, 'r') as ifile:
        for line in ifile:
            ofile.write(single_line(line, replace))


if __name__ == '__main__':
    generate_secrets()
