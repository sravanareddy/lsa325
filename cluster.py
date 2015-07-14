"""Cluster word2vec words using k-means"""

import scipy
from scipy.cluster.vq import kmeans, vq
from collections import defaultdict
import sys

if __name__=='__main__':
    basename = sys.argv[1]
    maxwords = 10000
    k = 1000
    
    vectors = scipy.loadtxt(basename+'.word2vec')
    vectors = vectors[:maxwords, :]
    words = map(lambda line: line.split()[0],
                open(basename+'.wordcounts').readlines())[:maxwords]
    print "Loaded data"

    centroids,_ = kmeans(vectors, k)
    idx, _ = vq(vectors, centroids)

    clusters = defaultdict(set)
    for i, c in enumerate(idx):
        clusters[c].add(words[i])

    for c in clusters:
        print 'CLUSTER', c,
        for word in clusters[c]:
            print word,
        print
        print
