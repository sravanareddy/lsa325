# -*- coding: utf-8 -*-
"""Search tweets containing given terms"""

from twython import Twython
import time
import codecs
import sys
import json
import string
from utilities import ProcessedTweet
                    
if __name__=='__main__':
    
    OAUTH_TOKEN = "14656609-IzjpUGipO5uDse1rFr3nXfBvVbX9T4hMHjkAvwA55"
    OAUTH_SECRET = "JYZoOPQK28fFv98d4zZg1OUBqIUKJQ6poQglmioz4"
    CONSUMER_KEY = "JksOBh39nyd95jagJQTZ8Q"
    CONSUMER_SECRET = "kx87N1Ge8iWuzwcWUH55PhUDOFCqBju6UqUtroYFo"

    word = sys.argv[1]
    n = int(sys.argv[2])
    
    o = codecs.open(word+'.statuses.tsv', 'w', 'utf-8')
    orep = codecs.open(word+'.replies.txt', 'w', 'utf-8')
    
    userinfo = {}
    searcher = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    until_id = 1e30
    for batch in range(n):  #at most n*100 tweets
        results = searcher.search(q=word.replace('_', ' OR '), count=100, max_id=until_id-1)
        for tweet in results['statuses']:
            ptweet = ProcessedTweet()
            success = ptweet.process_raw(tweet, userinfo, requiregeo = False)
            if success:
                o.write(ptweet.__str__())
                if ptweet.inreply:
                    orep.write('/'.join([ptweet.user, ptweet.status_id])
                               +': '
                               +'/'.join(ptweet.inreply)+'\n')
                until_id = min(until_id, int(ptweet.status_id))
        print "Searching until status", until_id
        time.sleep(5) #throttling
    
    oj = open(word+'.userinfo.json', 'w')
    json.dump(userinfo, oj)
    oj.close()
    
    orep.close()
    o.close()
