#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
ref_list = {}

# input comes from STDIN
#f = open('test.txt')
#for line in f:
for line in sys.stdin:

    # remove leading and trailing whitespace
    line = line.strip()
    if line.strip() == '':
        continue

    # parse the input we got from mapper.py
    word, count, url, index = line.split('\t', 3)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # convert index (currently a string) to int
    try:
        index = int(index)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
        ref_list[index] = count
    else:
        if current_word:
            # write result to STDOUT
            printLine = '%s\t%s\t' % (current_word, current_count)
            for i in ref_list:
                printLine += "(%s\t%s)\t" % (i, ref_list[i])
            print printLine
        current_count = count
        current_word = word
        ref_list = {}
        ref_list[index] = count

# do not forget to output the last word if needed!
if current_word == word:
    printLine = '%s\t%s\t' % (current_word, current_count)
    for i in ref_list:
        printLine += "(%s\t%s)\t" % (i, ref_list[i])
    print printLine
