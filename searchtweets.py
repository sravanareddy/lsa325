# -*- coding: utf-8 -*-
"""Search tweets containing given terms"""

from twython import Twython
import time
import codecs
import sys
import string
from utilities import ProcessedTweet, write_dict_tsv
import argparse

if __name__=='__main__':
    #file twitapikeys.txt should contain at least two lines with consumer key and secret, optionally followed by access token and secret 
    CONSUMER_KEY, CONSUMER_SECRET = open('twitapikeys.txt').read().split()[:2] 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--basename', help='base name of file to write to', type=str, required=True)
    parser.add_argument('--numtweets', help='number of tweets to search in', type=int, default=10000)
    parser.add_argument('--searchterm', help='term to search for. separate multiple terms by _', required=True)
    parser.add_argument('--lang', help='language of tweets (ISO code). default = en', default='en')
    args = parser.parse_args()
    
    args.searchterm = args.searchterm.replace('_', ' ')
    
    o = codecs.open(args.basename+'.statuses.tsv', 'w', 'utf-8')
    orep = codecs.open(args.basename+'.replies.txt', 'w', 'utf-8')
    
    o.write('userid\ttweet\tstatusid\tdate\tlat\tlon\n')
    
    userinfo = {}
    searcher = Twython(CONSUMER_KEY, CONSUMER_SECRET)
    until_id = 1e30
    for batch in range(args.numtweets/100):  
        results = searcher.search(q=args.searchterm, count=100, max_id=until_id-1, result_type='recent')  #can change result_type to popular or mixed
        print "Searching until status", until_id

        if len(results['statuses'])==1:  #usually repeat after data runs out
            break
        
        for tweet in results['statuses']:
            ptweet = ProcessedTweet()
            success = ptweet.process_raw(tweet, userinfo, requiregeo = False, lang = args.lang, requireword = args.searchterm) 
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
    
    write_dict_tsv(userinfo, args.basename+'.userinfo.tsv')    
