# -*- coding: utf-8 -*-
"""Search tweets containing given terms"""

from twython import Twython
import time
import codecs
import sys
import string
from utilities import ProcessedTweet, write_userinfo
                    
if __name__=='__main__':
    
    OAUTH_TOKEN = "14656609-IzjpUGipO5uDse1rFr3nXfBvVbX9T4hMHjkAvwA55"
    OAUTH_SECRET = "JYZoOPQK28fFv98d4zZg1OUBqIUKJQ6poQglmioz4"
    CONSUMER_KEY = "JksOBh39nyd95jagJQTZ8Q"
    CONSUMER_SECRET = "kx87N1Ge8iWuzwcWUH55PhUDOFCqBju6UqUtroYFo"

    word = sys.argv[1]
    n = int(sys.argv[2])
    
    o = codecs.open(word+'.statuses.tsv', 'w', 'utf-8')
    orep = codecs.open(word+'.replies.txt', 'w', 'utf-8')
    
    o.write('userid\ttweet\tstatusid\tdate\tlat\tlon\n')
    userinfo = {}
    searcher = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    until_id = 1e30
    for batch in range(n):  #at most n*100 tweets
        results = searcher.search(q=word, count=100, max_id=until_id-1, result_type='recent')  #can change result_type to popular or mixed
        print "Searching until status", until_id

        if len(results['statuses'])==1:  #usually repeat after data runs out
            break
        
        for tweet in results['statuses']:
            ptweet = ProcessedTweet()
            success = ptweet.process_raw(tweet, userinfo, requiregeo = False, lang = 'en', requireword = word) #change language, or set to None if unrestricted
            if success:
                o.write(ptweet.__str__())
                if ptweet.inreply:
                    orep.write('/'.join([ptweet.user, ptweet.status_id])
                               +': '
                               +'/'.join(ptweet.inreply)+'\n')
                until_id = min(until_id, int(ptweet.status_id))

        time.sleep(5) #throttling
    
    orep.close()
    o.close()
    
    if len(userinfo)>0:
        write_userinfo(userinfo, word+'.userinfo.tsv')    
