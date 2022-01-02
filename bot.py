import tweepy
import boto3
import requests
import psycopg2
import sys
import datetime
import time
from pytz import timezone
from dotenv import load_dotenv
from os import path, environ

dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

try: 
    AKEY = environ.get('AKEY')
    ASKEY = environ.get('ASKEY')
    ATKEY = environ.get('ATKEY')
    ATSKEY = environ.get('ATSKEY')
    AWSID = environ.get('AWSID')
    AWSSID = environ.get('AWSSID')
    db = environ.get("DATABASE_URL")
except KeyError:
    print("Config not accessible.")
    sys.exit(1)
    
# Authentication
auth = tweepy.OAuthHandler(AKEY, ASKEY)
auth.set_access_token(ATKEY, ATSKEY)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()

# Set interval and limit
ntweets = 500
keywords = ["Sunset", "Sunrise", "Sunlight", "Dusk"]
antikeywords = ["Person", "Human"]

# Search for keyword tweets
def search():
    searchResults = tweepy.Cursor(api.search, q='sunset OR sunsets -filter:retweets', lang="en", include_entities=True)

    for tweet in searchResults.items(ntweets):
        for media in tweet.entities.get("media",[{}]):
            if media.get("type",None) == "photo":
                imageurl = tweet.entities["media"][0]["media_url_https"]
                image = getimagebytes(imageurl)
                confidence = define(image)

                # When detection confidence is sufficient
                if confidence > 60:
                    try:
                        retweet(tweet, imageurl)

                        return True

                    except tweepy.TweepError as e:
                        pass
                    except StopIteration:
                        pass

# Twitter interaction and update database
def retweet(tweet, imageurl):
    tweet.retweet()
    tweetimage = uploadimage(imageurl)
    tweetloc = tweet.user.location
    tweettime = tweet.created_at
    tweettext = tweet.text

    # Update database
    updateDb(tweetloc, tweettime, tweettext, tweetimage)
    print(tweetloc, tweettime, tweettext)

# Database update
def updateDb(tweetloc, tweettime, tweettext, tweetimage):
    try:
        hour = gethour()
        conn = psycopg2.connect(db)
        cur = conn.cursor()
        query = '''
            INSERT INTO tweets (id, location, time, text, image)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
            (location, time, text, image) = (EXCLUDED.location, EXCLUDED.time, EXCLUDED.text, EXCLUDED.image)
        '''
        cur.execute(query, (hour, tweetloc, tweettime, tweettext, tweetimage))
        conn.commit()
        conn.close()
    except:
        print("Error updating DB")
        sys.exit()
    
# Define image with AWS
def define(image):
    client = boto3.client('rekognition',
            aws_access_key_id=AWSID,
            aws_secret_access_key=AWSSID,
            region_name='us-east-2')
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

# Get hour of day(GMT)
def gethour():
    london = timezone('Europe/London')
    date = datetime.datetime.now(london)
    hour = date.hour
    return hour

# Get image bytes
def getimagebytes(imageurl):
    response = requests.get(imageurl)
    imagebytes = response.content
    return imagebytes

# Upload image for current hour
def uploadimage(imageurl):
    hour = gethour()
    r = requests.get(imageurl, stream=True)

    # S3 connection
    session = boto3.Session()
    s3 = session.resource("s3")
    bucket_name = "permanent-sunset"
    filename = "%s.jpg" % hour
    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(r.raw, filename)
    imagepath = "https://%s.s3.us-east-2.amazonaws.com/%s" % (bucket_name, filename)
    return imagepath

# Search for tweets until there is a hit
def start():
    while True:
        hit = search()
        time.sleep(10)

if __name__ == "__main__":
    start()