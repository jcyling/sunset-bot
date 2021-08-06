import tweepy
import time
from os import environ
import urllib.request
import boto3
import requests

# from credentials import *

# Configure environment variables
AKEY = environ['AKEY']
ASKEY = environ['ASKEY']
ATKEY = environ['ATKEY']
ATSKEY = environ['ATSKEY']

# API setup
auth = tweepy.OAuthHandler(AKEY, ASKEY)
auth.set_access_token(ATKEY, ATSKEY)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()

# Set interval and limit
INTERVAL = 15 * 60 # 15 minute interval
ntweets = 500
keywords = ["Sunset", "Sunrise", "Sunlight", "Dusk"]
antikeywords = ["Person", "Human"]

def search():
    counter = 0

    # API search query
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets' , lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):
        for media in tweet.entities.get("media",[{}]):
            if media.get("type",None) == "photo":

                # Access image
                img = getimage(tweet.entities["media"][0]["media_url_https"])
                
                # Increment image counter limit
                counter += 1

                if counter == 25:
                    counter == 0

                # Detect labels
                labels = define(img)
                confidence = 0

                for label in labels:
                    print(label["Name"], label["Confidence"])

                    if label["Name"] in keywords:
                        confidence = label["Confidence"]
                    elif label ["Name"] in antikeywords and label["Confidence"] > 70:
                        break
                
                # When detection confidence is sufficient
                if confidence > 60:
                    
                    # Retweet
                    try:
                        tweet.retweet()
                        print('Tweet Retweeted')
                    except tweepy.TweepError as e:
                        print(e.reason)
                    except StopIteration:
                        break

                    return True

                    # Download photo
                    # urllib.request.urlretrieve(imageurl, "images/%d.jpg" % counter)
                    # image = "images/%d.jpg" % counter

def define(image):
    client = boto3.client('rekognition')

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

while True:
    hit = search()
    if hit == True:
        time.sleep(INTERVAL)
