'''
    NDCG.py
    Purpose: computes the normalized discounted cumulative gain for a list
             of querries for our cs 221 project. See useage in main()

    Note: google_results.txt must be in the same directory as this file

'''
import numpy as np


# This is the main function you want to call.
# Pass it a list of urls and the query term used to get the
# list of urls (e.g. 'Computer Science', 'REST') and it will
# return the NDCG value for your URLS
def CalcNDCG(urls, query_term):
    dictionary = LoadGoogleScores('google_results.txt')
    truth_list = dictionary[query_term.lower()]

    #make truth list rankings as proposed by the professor
    truth_list_rank = [5, 4, 3, 2, 1, 0, 0, 0, 0, 0]
    url_ranks = GetRankings(truth_list, truth_list_rank, urls)

    score = rawCalcNDCG(truth_list, truth_list_rank,
                        urls, url_ranks)
    return score


# Calculates the NDCG score for a given list and scores by normalizing
# with the ideal links and scores
def rawCalcNDCG(ideal, ideal_scores, given, given_scores):
    DCG = CalcDCG(given, given_scores)
    IDCG = CalcDCG(ideal, ideal_scores)
    if IDCG == 0:    # Make sure we're not dividng by 0
        return 0.
    return float(DCG/IDCG)


# Calculate DCG value for a list of urls and its list of scores
def CalcDCG(urls, scores):
    total = 0.
    position = 1
    for link, score in zip(urls, scores):
        if position == 1:
            total += score
        else:
            total += score/np.log2(position)
        position += 1

    return total


# Returns list of scores for a given list of urls by
# comparing the given list to an ideal list and ideal_scores
def GetRankings(ideal, ideal_scores, given):
    return_scores = []
    for i in given:

        # if the url is in the ideal list, append the ideal score
        if i in ideal:
            return_scores.append(ideal_scores[ideal.index(i)])
        # else just append 0 because it wasn't there
        else:
            return_scores.append(0)
    return return_scores


#Loads google_results.txt
def LoadGoogleScores(fname):
    google = {}
    with open(fname, 'r') as f:
        while True:
            #get the query word(s)
            query = f.readline()
            query = query.strip().lower()

            # if no query word exists, we opened a blank document or EOL
            if not query:
                if len(google) == 0:
                    return None
                else:
                    return google

            # iterate through and store the 10 results from the document
            # for the given word
            results = []
            for i in xrange(10):
                results.append(f.readline().strip())
            google[query] = results

            # go to the next set of search querries
            f.readline()


#sample useage
def main():
    test_url = ['http://www.ics.uci.edu/~fielding/pubs/dissertation/conclusions.htm',
                'http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm',
                'http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm',
                'http://www.ics.uci.edu/~eppstein/pix/ontheroad/BwilOrchard.html',
                'http://vcp.ics.uci.edu/content/harmonizing-architectural-dissonance-rest-based-architectures-0']

    test_query = "REST"

    score = CalcNDCG(test_url, test_query)
    print "NDCG Score for %s is: %f" % (test_query, score)

if __name__ == '__main__':
    main()
