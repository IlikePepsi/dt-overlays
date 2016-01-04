#!/usr/bin/python
__author__ = "archuser"

import argparse
import sys

from pprint import pprint as pp

parser = argparse.ArgumentParser()
parser.add_argument("file", help = "file to operate on")
parser.add_argument("--select", help = "show a keys associated value string (if present)")
parser.add_argument("--append", help = "append input string to value of selected key")
parser.add_argument("--remove", help = "remove input string from value of selected key")
parser.add_argument("--add", help = "add a new key/value parameter")

#parser.add_argument("key", help = "the key whose value you want to modify")

args = parser.parse_args()


def parse_recurse(line):
    if '=' in line:
        d = {}
        keys = line.split("=", 1)
        if len(keys) < 2:
            d[keys[0].strip()] = None
            return d
        else:
            d[keys[0].strip()] = parse_recurse(keys[1])
    else:
        line = line.strip()
        return line.split(',')


def deserialize_recurse(filename):
    with open(args.file, mode='r') as f:
        d = {}
        for line in f.readlines():
            d = parse_recurse(line)

    return d


def deserialize(filename):
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

    #with open(args.file, mode='w') as f:
    with open("test.txt", mode='w') as f:
        result.sort()
        f.writelines(result)


def main():
    maintain_default = True

    d = deserialize_recurse(args.file)

    if args.select:
        maintain_default = False

        if args.append:
            d[args.select] = d[args.select] + " " + args.append.strip()

        if args.remove:
            d[args.select] = d[args.select].replace(args.remove, "").strip()

        if args.select in d:
            print("{0} = {1}".format(args.select, d.get(args.select)))
        else:
            sys.exit("key '{0}' not found in {1}".format(args.show, args.file))
            return

    elif args.add:
        result = args.add.split("=", 1)
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
