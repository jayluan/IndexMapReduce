#!/usr/bin/env python
'''
    reducer.py
    purpose: does the reduction coming from the mapper
    input:
    (word) (freq) (url) (doc#) (#words_in_doc) (pos1) (pos2) (pos3) ...

    output:
    (word) (freq) (# docs w/ word) (doc#1) (#words_total) (#of_given_word) (pos1) (pos2) (pos3) ... (doc2) (#words_total) (#of_given_word) (pos1) (pos2) ...


'''
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
ref_list = {}
DEBUG = False

# input comes from STDIN
#f = open('../test.txt')
for line in sys.stdin:
#for line in sys.stdin:

    # remove leading and trailing whitespace
    line = line.strip()
    if line.strip() == '':
        continue

    # parse the input we got from mapper.py
    positions = []
    entry = line.split('\t')
    word = entry[0]
    count = entry[1]
    url = entry[2]
    index = entry[3]
    numWords = entry[4]    # total # of words in document
    if len(entry) > 5:
        positions = entry[5:]

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
        ref_list[index] = [count, numWords, positions]
    else:
        if current_word:
            # write result to STDOUT
            printLine = '%s\t%s\t%d\t' % (current_word, current_count, len(ref_list))
            for i in ref_list:
                if DEBUG:
                    printLine += "("
                printLine += "%d\t%s\t%d" % (i, ref_list[i][1], ref_list[i][0])    # Doc_num, numWords, count
                for k in ref_list[i][2]:
                    printLine += "\t%s" % (k)
                if DEBUG:
                    printLine += ")"
                printLine += "\t"
                
            print printLine
        current_count = count
        current_word = word
        ref_list = {}
        ref_list[index] = [count, numWords, positions]

# do not forget to output the last word if needed!
if current_word == word:
    printLine = '%s\t%s\t%d\t' % (current_word, current_count, len(ref_list))
    for i in ref_list:
        if DEBUG:
            printLine += "("
        printLine += "%d\t%s\t%d" % (i, ref_list[i][1], ref_list[i][0])
        for k in ref_list[i][2]:
            printLine += "\t%s" % (k)
        if DEBUG:
            printLine += ")"
        printLine += "\t"
    print printLine
