import requests
import tweepy
import time
from credentials import *
from os import environ

AKEY = environ['AKEY']
ASKEY = environ['ASKEY']
ATKEY = environ['ATKEY']
ATSKEY = environ['ATSKEY']

auth = tweepy.OAuthHandler(AKEY, ASKEY)

auth.set_access_token(ATKEY, ATSKEY)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

ntweets = 500

def search():
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets' , lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):
        for media in tweet.entities.get("media",[{}]):
            if media.get("type",None) == "photo":
                try:
                    tweet.retweet()
                    print('Tweet Retweeted')
                    
                    ##image_content = requests.get(media["media_url"])
                    ##print(image_content)
                    time.sleep(100)
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break

search()