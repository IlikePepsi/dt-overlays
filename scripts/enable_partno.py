#!/usr/bin/python
__author__ = "archuser"

import argparse
import sys
import os

from pprint import pprint as pp

parser = argparse.ArgumentParser()
parser.add_argument("file", help = "file to operate on")
parser.add_argument("--select", help = "show a keys associated value string (if present)")
parser.add_argument("--append", help = "append input string to value of selected key")
parser.add_argument("--remove", help = "remove input string from value of selected key")

args = parser.parse_args()


def deserialize(filename):
    if not os.path.exists(filename):
        return []
    with open(args.file, mode='r') as f:
        return f.readlines()


def serialize(d):
    result = []
    for key, value in d.items():
        result.append(key + " = " + value + "\n")

    with open(args.file, mode='w') as f:
        result.sort()
        f.writelines(result)


def main():
    for line in deserialize(args.file):
        assert isinstance(line, str)
        l = line.split()
        indices = [i for i, s in enumerate(l) if args.select in s]

        if args.append:
            pass

        if args.remove:
            pass



if __name__ == '__main__':
    main()