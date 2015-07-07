from __future__ import division
"""Associate text features with each category, compute probabilities and MI"""

from math import log
import sys

def log2(x):
    return log(x, 2)

#Note for programmers: code will be cleaner with defaultdict. using ordinary dicts here for clarity

def get_mutual_information(filename):
    """Read and parse data, compute mutual information between words and user categories"""
    categories = {}   #{category: speakers of this category}
    features = {}  #{feat: speakers who use this feature}
    pos_categories_features = {}   #{category: {feat: speakers of category who use this feat}}
    neg_categories_features = {}   #{category: {feat: speakers of category who do not use this feat}}
    users = set()   #set of all users in data
    
    for line in open(filename):
        userid, c, date, statusid, rawtweet, toktweet, tagtweet = line.split('\t')
        users.add(userid)
        
        if c not in categories:
            categories[c] = set()
            pos_categories_features[c] = {}
        categories[c].add(userid)
            
        feats = set(toktweet.lower().split())  #lowercase tweet and split into words

        for feat in feats:
            if feat not in pos_categories_features[c]:
                pos_categories_features[c][feat] = set()
            pos_categories_features[c][feat].add(userid)
            
            if feat not in features:
                features[feat] = set()
            features[feat].add(userid)

    print "Parsed data"

    numfeats = len(features)  #num of features
    print numfeats, "features"
    numusers = len(users)   #num of users 
    print numusers, "users"

    #keep sizes of sets, not sets themselves
    for feat in features:
        features[feat] = len(features[feat])
    for c in categories:
        categories[c] = len(categories[c])
    for c in pos_categories_features:
        for feat in features:
            if feat in pos_categories_features[c]:
                pos_categories_features[c][feat] = len(pos_categories_features[c][feat])
            else:
                pos_categories_features[c][feat] = 0

    for c in categories:
        print c, categories[c], "users"

    print "Computed counts"
            
    mi = {}
    for feat in features:
        mi[feat] = 0.0
        for c in categories:
            #print c, feat, features[feat], pos_categories_features[c][feat]
            
            catprob = categories[c]/numusers

            #prob of speakers of category c using feat
            featprob = features[feat]/numusers
            jointprob = pos_categories_features[c][feat]/numusers
            if jointprob > 0 and featprob > 0:
                mi[feat] += jointprob * log2(jointprob/(catprob * featprob))
                
            #prob of speakers of category c NOT using feat
            featprob = 1 - featprob
            jointprob = (categories[c] - pos_categories_features[c][feat])/numusers
            if jointprob > 0 and featprob > 0:
                mi[feat] += jointprob * log2(jointprob/(catprob * featprob))

    print "Computed mutual information"

    feature_scores = sorted(mi.items(), key=lambda x:x[1], reverse=True)
    refcat = categories.keys()[0]  #pick one of the categories
    print 'Feature\tMI\tP({0}|Feature)'.format(refcat)
    for feat, score in feature_scores[:200]:
        prob = pos_categories_features[refcat][feat]/features[feat]
        print '{0}\t{1:.3f}\t{2:.3f}'.format(feat, score, prob)

if __name__=='__main__':
    filename = sys.argv[1]
    get_mutual_information(filename)
                                                                                                                                                                                               
        
