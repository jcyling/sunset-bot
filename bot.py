import tweepy
import urllib.request
import boto3
import requests
import psycopg2
import sys
from os import path, environ
from pathlib import Path

try: 
    AKEY = environ.get('AKEY')
    ASKEY = environ.get('ASKEY')
    ATKEY = environ.get('ATKEY')
    ATSKEY = environ.get('ATSKEY')
except KeyError:
    print("Keys not accessible.")
    sys.exit(1)
    
# Authentication
auth = tweepy.OAuthHandler(AKEY, ASKEY)
auth.set_access_token(ATKEY, ATSKEY)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()

# Database connection
# db = sqlite3.connect('sunsets.db', check_same_thread=False)
# cur = db.cursor()
db = environ.get("DATABASE_URI")
conn = psycopg2.connect("DATABASE_URI")
cur = conn.cursor()

# Set interval and limit
ntweets = 500
keywords = ["Sunset", "Sunrise", "Sunlight", "Dusk"]
antikeywords = ["Person", "Human"]
counter = 0

def search():
    # API search query
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets', lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):

        for media in tweet.entities.get("media",[{}]):
            if media.get("type",None) == "photo":

                # Access image
                imageurl = tweet.entities["media"][0]["media_url_https"]
                image = getimage(imageurl)
                
                # Detect labels
                confidence = define(image)

                # When detection confidence is sufficient
                if confidence > 60:
                    try:
                        # Retweet
                        tweet.retweet()
                        tweetimage = downloadimage(imageurl)
                        
                        loc = tweet.user.location
                        tweettime = tweet.created_at
                        tweettext = tweet.text

                        # Update database
                        cur.execute("UPDATE tweets SET location = ?, time = ?, text = ? WHERE image = ?", 
                        (loc, tweettime, tweettext, tweetimage))

                        # Insert into database
                        # cur.execute("INSERT INTO tweets (location, time, text, image) VALUES (?, ?, ?, ?)",
                        # (loc, tweettime, tweettext, tweetimage))

                        print(loc, tweettime, tweettext)
                        print('Tweet Retweeted')
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
    labels = results["Labels"]

    confidence = 0

    for label in labels:
        print(label["Name"], label["Confidence"])

        if label["Name"] in keywords:
            confidence = label["Confidence"]
        elif label ["Name"] in antikeywords and label["Confidence"] > 60:
            print("Image not appropriate.")
            return False
    return confidence

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
    images = loadimage()
    lastfile = images[len(images) - 1]
    name = path.basename(lastfile)

    urllib.request.urlretrieve(imageurl, "static/images/%s" % name)
    image = "static/images/%s" % name
    return image

# Search for tweets until there is a hit
def start():
    while True:
        hit = search()
        if hit == True:
            # Close database connection
            db.commit()
            db.close()
            
            # Confirm hit
            return True

if __name__ == "__main__":
    start()
    images = loadimage()