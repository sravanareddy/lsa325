"""Get top n similar words for each word"""

import scipy
import scipy.spatial.distance
import argparse

def load_vectors(basename, maxwords):
    vectors = scipy.loadtxt(basename+'.word2vec')
    vectors = vectors[:maxwords, :]
    words = map(lambda line: line.split()[0],
                open(basename+'.wordcounts').readlines())[:maxwords]
    print "Loaded data"
    return vectors, words

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--basename', help='base name of word vector files', type=str)
    parser.add_argument('--maxwords', help='maximum number of words to consider', type=int)
    parser.add_argument('--n', help='number of most similar words', type=int)
    args = parser.parse_args()

    vectors, words = load_vectors(args.basename, args.maxwords)
    
    pairwise = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(vectors, 'cosine'))
    
    for i, word in enumerate(words):
        topkindices = scipy.argsort(pairwise[i, :])[1:args.n]
        print word.upper(),
        for ind in topkindices:
            print words[ind],
        print
