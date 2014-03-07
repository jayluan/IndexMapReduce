import sys
from bs4 import BeautifulSoup as bs


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
    urls = []
    titles = []
    totalRelationships = []
    fuck = 0
    with open(pagesFilename) as f:
        for line in f:
            urlStart = find_nth(line, 'AFUCKINGDELIMITER', 1) + 17
            urlEnd = find_nth(line, 'AFUCKINGDELIMITER', 2)
            url = line[urlStart:urlEnd]
            startIndex = find_nth(line, 'AFUCKINGDELIMITER', 3) + 19
            endIndex = find_nth(line, 'AFUCKINGDELIMITER', 4) - 3
            plainText = line[startIndex:endIndex]
            htmlStartIndex = find_nth(line, 'AFUCKINGDELIMETER', 4) + 17
            htmlEndIndex = find_nth(line, 'AFUCKINGDELIMITER', 5)
            html = line[htmlStartIndex:htmlEndIndex]
            linkAnchors = []
            soup = bs(html)
            for link in soup.find_all('a'):
                linkAnchors.append(link.get('href'))
            linkRelationships = []
            linkCount = 0
            externalLinkCount = 0
            for link in linkAnchors:
                if link != None and link.startswith('http'):
                    linkRelationships.append((url,link))
                    externalLinkCount += 1
                linkCount += 1
            if linkCount != externalLinkCount:
                linkRelationships.append((url,url))
            titleStartIndex = html.find('<title>') + 7
            titleEndIndex = html.find('</title>')
            titleStr = html[titleStartIndex:titleEndIndex]
            titles.append(titleStr)
            docs.append(plainText)
            urls.append(url)
            totalRelationships.append(linkRelationships)
            print fuck
            fuck += 1
    return docs, urls, titles, tuple(totalRelationships)









