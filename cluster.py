"""Cluster word2vec words using k-means"""

import scipy
from scipy.cluster.vq import kmeans, vq, whiten
from collections import defaultdict
from similar_words import load_vectors
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--basename', help='base name of word vector files', type=str)
    parser.add_argument('--maxwords', help='maximum number of words to cluster', type=int)
    parser.add_argument('--k', help='number of clusters', type=int)
    args = parser.parse_args()
    
    vectors, words = load_vectors(args.basename, args.maxwords)

    vectors = whiten(vectors)
    centroids,_ = kmeans(vectors, args.k)
    idx, dist_to_center = vq(vectors, centroids)

    clusters = defaultdict(list)
    for i, c in enumerate(idx):
        clusters[c].append((words[i], dist_to_center[i]))

    for c in range(args.k):
        print 'CLUSTER', c+1,
        words = sorted(clusters[c], key=lambda x:x[0])
        for word, _ in words:
            print word,
        print
        print
