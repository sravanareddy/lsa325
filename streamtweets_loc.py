# -*- coding: utf-8 -*-
"""Mine tweets from Streaming API"""

from twython import TwythonStreamer
import time
import codecs
import sys
import json
import string
from utilities import ProcessedTweet, write_dict_tsv
import argparse

class LocationStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, start_time, maxsecs, lang):
        TwythonStreamer.__init__(self, app_key, app_secret, oauth_token, oauth_token_secret)
        self.userinfo = {}   
        self.start_time = start_time
        self.maxsecs = maxsecs
        self.lang = lang
        print "initialized"
    
    def on_error(self, status_code, tweet):
        print status_code, tweet
        self.disconnect()
        
    def on_success(self, tweet):
        if tweet:
            ptweet = ProcessedTweet()
            success = ptweet.process_raw(tweet, self.userinfo, requiregeo=True, lang=self.lang, requireword=False) 
            if success:
                o.write(ptweet.__str__())
                if ptweet.inreply:
                    orep.write('/'.join([ptweet.user, ptweet.status_id])
                               +': '
                               +'/'.join(ptweet.inreply)+'\n')
        #check if max time has lapsed
        if time.time()-self.start_time>maxsecs:
            self.disconnect()
                    
if __name__=='__main__':
    
    #File twitapikeys.txt should contain 4 lines: consumer key, consumer secret, access token, access secret 
    CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET = open('twitapikeys.txt').read().split()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--basename', help='base name of file to write to', type=str, required=True)
    parser.add_argument('--maxhours', help='maximum hours to run script', type=float, required=True)
    parser.add_argument('--boundingbox', help='location bounding box. default (US and Canada) = -138, 24, -52, 80', default='-138, 24, -52, 80', type=str)  #US and Canada; change bounding box for other locations
    parser.add_argument('--lang', help='language of tweets (ISO code). default = en', default=None)
    args = parser.parse_args()
    print 'Streaming', args.lang, 'tweets within', args.boundingbox, 'for', args.maxhours, 'hours' 
    
    maxsecs = args.maxhours*60*60  #how long to stream
    start_time = time.time()

    o = codecs.open(args.basename+'.statuses.tsv', 'w', 'utf-8')
    orep = codecs.open(args.basename+'.replies.txt', 'w', 'utf-8')
    
    o.write('userid\ttweet\tstatusid\tdate\tlat\tlon\n')
    
    stream = LocationStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET, start_time, maxsecs, args.lang)
    while time.time()-start_time<maxsecs:
        try:
            stream.statuses.filter(locations=args.boundingbox) 
        except Exception as e:
            continue

    write_dict_tsv(stream.userinfo, args.basename+'.userinfo.tsv')
    
    orep.close()
    o.close()
