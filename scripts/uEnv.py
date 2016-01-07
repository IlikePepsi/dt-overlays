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


def assemble_string(l, d, s):
    ret = ""
    if s:
        l.sort()
    for t in l:
        if t is not '':
            ret = ret + t + d
    return ret.rstrip(d)


def list_append(l, a):
    for arg in a.split(','):
        if arg not in l:
            l.append(arg)


def list_remove(l, r):
    for arg in r.split(','):
        if arg in l:
            l.remove(arg)


def main():
    # Read all lines from file
    lines = deserialize(args.file)
    lcount = 0
    default = True

    # Select rootkey or a subkey for further operation
    if args.select:
        for line in lines:
            # Get all whitespace separated words within the current line
            words = line.split()
            # Enumerate the words and find indices matching the pattern given by 'args.select'
            indices = [i for i, s in enumerate(words) if args.select in s]
            # If at least one matching index was found
            if len(indices) > 0:
                # We selected the rootkey and may append or remove values
                if 0 in indices:
                    # We want to append args.append if it is not present
                    if args.append:
                        list_append(words, args.append)
                    # We want to remove args.remove if it is present
                    if args.remove:
                        list_remove(words, args.remove)
                # We selected a subkey and may append or remove values
                else:
                    # Iterate over matched indices
                    for i in indices:
                        # Index contains assignment -> We found a subkey
                        values = words[i].split('=', 1)
                        # Split value string at the given separator
                        if values[1] is not '':
                            tmp = values[1].split(',')
                        else:
                            tmp = []
                        # Append to the list of values if args.append is not in it
                        if args.append:
                            list_append(tmp, args.append)
                            # Reassemble the value string
                            values[1] = assemble_string(tmp, ',', True)
                        # Remove from the list of values if args.append is in it
                        if args.remove:
                            list_remove(tmp, args.remove)
                            # Reassemble the value string
                            values[1] = assemble_string(tmp, ',', True)
                        # Assign new string to list element
                        words[i] = values[0] + '=' + values[1]
                slist = words[words.index('=') + 1:]
                slist.sort()
                ret = words[0:words.index('=') + 1] + slist
                i = lines.index(line)
                # Assemble the whole line from all elements in 'words'
                lines[i] = assemble_string(ret, ' ', False) + '\n'
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