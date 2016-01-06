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
    """
    This method parses lines of text recursively to return nested lists of the lines content, assuming the text sticks to a specific pattern
    :param line: the input text
    :return: list
    """
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
            value = value.split(',')
            for v in value:
                l.append(v)
            continue

    return l


def deserialize_recursive(filename):
    """ A function to deserialize files containing text recursively

    This method assumes a specific assignment pattern within the file given by ``filename``.
    The pattern reads as follows:
        "Rootkey = value1 value2 child_key1=value3,value4 value5.."
    Text sticking to this pattern will be parsed by ``parse_recursive()`` to generate nested lists as follows:
        [['Rootkey', [['value1'], ['value2'], ['child_key1', ['value3', 'value4']], ['value5'].. ]]]
    :param filename: name of the file to read
    :return: list
    """
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


def is_list(o):
    return isinstance(o, list)


def is_dict(o):
    return isinstance(o, dict)


def list_to_dict(l):
    if len(l) is 2:
        return {l[0]: l[1]}
    else:
        return l


def deep_transform(l):
        d = {}
        for e in l:
            if is_list(e) and len(e) is 2:
                d[e[0]] = deep_transform(e[1])
                return d
            else:
                return [e]


def main():

    default = True

    # Convert the lists of lists object to a dict
    d = dict(deserialize_recursive(args.file))

    for key in d.keys():
        d[key] = [list_to_dict(e) for e in d[key]]

    if args.select:
        default = False
        args.select = args.select.split(',')


        if len(args.select) > 1:
            if args.select[0] in d:
                for e in d[args.select[0]]:
                    if args.select[1] in e:
                        v = d[args.select[0][args.select[1]]]
        # TODO: Implement select behavior if list is passed

        if args.append:
            l = parse_recursive(args.append)
            for e in l:
                d[args.select[0]].append(list_to_dict(e))

        if args.remove:
            l = parse_recursive(args.append)

            d[args.select] = d[args.select].replace(args.remove, "").strip()

        if args.select[0] in d:
            pp(d[args.select[0]])
            return
        else:
            sys.exit("key '{0}' not found in {1}".format(args.select[0], args.file))
            return

    elif args.append:
        l = parse_recursive(args.append)
        v = deep_transform(l)
        d[v.keys()[0]] = v.keys()[0]
        pass

    elif args.remove:
        d.pop(args.remove)

    else:
        # pretty print the dict
        pp(d)
        return

    # serialize(d)

if __name__ == '__main__':
    main()
