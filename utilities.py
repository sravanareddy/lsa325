import codecs

class ProcessedTweet:
    def __init__(self):
        self.user = None
        self.loc = {'lat': 0, 'lon': 0}
        self.status_id = None
        self.text = None
        self.datetime = None
        self.inreply = None
    def set_loc(self, coordinates):
        self.loc['lat'] = coordinates['coordinates'][0]
        self.loc['lon'] = coordinates['coordinates'][1]
    def set_inreply(self, tweet):
        if 'in_reply_to_user_id_str' in tweet and tweet['in_reply_to_user_id_str']: #tweet is a reply           
            self.inreply = (tweet['in_reply_to_user_id_str'],
                            tweet['in_reply_to_status_id_str'] if tweet['in_reply_to_status_id_str'] else 'None')
    def __str__(self):
        try:
            return '\t'.join([self.user, 
                              self.text, 
                              self.status_id, 
                              self.datetime, 
                              str(self.loc['lat']), 
                              str(self.loc['lon'])])+'\n'
        except Exception as e:
            print e
            return ''
    def process_raw(self, tweet, userinfo, requiregeo, lang=None, requireword=None):
        if tweet=='' or tweet=={}:  #blank lines                                    
            return False
        if lang and ('lang' not in tweet or tweet['lang']!=lang):  #tweets from wrong language    
            return False
        if 'retweeted_status' in tweet: #native retweets                               
            return False
        if tweet['text'].startswith('RT'):  #naive retweets                            
            return False
        if requiregeo and (not tweet['coordinates'] or not tweet['coordinates']['coordinates']): #geo-location  
            return False
        if tweet['user']['contributors_enabled']:   #shared accounts                   
            return False
        if tweet['user']['verified']:   #celebrities                                  
            return False
        if not tweet['text']:   #blank                                                
            return False
        if requireword and requireword not in tweet['text']:  #word to be in tweet
            return False
        #hopefully, tweet is valid now
        self.text = tweet['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        self.status_id = tweet['id_str']
        self.user = tweet['user']['id_str']
        self.datetime = tweet['created_at']
        if 'coordinates' in tweet and tweet['coordinates']: 
            self.set_loc(tweet['coordinates'])
        self.set_inreply(tweet)
        
        if 'user' in tweet:
            if self.user not in userinfo:
                userinfo[self.user] = {}
            for attr in ['screen_name', 
                         'created_at', 
                         'name', 
                         'location', 
                         'statuses_count', 
                         'friends_count', 
                         'followers_count', 
                         'favourites_count']:
                userinfo[self.user][attr] = tweet['user'][attr]
            
            userinfo[self.user]['description'] = tweet['user']['description'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        return True

def write_userinfo(userinfo, filename):
    ou = codecs.open(filename, 'w', 'utf8')
    fields = userinfo[userinfo.iterkeys().next()].keys() #convoluted but only way of getting list of fields
    ou.write('userid\t'+'\t'.join(fields)+'\n')
    for userid in userinfo:
        ou.write(userid+'\t')
        for field in fields:
            ou.write(unicode(userinfo[userid][field])+'\t')
        ou.write('\n')
    ou.close()
