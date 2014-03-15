from sklearn.feature_extraction.text import TfidfVectorizer
from pages_to_memory import pages_to_mem
from sklearn.metrics.pairwise import linear_kernel
from itertools import izip
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import coo_matrix
import sys
from scipy.sparse.linalg import svds
import numpy as np
import cPickle as pickle
from utilities import Utility
from NDCG import CalcNDCG

output_text = False


# Loads an index and returns the TFIDF matrix for both the title and terms
# and also returns dictionaries for each matrix mapping words to indicies
def LoadDocuments(fname, collect_links):
    crawl_data, urls, titles = pages_to_mem(fname, collect_links)
    tfidfVect = TfidfVectorizer(strip_accents='unicode', stop_words='english', ngram_range=(1,2))
    term_tfidf = tfidfVect.fit_transform(crawl_data)
    dict_values = tfidfVect.get_feature_names()
    i = iter(dict_values)
    term_b = dict(izip(i, xrange(len(dict_values))))    # dictionary of words and indicies

    tfidfVect = TfidfVectorizer(strip_accents='unicode', stop_words='english', ngram_range=(1,2))
    title_tfidf = tfidfVect.fit_transform(titles)
    dict_values = tfidfVect.get_feature_names()
    i = iter(dict_values)
    title_b = dict(izip(i, xrange(len(dict_values))))    # dictionary of words and indicies
    return title_tfidf, title_b, term_tfidf, term_b, urls


#parse a query into either ngrams or if it's less than the size of an ngram, into
#individual words
def ParseQuery(query, ngram_size):
    indata = query.split()
    output = []
    for i in range(len(indata) - ngram_size + 1):
        output.append(" ".join(indata[i:i+ngram_size]))
    if not output: # if ngrams don't exist in the query, just return split input
        output = indata
    return output


def GetTop5Tfidf(query, tfidf, dictionary):
#    query = query.split()
#    query = [x.strip().lower() for x in query]
    query.lower()
    query_vector = lil_matrix((1, len(dictionary)), dtype='float64')
    try:
        query_vector[0, dictionary[query]] = 1
    except KeyError, err:
        print 'Warning, Key %s Not Found' % (err)
    if query_vector.nnz == 0:
        return None, None

    cosine_similarities = linear_kernel(query_vector, tfidf).flatten()
    cos_indicies = cosine_similarities.argsort()[:-6:-1]
    scores = cosine_similarities[cos_indicies]
    return cos_indicies, scores


#user query terms to figure out resultant idea position, then compare idea
#position to the location of doucments 
#Note: Terms_redeuced should be NxK
#Note: Docs_reduced should also be NxK
def GetTop5Enhanced(query, Terms_reduced, Docs_reduced, Term_dictionary):
    query = query.split()
    query = [x.strip().lower() for x in query]
    query_pos = []
    for i in query:
        try:
            query_pos.append(Terms_reduced[Term_dictionary[i]])
        except KeyError, err:
            print 'Warning, Key %s Not Found' % (err)
    if len(query_pos) == 0:
        return None, None
    query_pos = np.array(query_pos).mean(axis=0)
    cosine_similarities = linear_kernel(query_pos, Docs_reduced).flatten()
    cos_indicies = cosine_similarities.argsort()[:-6:-1]
    scores = cosine_similarities[cos_indicies]
    return cos_indicies, scores


def ExpandTitleMatrix(term_tfidf, term_dict, title_tfidf, title_dict):
    total_matrix = lil_matrix((term_tfidf.shape), dtype=np.float64)
    k = 0
    for term in title_dict:
        try:
            title_index = term_dict[term]
        except KeyError, err:
            title_index = None
        if title_index is not None:
            for i in range(total_matrix.shape[0]-1):
                if title_tfidf[i, title_dict[term]] != 0:
                    total_matrix[i, title_dict[term]] = title_tfidf[i, title_dict[term]]
        print "Expanded %d/%d rows" % (k, len(title_dict))
        k += 1
    return total_matrix


#Calculate weighted TF-IDF matrix basied on term and title tf-idfs
def AddTermTitleMat(term_tfidf, term_dict, title_tfidf, title_dict):
    #total_tfidf = lil_matrix(term_tfidf)
    term_tfidf = csr_matrix(term_tfidf)

    title_tfidf = ExpandTitleMatrix(term_tfidf, term_dict, title_tfidf, title_dict)
    return term_tfidf + title_tfidf
    #add the weighted term and weighted title tfidfs if title tfidf exists
    # i = 0
    # for term in term_dict:
    #     #get the tfidfs for the current term
    #     term_col = term_tfidf[:, term_dict[term]]
        
    #     #if it exists, get the title term
    #     try:
    #         title_col = title_tfidf[:, title_dict[term]]
    #         #total_tfidf[:, term_dict[term]] += (total_tfidf[:, term_dict[term]].tocsr() + title_col).tolil()
    #         total_tfidf[:, term_dict[term]] += csr_matrix(total_tfidf[:, term_dict[term]].todense() + title_col.todense()).tolil()
    #     #if it doesn't exist, just add 0's
    #     except KeyError, err:
    #         t = 0
    #     i += 1
    #     print "%d/%d" % (i, len(term_dict))
    return total_tfidf


#Original tfidf function that just returns page rank based on tfidf
def main2():

    tfidf, dictionary, urls, relationships = LoadDocuments(sys.argv[1], True)
    
    util = Utility()
    util.addEdges(relationships)
    pageRank = util.pageRank()

    query = ""
    f = open('milestone2.txt', 'w')
    while(True):
        url_return = np.array([])
        score = np.array([])
        query = raw_input("Please enter query ('q' to quit): ")
        if query == "q":
            break

        query_list = ParseQuery(query, 2)
        for word in query_list:
            tmp_urls, tmp_scores = GetTop5Tfidf(query, tfidf, dictionary)
            url_return = np.concatenate((url_return, tmp_urls))
            scores = np.concatenate((score, tmp_scores))
        url_return = url_return.astype(int)

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
            print "NDCG Score: %f" % (CalcNDCG([urls[f] for f in url_return], query))
    f.close()


#New and improved page ranking algorithm
def main(fname):
    print "Initializing..."
    weight_title = 0.3
    weight_term = 0.3
    K = 400
    title_tfidf = pickle.load(open('title_tfidf.p', "rb"))
    term_tfidf = pickle.load(open('term_tfidf.p', "rb"))
    title_dict = pickle.load(open('title_dict.p', "rb"))
    term_dict = pickle.load(open('term_dict.p', "rb"))

    # title_tfidf, title_dict, term_tfidf, term_dict, urls = LoadDocuments(fname)
    # pickle.dump(title_tfidf, open('title_tfidf.p', "wb"))
    # pickle.dump(term_tfidf, open('term_tfidf.p', "wb"))
    # pickle.dump(title_dict, open('title_dict.p', "wb"))
    # pickle.dump(term_dict, open('term_dict.p', "wb"))


    print "Loaded Index"
    #apply weighting to the tfidf matricies
    title_tfidf *= weight_title
    term_tfidf *= weight_term
    total_tfidf = term_tfidf
    #add the matricies together
    total_tfidf = AddTermTitleMat(term_tfidf, term_dict, term_tfidf, title_dict)
    print "Added Matricies"
    if K > min(total_tfidf.shape[0], total_tfidf.shape[1])-1:
        K = min(total_tfidf.shape[0], total_tfidf.shape[1])-1
    print "Doing SVD...."
    U, s, V = svds(total_tfidf, k=K)
    print "SVD Done"
    s_reduced  = np.diag(s)
    U_reduced = np.dot(U, s_reduced)
    V_reduced = np.dot(s_reduced, V).T
    print "Reduced SVD Done"
    f = open('milestone2.txt', 'w')
    while(True):
        query = raw_input("Please enter query ('q' to quit): ")
        if query == "q":
            break
        url_return, scores = GetTop5Enhanced(query, V_reduced, U_reduced, term_dict)
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
    main(sys.argv[1])




















