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
        try:
            result.remove('\n')
        except ValueError:
            pass
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


def append_to_list(l, a):
    for arg in a.split(','):
        s = search_list(l, arg)
        if len(s) is 0:
            l.append(arg)
        else:
            continue


def remove_from_list(l, r):
    for arg in r.split(','):
        s = search_list(l, arg)
        if len (s) is not 0:
            for i in s:
                l.remove(l[i])
        else:
            continue


def search_list(l, s):
    return [i for i, v in enumerate(l) if v.find(s) is not -1]


def split_line(l):
    tmp = l.split('=', 1)
    return [tmp[0].strip()] + [w.strip('= ') for w in tmp[1].split()]


def main():
    # Read all lines from file
    lines = deserialize(args.file)
    lcount = 0
    default = True

    # Select rootkey or a subkey for further operation
    if args.select:
        for line in lines:
            # Handle empty lines
            if line == '\n':
                lcount = lcount + 1
                continue
            # Get all whitespace separated words within the current line
            words = split_line(line)
            # Enumerate the words and find indices matching the pattern given by 'args.select'
            indices = search_list(words, args.select)
            # If at least one matching index was found
            if len(indices) > 0:
                # Iterate over matched indices
                for i in indices:
                    key = words[i].split('=', 1)
                    if key[0] is words[0]:
                        if args.append: # Assign new value/subkey to rootkey
                            append_to_list(words, args.append)
                        if args.remove:
                            remove_from_list(words, args.remove)
                    else:
                        # There were no values assigned before so we create an empty value list
                        if len(key) is 1:
                            key.append('')
                            tmp = []
                        # We already have some values and must handle different cases
                        else:
                            if len(key) is 2:
                                tmp = key[1].split(',')
                            if tmp[0] is '': # Happens when the subkey in line is 'subkey='
                                tmp = []
                        # Append to the list of values if args.append is not in it
                        if args.append:
                            append_to_list(tmp, args.append)
                            # Reassemble the value string
                            key[1] = assemble_string(tmp, ',', True)
                        # Remove from the list of values if args.append is in it
                        if args.remove:
                            remove_from_list(tmp, args.remove)
                            # Reassemble the value string
                            key[1] = assemble_string(tmp, ',', True)
                        # Assign new string to list element
                        words[i] = key[0] + '=' + key[1]
                        words[i] = words[i].rstrip('= ')
                slist = words[1:]
                slist.sort()
                ret = words[0:1] + ['='] + slist
                i = lines.index(line)
                # Assemble the whole line from all elements in 'words'
                lines[i] = assemble_string(ret, ' ', False) + '\n'
                print(lines[i].strip())
                default = False
            else:
                lcount = lcount + 1

        if len(lines) is lcount:
            sys.exit("key '{0}' not found in {1}".format(args.select, args.file))
            return

    if args.append and default:
        doublet = False
        for line in lines:
            if args.append in line:
                doublet = True
        if not doublet:
            lines.append(args.append)

    if args.remove and default:
        for line in lines:
            if args.remove in line:
                lines.remove(line)

    serialize(lines)

    if default:
        for line in lines:
            print(line.strip())


if __name__ == '__main__':
    main()