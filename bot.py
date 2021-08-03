import requests
import tweepy
import time
from os import environ
import urllib.request

from credentials import *

# Configure environment variables
# AKEY = environ['AKEY']
# ASKEY = environ['ASKEY']
# ATKEY = environ['ATKEY']
# ATSKEY = environ['ATSKEY']

# API setup
auth = tweepy.OAuthHandler(AKEY, ASKEY)
auth.set_access_token(ATKEY, ATSKEY)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()

# Set vars
INTERVAL = 15 * 60 # 15 minute interval
ntweets = 500

def search():
    counter = 0

    # API search query
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets' , lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):
        for media in tweet.entities.get("media",[{}]):
            if media.get("type",None) == "photo":
                try:
                    # Retweet
                    tweet.retweet()
                    print('Tweet Retweeted')
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break

                # Save image
                imageurl = tweet.entities["media"][0]["media_url_https"]
                print(imageurl)
                urllib.request.urlretrieve(imageurl, "images/%d.jpg" % counter)
                
                # Increment image counter limit
                counter += 1

                if counter == 25:
                    counter == 0

                # Set interval
                time.sleep(INTERVAL)



search()