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

class TrackStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, start_time, maxsecs, lang, trackterm):
        TwythonStreamer.__init__(self, app_key, app_secret, oauth_token, oauth_token_secret)
        self.userinfo = {}   
        self.start_time = start_time
        self.maxsecs = maxsecs
        self.lang = lang
        self.trackterm = trackterm
        print "initialized"
    
    def on_error(self, status_code, tweet):
        print status_code, tweet
        self.disconnect()
        
    def on_success(self, tweet):
        if tweet:
            ptweet = ProcessedTweet()
            success = ptweet.process_raw(tweet, self.userinfo, requiregeo=False, lang=self.lang, requireword=self.trackterm)
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
 
    CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET = open('twitapikeys.txt').read().split()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--basename', help='base name of file to write to', type=str, required=True)
    parser.add_argument('--maxhours', help='maximum hours to run script', type=float, required=True)
    parser.add_argument('--lang', help='language of tweets (ISO code). default = en', default=None)
    parser.add_argument('--trackterm', help='term to track in streamer. separate multiple words by _.', required=True)
    
    args = parser.parse_args()
    args.trackterm = args.trackterm.replace('_', ' ')
    
    print 'Streaming', args.lang, 'tweets containing', args.trackterm, 'for', args.maxhours, 'hours'
    
    maxsecs = args.maxhours*60*60  #how long to stream
    start_time = time.time()

    o = codecs.open(args.basename+'.statuses.tsv', 'w', 'utf-8')
    orep = codecs.open(args.basename+'.replies.txt', 'w', 'utf-8')
    
    o.write('userid\ttweet\tstatusid\tdate\tlat\tlon\n')
    
    stream = TrackStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET, start_time, maxsecs, args.lang, args.trackterm)
    while time.time()-start_time<maxsecs:
        try:
            stream.statuses.filter(track=args.trackterm) #stream tweets containing word 
        except Exception as e:
            print e
            continue

    write_dict_tsv(stream.userinfo, args.basename+'.userinfo.tsv')
    
    orep.close()
    o.close()
