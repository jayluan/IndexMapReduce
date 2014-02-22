#!/usr/bin/env python
"""
    reducer_pt2.py
    purpose: takes pipe from reducer and computes the TF-IDF index
    the layout of the input is as follows:

    (word) (total_freq) (#of_documents) (doc#1) (#words_total) (freq) (pos1) (pos2) (pos3) ... (doc#2) (#words_total) (freq) (pos1) (pos2) ...

    the output is:
   (word) (total_freq) (#of_documents) (doc#1) (TFIDF) (#words_total) (freq) (pos1) (pos2) (pos3) ... (doc#2) (TFIDF) (#words_total) (freq) (pos1) (pos2) ...
"""

import sys
import math
import re

stored_data = []
stored_doc_count_word = {}    # number of documents with a given word
#f = open('../reduced.txt')
#for line in f:
for line in sys.stdin:
    #count the number of lines and get # of docs w/ the term in it
    line = line.strip()
    if line.strip() == '':
        continue

    # parse the input we got from mapper.py and store it
    entry = line.split('\t')
    stored_data.append(entry)

#loop through all the stored input data
regex = re.compile(r'[\W_]+')
for entry in stored_data:
    tfidf = {}
    word = entry[0]
    if bool(regex.match(word)):     # Skip non-alpha numeric stuff
            continue
    count = entry[1]
    numDocs = entry[2]    # number of documents with this word in it
    i = 3

    #loop through the rest of the doc and compute all the TFIDF's
    while i < len(entry):
        doc = entry[i]
        i += 1
        totalWords = entry[i]
        tfidf_index = i    # we want to store tfidf right bdeefore frequency, so we keep track of the index of that position
        i += 1
        freq = entry[i]
        i += int(freq)+1

        #calculate tfidf for the current word for this specific document
        tf = float(freq)/float(totalWords)
        idf = math.log(float(len(stored_data))/float(numDocs))
        tfidf[tfidf_index] = tf*idf

    #insert tfidf values into the entry
    offset = 0
    for i in sorted(tfidf.iterkeys()):
        entry.insert(i + offset, str(tfidf[i]))
        offset += 1
    #print the line
    print "\t".join(entry)
