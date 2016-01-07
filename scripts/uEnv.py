#!/usr/bin/python
__author__ = "archuser"

import argparse
import sys
import os

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


def serialize(result):
    with open(args.file, mode='w') as f:
        result.sort()
        f.writelines(result)

def assemble_string(l, d):
    ret = ""
    for t in l:
        if t is not '':
            ret = ret + t + d
    return ret.rstrip(d)


def main():
    # Read all lines from file
    lines = deserialize(args.file)
    lcount = 0
    default = True

    if args.select:
        for line in lines:
            # Get all whitespace separated words within the current line
            words = line.split()
            # Enumerate the words and find indices matching the pattern given by 'args.select'
            indices = [i for i, s in enumerate(words) if args.select in s]
            # If at least one matching index was found
            if len(indices) > 0:
                # Look for assignment operator (indicating a list on right side of assignment
                for i in indices:
                    values = words[i].split('=', 1)
                    if len(values) < 2:
                        continue
                    else:
                        tmp = values[1].split(',')
                        assert isinstance(tmp, list)
                        if args.append:
                            if args.append not in tmp:
                                tmp.append(args.append)
                            values[1] = assemble_string(tmp, ',')
                        if args.remove:
                            if args.remove in tmp:
                                tmp.remove(args.remove)
                            values[1] = assemble_string(tmp, ',')
                        words[i] = values[0] + '=' + values[1]
                i = lines.index(line)
                lines[i] = assemble_string(words, ' ') + '\n'
                print(lines[i])
                default = False
            else:
                lcount = lcount + 1

        if len(lines) is lcount:
            sys.exit("key '{0}' not found in {1}".format(args.select, args.file))
            return

    if args.append:
        doublet = False
        for line in lines:
            if args.append in line:
                doublet = True
        if not doublet:
            lines.append(args.append)

    if args.remove:
        for line in lines:
            if args.remove in line:
                lines.remove(line)

    serialize(lines)

    if default:
        for line in lines:
            print(line.strip())


if __name__ == '__main__':
    main()