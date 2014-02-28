from sklearn.feature_extraction.text import TfidfVectorizer
from pages_to_memory import pages_to_mem
from sklearn.metrics.pairwise import linear_kernel
from itertools import izip
from scipy.sparse import lil_matrix


def LoadDocuments():
    crawl_data, urls = pages_to_mem('../output_test.txt')
    tfidfVect = TfidfVectorizer(strip_accents='unicode', stop_words='english')
    tfidf = tfidfVect.fit_transform(crawl_data)
    dict_values = tfidfVect.get_feature_names()
    i = iter(dict_values)
    b = dict(izip(i,xrange(len(dict_values))))
    return tfidf, b, urls


def GetTop5(query, tfidf, dictionary):
    query = query.split()
    query = [x.strip().lower() for x in query]
    query_vector = lil_matrix((1, len(dictionary)), dtype='float64')
    try:
        for i in query:
            query_vector[0, dictionary[i]] = 1
    except KeyError, err:
        print err
        return

    cosine_similarities = linear_kernel(query_vector, tfidf).flatten()
    return cosine_similarities.argsort()[:-5:-1]


def main():
    tfidf, dictionary, urls = LoadDocuments()
    query = ""
    while(True):
        query = raw_input("Please enter query: ")
        if query == "q":
            break
        url_return = GetTop5(query, tfidf, dictionary)
        print [urls[i] for i in url_return]

if __name__ == "__main__":
    main()
