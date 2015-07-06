from __future__ import division
"""Associate text features with each gender by parsing user.gender.taggedtweets file, compute MI"""

from math import log
from collections import defaultdict

def log2(x):
    return log(x, 2)

def parse_data(filename):
    user_features = defaultdict(set)   #{user: set of features}
    user_gender = {}
    for line in open(filename):
        userid, gender, date, statusid, rawtweet, toktweet, tagtweet = line.split('\t')
        feats = set(toktweet.lower().split())  #lowercase and split into words
        user_features[userid].update(feats)  #update tweet to user's set of all features
        if userid not in user_gender:
            user_gender[userid] = gender
    print "Parsed data"
    return user_features, user_gender

def get_mutual_information(user_features, user_gender):
    """Get mutual information between every feature and gender"""
    pospaircounts = defaultdict(float)   #Count(feat, female), Count(feat, male)
    negpaircounts = defaultdict(float)  #Count(no feat, female), Count(no feat, male)
    posfeatcounts = defaultdict(float)  #Count(feat)
    negfeatcounts = defaultdict(float)   #Count(no feat)

    genders = ['M', 'F']
    gendercounts = defaultdict(float)    #Count(gender)
    
    featureset = reduce(lambda x,y:x.union(y), user_features.values()) #set of all features across all users

    for userid, gender in user_gender.items():
        print '.',
        for feature in featureset:
            if feature in user_features[userid]:
                pospaircounts[(feature, gender)]+=1
                posfeatcounts[feature]+=1
            else:
                negpaircounts[(feature, gender)]+=1
                negfeatcounts[feature]+=1
        gendercounts[gender]+=1
                   
    numusers = len(user_features)
    mi = defaultdict(float)
    for feature in featureset:
        for gender in genders:
            if pospaircounts[(feature, gender)]>0:  #to avoid log error
                mi[feature] += pospaircounts[(feature, gender)]/numusers * log2(pospaircounts[(feature, gender)]*numusers/(gendercounts[gender] * posfeatcounts[feature]))
            if  negpaircounts[(feature, gender)]>0:   #to avoid log error
                 mi[feature] += negpaircounts[(feature, gender)]/numusers * log2(negpaircounts[(feature, gender)]*numusers/(gendercounts[gender] * negfeatcounts[feature]))

    print "Computed mutual information"

    feature_scores = sorted(mi.items(), key=lambda x:x[1], reverse=True)
    print 'Feature\t\tMI\tP(Female|Feature)'
    for feature, score in feature_scores[:200]:
        prob_female = pospaircounts[(feature, 'F')]/posfeatcounts[feature]  #P(female|feat)
        print '{0}\t\t{1:.3f}\t{2:.3f}'.format(feature, score, prob_female)

if __name__=='__main__':
    filename = 'user.gender.taggedtweets'
    
    user_features, user_gender = parse_data(filename)
    get_mutual_information(user_features, user_gender)
                                                                                                                                                                                               
        
