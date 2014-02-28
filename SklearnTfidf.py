from sklearn.feature_extraction.text import TfidfVectorizer
from pages_to_memory import pages_to_mem
from sklearn.metrics.pairwise import linear_kernel
from itertools import izip
from scipy.sparse import lil_matrix
import sys
import numpy as np

output_text = True


def LoadDocuments(fname):
    crawl_data, urls = pages_to_mem(fname)
    tfidfVect = TfidfVectorizer(strip_accents='unicode', stop_words='english')
    tfidf = tfidfVect.fit_transform(crawl_data)
    dict_values = tfidfVect.get_feature_names()
    i = iter(dict_values)
    b = dict(izip(i, xrange(len(dict_values))))
    return tfidf, b, urls


def GetTop5(query, tfidf, dictionary):
    query = query.split()
    query = [x.strip().lower() for x in query]
    query_vector = lil_matrix((1, len(dictionary)), dtype='float64')
    try:
        for i in query:
            query_vector[0, dictionary[i]] = 1
    except KeyError, err:
        print 'Warning, Key %s Not Found' % (err)
    if query_vector.nnz == 0:
        return None, None

    cosine_similarities = linear_kernel(query_vector, tfidf).flatten()
    cos_indicies = cosine_similarities.argsort()[:-6:-1]
    scores = cosine_similarities[cos_indicies]
    return cos_indicies, scores


def main():
    tfidf, dictionary, urls = LoadDocuments(sys.argv[1])
    query = ""
    f = open('milestone2.txt', 'w')
    while(True):
        query = raw_input("Please enter query ('q' to quit): ")
        if query == "q":
            break
        url_return, scores = GetTop5(query, tfidf, dictionary)
        if url_return is None:
            if output_text:
                f.write('Query: %s\nNo Results Found\n\n' % (query))
            print "Sorry, no results found...\n\n"
        else:
            print "TF-IDF\t\tURL(s)"
            elegant_return = ['%.6f' % (i) + '\t' + urls[k] for i, k in zip(scores, url_return)]
            if output_text:
                f.write('Query: %s\nResults\n----------------------------------------------\n\tTF-IDF\t\tURL\n\t' % (query) + '\n\t'.join(elegant_return))
                f.write("\n\n")
            print "\n".join(elegant_return)+'\n\n'

    f.close()

if __name__ == "__main__":
    main()
