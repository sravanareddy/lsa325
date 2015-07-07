from __future__ import division
"""Associate text features with each category, compute probabilities and MI"""

from math import log
from collections import defaultdict
import sys

def log2(x):
    return log(x, 2)

def parse_data(filename):
    user_features = defaultdict(set)   #{user: set of features}
    user_category = {}
    for line in open(filename):
        userid, category, date, statusid, rawtweet, toktweet, tagtweet = line.split('\t')
        feats = set(toktweet.lower().split())  #lowercase and split into words
        user_features[userid].update(feats)  #update tweet to user's set of all features
        if userid not in user_category:
            user_category[userid] = category
    print "Parsed data"
    return user_features, user_category

def get_mutual_information(user_features, user_category):
    """Get mutual information between every feature and category"""
    pospaircounts = defaultdict(float)   #Count(feat, c1), Count(feat, c2)
    negpaircounts = defaultdict(float)  #Count(no feat, c1), Count(no feat, c2)
    posfeatcounts = defaultdict(float)  #Count(feat)
    negfeatcounts = defaultdict(float)   #Count(no feat)

    categorycounts = defaultdict(float)    #Count(category)
    
    featureset = reduce(lambda x,y:x.union(y), user_features.values()) #set of all features across all users

    for userid, category in user_category.items():
        print '.',
        for feature in featureset:
            if feature in user_features[userid]:
                pospaircounts[(feature, category)]+=1
                posfeatcounts[feature]+=1
            else:
                negpaircounts[(feature, category)]+=1
                negfeatcounts[feature]+=1
        categorycounts[category]+=1
                   
    numusers = len(user_features)
    mi = defaultdict(float)
    for feature in featureset:
        for category in categorycounts:
            if pospaircounts[(feature, category)]>0:  #to avoid log error
                mi[feature] += pospaircounts[(feature, category)]/numusers * log2(pospaircounts[(feature, category)]*numusers/(categorycounts[category] * posfeatcounts[feature]))
            if  negpaircounts[(feature, category)]>0:   #to avoid log error
                 mi[feature] += negpaircounts[(feature, category)]/numusers * log2(negpaircounts[(feature, category)]*numusers/(categorycounts[category] * negfeatcounts[feature]))

    print "Computed mutual information"

    feature_scores = sorted(mi.items(), key=lambda x:x[1], reverse=True)
    refcat = categorycounts.keys()[0]  #pick one of the two categories
    print 'Feature\tMI\tP({0}|Feature)'.format(refcat)
    for feature, score in feature_scores[:200]:
        prob = pospaircounts[(feature, refcat)]/posfeatcounts[feature]  
        print '{0}\t{1:.3f}\t{2:.3f}'.format(feature, score, prob)

if __name__=='__main__':
    filename = sys.argv[1]
    
    user_features, user_category = parse_data(filename)
    get_mutual_information(user_features, user_category)
                                                                                                                                                                                               
        
