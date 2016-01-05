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


def parse_recursive(line):
    l = []
    # Assuming 'line' contains whitespace separated values we split'em up
    for arg in line.split():
        # Are there still assignments in 'value'?
        if '=' in arg:
            # Yes there are
            # Split 'arg' at the assignment operators position
            keys = arg.split("=", 1)
            # Does the resulting list contain at least 2 elements?
            if len(keys) < 2:
                # No it doesn't, so append key[0] with an empty value list
                l.append([keys[0].strip(), []])
                continue
            else:
                # Yes it does, so append a key[0] and parse key[1] for further assignments
                l.append([keys[0].strip(), parse_recursive(keys[1])])
                continue
        else:
            # No there are not. So we assume there are only comma separated values left in 'value'
            value = arg.strip()
            l.append(value.split(','))
            continue

    return l


def deserialize_recursive(filename):
    with open(args.file, mode='r') as f:
        l = []
        # Read all lines in given file and create list of lists (of lists) for each line
        for line in f.readlines():
            if '=' in line:
                rootkey = line.split('=',1)
                if len(rootkey) < 2:
                    l.append([rootkey[0].strip(), []])
                else:
                    l.append([rootkey[0].strip(), parse_recursive(rootkey[1])])

        # Make dictionary from List

    return l


def deserialize(filename):
    if not os.path.exists(filename):
        return {}
    with open(args.file, mode='r') as f:
        d = {}
        for line in f.readlines():
            values = line.split("=", 1)
            if len(values) < 2:
                continue
            d[values[0].strip()] = values[1].strip()

    return d


def serialize(d):
    result = []
    for key, value in d.items():
        result.append(key + " = " + value + "\n")

    with open(args.file, mode='w') as f:
        result.sort()
        f.writelines(result)


def main():
    maintain_default = True

    d = dict(deserialize_recursive(args.file))

    if args.select:
        maintain_default = False

        args.select = args.select.split(',')

        if args.append:
            d[args.select[0]] = d[args.select] + " " + args.append.strip()

        if args.remove:
            d[args.select] = d[args.select].replace(args.remove, "").strip()

        if args.select[0] in d:
            pp(d[args.select[0]])
            return
        else:
            sys.exit("key '{0}' not found in {1}".format(args.select[0], args.file))
            return

    elif args.append:
        result = args.append.split("=", 1)
        d[result[0]] = result[1]

    elif args.remove:
        d.pop(args.remove)

    else:
        # pretty print the dict
        pp(d)
        return

    serialize(d)

if __name__ == '__main__':
    main()
