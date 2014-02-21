#!/usr/bin/env python

import sys
import re

stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours ", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

def find_occurrences(text, word):
    wordOccur = []
    text = text.lower()
    start = text.find(word)
    if start > 0:
        wordOccur.append(start)
    while start >= 0:
        start = text.find(word, start+len(word))
        if start > 0:
            wordOccur.append(start)
    return wordOccur

def find_nth(line, delim, n):
    start = line.find(delim)
    while start >= 0 and n > 1:
        start = line.find(delim, start+len(delim))
        n -= 1
    return start

docNum = 1
# input comes from STDIN (standard input)
for line in sys.stdin:
    urlStart = find_nth(line, 'AFUCKINGDELIMITER', 1) + 17
    urlEnd = find_nth(line, 'AFUCKINGDELIMITER', 2)
    url = line[urlStart:urlEnd]
    startIndex = find_nth(line, 'AFUCKINGDELIMITER', 3) + 19
    endIndex = find_nth(line, 'AFUCKINGDELIMITER', 4) - 3
    plainText = line[startIndex:endIndex]

    plainText.decode("utf-8")

    word_list = re.sub(ur"(?u)\\x[A-Za-z0-9]{0,2}",'' ,plainText)
    word_list = re.sub(ur"(?u)\\t", ' ', word_list)
    word_list = re.sub("\d+", " ", word_list)
    word_list = re.sub("(^| ).( |$)", " ", word_list)
    word_list = re.sub("[^\w']", " ", word_list).lower().split()
    for stop in stop_words:
        word_list[:] = [x for x in word_list if x != stop]

    tmpD = {}
    for word in word_list:
        tmpD.setdefault(word,[0, []])
        tmpD[word][0] += 1
        tmpD[word][1] = find_occurrences(plainText, word)

    for k,v in tmpD.iteritems():
        print "%s\t%d\t%s\t%d\t%s" % (k,v[0],url,docNum, '\t'.join(map(str, v[1])))

    docNum += 1