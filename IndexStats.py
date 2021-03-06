#!/usr/bin/env python
"""
    IndexStats.py
    Purpose: Script to generate stats related to the current index

    input format:
   (word) (total_freq) (#of_documents) (doc#1) (TFIDF) (#words_total) (freq) (pos1) (pos2) (pos3) ... (doc#2) (TFIDF) (#words_total) (freq) (pos1) (pos2) ...
"""

from IndexStruct import Index, Doc
import csv


def LoadIndex(index_fname):
    #load the index first
    word_index = {}
    with open(index_fname, "r") as f:
        reader = csv.reader(f, dialect='excel-tab')
        for line in reader:
            index = Index(line[0], int(line[1]), int(line[2]))
            i = 3
            while i < len(line):
                docId = int(line[i])
                i += 1
                tfidf = float(line[i])
                i += 1
                total_words = int(line[i])
                i += 1
                count = int(line[i])
                i += 1
                doc = Doc(docId, tfidf, total_words, count)

                k = 0
                while k < count:
                    pos = int(line[i])
                    doc.Positions.append(pos)
                    k += 1
                    i += 1

                index.Append(doc)

            if line[0] in word_index:
                for item in index.Docs:
                    word_index[line[0]].Append(item)
            else:
                word_index[line[0]] = index
    return word_index
            

#do stuff with the index
def main():
    fname = '../index.txt'
    return LoadIndex(fname)
