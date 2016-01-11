#!/usr/bin/python
__author__ = "archuser"

import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to operate on")
parser.add_argument("name", help="name of the device-tree overlay")
parser.add_argument("--slot", help="return the slotnumber where the overlay was loaded")

args = parser.parse_args()


def open_file(filename):
    if not os.path.exists(filename):
        sys.exit("Could not open file! Path doesn't exist.")
        return
    with open(filename, mode='r') as f:
        return f.readlines()


def main():
    lines = open_file(args.file)
    indices = [i for i, s in enumerate(lines) if s.find(args.name) is not -1]
    if len(indices) > 0:
        for i in indices:
            if args.slot:
                print(lines[i].strip()[0:lines[i].find(':')]) # First character of the matching line == slotnumber
            else:
                print(lines[i].strip())
    else:
        sys.exit("Could not find device-tree overlay!")
    return


if __name__ == '__main__':
    main()