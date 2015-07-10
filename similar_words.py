"""Get top k similar words for each word"""

import scipy
import scipy.spatial.distance
import sys

if __name__=='__main__':
    basename = sys.argv[1]
    maxwords = 3000
    k = 20
    
    vectors = scipy.loadtxt(basename+'.word2vec')
    vectors = vectors[:maxwords, :]
    words = map(lambda line: line.split()[0],
                open(basename+'.wordcounts').readlines())[:maxwords]
    
    pairwise = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(vectors, 'cosine'))
    
    for i, word in enumerate(words):
        topkindices = scipy.argsort(pairwise[i, :])[1:k]
        print word.upper(),
        for ind in topkindices:
            print words[ind],
        print
