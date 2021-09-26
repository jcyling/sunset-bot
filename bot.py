import tweepy
import urllib.request
import boto3
import requests
import glob
from os import path, environ
from pathlib import Path

from credentials import *

# try: 
#     AKEY = environ['AKEY']
#     ASKEY = environ['ASKEY']
#     ATKEY = environ['ATKEY']
#     ATSKEY = environ['ATSKEY']
# except KeyError:
#     print("Keys not accessible.")
#     sys.exit(1)
    
# Authentication
auth = tweepy.OAuthHandler(AKEY, ASKEY)
auth.set_access_token(ATKEY, ATSKEY)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()

# Set interval and limit
ntweets = 500
keywords = ["Sunset", "Sunrise", "Sunlight", "Dusk"]
antikeywords = ["Person", "Human"]
counter = 0
locations = []

def search():
    # API search query
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets', lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):
        ## print(json.dumps(tweet._json, indent = 2))

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
                    try:
                        # Retweet
                        tweet.retweet()
                        print('Tweet Retweeted')

                        downloadimage(imageurl)
                        return True
                    
                    except tweepy.TweepError as e:
                        pass
                    except StopIteration:
                        pass

# Define image with AWS
def define(image):
    client = boto3.client('rekognition', region_name='us-east-2')
    results = client.detect_labels(
        Image={
            'Bytes': image
            }
        )
    return results["Labels"]

# Get photo bytes
def getimage(imageurl):
    response = requests.get(imageurl)
    imagebytes = response.content
    return imagebytes

# Load images in static
def loadimage():
    images = sorted(Path("static/images/").iterdir(), key=path.getmtime, reverse=True)
    return images

# Download photo
def downloadimage(imageurl):
    # Implement replace last modified file
    images = loadimage()
    lastfile = images[len(images) - 1]
    name = path.basename(lastfile)

    urllib.request.urlretrieve(imageurl, "static/images/%s" % name)
    image = "static/images/%s" % name

# Search for tweets until there is a hit
def start():
    while True:
        hit = search()
        if hit == True:
            return True

if __name__ == "__main__":
    start()
    images = loadimage()