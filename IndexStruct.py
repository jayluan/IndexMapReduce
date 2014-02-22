#!/usr/bin/env python
'''
    IndexStruct.py
    purpose: Helper structures for read the index
'''


class Doc(object):
    def __init__(self, num, tfidf=0, word_count=0, count=0, pos=None):
        self.DocID = num
        self.TFIDF = tfidf 
        self.Count = count
        if pos is None:
            self.Positions = []
        else:
            self.Positions = pos


class Index(object):
    def __init__(self, word, freq=0, num_docs=0):
        self.Word = word
        self.Count = freq
        self.NumDocs = num_docs
        self.Docs = []

    #Append a Doc item to the index
    def Append(self, Doc):
        self.Docs.append(Doc)

    #Returns a dictionary of (DocID, TFIDF) pairs
    def GetDocTFIDF(self):
        entries = {}
        for doc in self.Docs:
            entries[doc.DocID] = doc.TFIDF
        return entries

    #Returns a dictionary of (DocID, Count) pairs
    def GetDocCount(self):
        entries = {}
        for doc in self.Docs:
            entries[doc.DocID] = doc.Count
        return entries

    #Returns a list of positions where the current word is listed
    #in a given DocId, or a single position at position=index  
    def GetDocPositions(self, DocId, position=None):
        for doc in self.Docs:
            if doc.DocID is DocId:
                if position is None:
                    return doc.Positions
                else:
                    return doc.Positions[position]
