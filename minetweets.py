# -*- coding: utf-8 -*-
"""Mine tweets from Streaming API"""

from twython import TwythonStreamer
import time
import codecs
import sys
import json
import string
                    
class ProcessedTweet:
    def __init__(self):
        self.user = None 
        self.loc = {'lat': None, 'lon': None}
        self.status_id = None
        self.text = None
        self.time = None
    def set_text(self, text):
        self.text = text
    def set_statusid(self, status_id):
        self.status_id = status_id
    def set_user(self, userid):
        self.user = userid
    def set_time(self, dstr):
        self.time = dstr
    def set_loc(self, coordinates):
        self.loc['lat'] = coordinates['coordinates'][0]
        self.loc['lon'] = coordinates['coordinates'][1]
    def __str__(self):
        try:
            return '\t'.join([self.user, self.text, self.status_id, self.time, str(self.loc['lat']), str(self.loc['lon'])])+'\n'
        except Exception as e:
            print e
            return ''
 
def process_tweet(tweet, userinfo):
    ptweet = ProcessedTweet()
    if tweet=='' or tweet=={}:  #blank lines                   
        return
    elif 'lang' not in tweet or tweet['lang']!='en':  #non-english tweets
        return
    elif 'retweeted_status' in tweet: #native retweets
        return
    elif tweet['text'].startswith('RT'):  #naive retweets
        return
    elif not tweet['coordinates'] or not tweet['coordinates']['coordinates']: #geo-location
        return
    elif tweet['user']['contributors_enabled']:   #shared accounts
        return
    elif tweet['user']['verified']:   #celebrities
        return
    elif not tweet['text']:   #blank
        return
    else:
        ptweet.set_text(tweet['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' '))
        ptweet.set_statusid(tweet['id_str'])
        ptweet.set_user(tweet['user']['id_str'])
        ptweet.set_time(tweet['created_at'])
        ptweet.set_loc(tweet['coordinates'])
    
    if 'user' in tweet:
        if ptweet.user not in userinfo:
            userinfo[ptweet.user] = {}
        for attr in ['screen_name', 'created_at', 'name', 'location', 'statuses_count', 'friends_count', 'following', 'favourites_count', 'description']:
            userinfo[ptweet.user][attr] = tweet['user'][attr]
    
    return ptweet

class CustomStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, start_time, maxsecs):
        TwythonStreamer.__init__(self, app_key, app_secret, oauth_token, oauth_token_secret)
        self.userinfo = {}   
        self.start_time = start_time
        self.maxsecs = maxsecs
        print "initialized"
    
    def on_error(self, status_code, tweet):
        print status_code, tweet
        self.disconnect()
        
    def on_success(self, tweet):
        if tweet:
            ptweet = process_tweet(tweet, self.userinfo)
            if ptweet:
                o.write(ptweet.__str__())
                if 'in_reply_to_user_id_str' in tweet and tweet['in_reply_to_user_id_str']:
                    #tweet is a reply
                    orep.write(ptweet.user+'/'+ptweet.status_id+': '+
                               tweet['in_reply_to_user_id_str']+'/'+str(tweet['in_reply_to_status_id'])+'\n')
        #check if max time has lapsed
        if time.time()-self.start_time>maxsecs:
            self.disconnect()
                    
if __name__=='__main__':
    
    OAUTH_TOKEN = "14656609-IzjpUGipO5uDse1rFr3nXfBvVbX9T4hMHjkAvwA55"
    OAUTH_SECRET = "JYZoOPQK28fFv98d4zZg1OUBqIUKJQ6poQglmioz4"
    CONSUMER_KEY = "JksOBh39nyd95jagJQTZ8Q"
    CONSUMER_SECRET = "kx87N1Ge8iWuzwcWUH55PhUDOFCqBju6UqUtroYFo"

    basename, maxhours = sys.argv[1:3]
    
    maxsecs = float(maxhours)*60*60  #how long to stream
    start_time = time.time()

    o = codecs.open(basename+'.statuses.tsv', 'w', 'utf-8')
    orep = codecs.open(basename+'.replies.txt', 'w', 'utf-8')
    
    stream = CustomStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET, start_time, maxsecs)
    while time.time()-start_time<maxsecs:
        try:
            stream.statuses.filter(locations='-138, 24, -52, 80') #US and Canada; change bounding box for other locations
        except Exception as e:
            print e
            continue

    oj = open(basename+'.userinfo.json', 'w')
    json.dump(stream.userinfo, oj)
    oj.close()
    
    orep.close()
    o.close()
