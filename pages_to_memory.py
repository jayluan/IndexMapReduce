import sys


def find_occurrences(text, word):
    word = word.center(len(word)+2)
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


def pages_to_mem(pagesFilename='output.txt'):
    docs = []
    with open(pagesFilename) as f:
        for line in f:
            urlStart = find_nth(line, 'AFUCKINGDELIMITER', 1) + 17
            urlEnd = find_nth(line, 'AFUCKINGDELIMITER', 2)
            url = line[urlStart:urlEnd]
            startIndex = find_nth(line, 'AFUCKINGDELIMITER', 3) + 19
            endIndex = find_nth(line, 'AFUCKINGDELIMITER', 4) - 3
            plainText = line[startIndex:endIndex]
            docs.append(plainText)
    return docs