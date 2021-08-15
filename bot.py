import tweepy
import time
from os import environ
import urllib.request
import boto3
import requests
import sys
# from credentials import *

try: 
    AKEY = environ['AKEY']
    ASKEY = environ['ASKEY']
    ATKEY = environ['ATKEY']
    ATSKEY = environ['ATSKEY']
except KeyError:
    print("Keys not accessible.")
    sys.exit(1)
    
# Authentication
auth = tweepy.OAuthHandler(AKEY, ASKEY)
auth.set_access_token(ATKEY, ATSKEY)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()

# Set interval and limit
INTERVAL = 15 * 60 # 30 minute interval
ntweets = 500
keywords = ["Sunset", "Sunrise", "Sunlight", "Dusk"]
antikeywords = ["Person", "Human"]
counter = 0

def search():
    # API search query
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets' , lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):
        for media in tweet.entities.get("media",[{}]):
            if media.get("type",None) == "photo":

                # Access image
                imageurl = tweet.entities["media"][0]["media_url_https"]
                image = getimage(imageurl)
                
                # Detect labels
                labels = define(image)
                confidence = 0

                for label in labels:
                    print(label["Name"], label["Confidence"])

                    if label["Name"] in keywords:
                        confidence = label["Confidence"]
                    elif label ["Name"] in antikeywords and label["Confidence"] > 70:
                        print("Image not appropriate.")
                        return False
                
                # When detection confidence is sufficient
                if confidence > 60:
                    
                    # Retweet
                    try:
                        # Retweet
                        tweet.retweet()
                        print('Tweet Retweeted')
                        
                        # Download photo
                        downloadimage(imageurl)
                        return True
                    
                    except tweepy.TweepError as e:
                        print(e.reason)
                        break
                    except StopIteration:
                        break


def define(image):
    client = boto3.client('rekognition', region_name='us-east-2')
    results = client.detect_labels(
        Image={
            'Bytes': image
            }
        )
    return results["Labels"]

def getimage(imageurl):
    response = requests.get(imageurl)
    imagebytes = response.content
    return imagebytes

def downloadimage(imageurl):    
    # Maximum image limit
    global counter
    if counter == 12:
        counter == 0
    else:
        counter += 1

    urllib.request.urlretrieve(imageurl, "static/images/%d.jpg" % counter)
    image = "static/images/%d.jpg" % counter

# Search for tweets until there is a hit
while True:
    hit = search()
    if hit == True:
        time.sleep(INTERVAL)
