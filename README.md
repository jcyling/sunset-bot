# Perpetual Sunset
This bot looks for images of sunsets posted in Twitter and retweets them, every hour of the day. It started from the idea that there is always a sunset happening at any point in time. These images are showcased in a simple single-purpose website.

### Video
https://youtu.be/W0o_OXk5hXk

## What Is It?
Perpetual Sunset is a single-page web app that displays photos of sunsets by Twitter users. Tweepy is used to search for tweets with the keyword `sunset`. Each tweet image is passed to AWS image recognition service to evaluate the contents of the image. If the confidence level of the image containing a sunset is above 60%, the bot retweets the tweet. As well as recognizing sunsets, the bot is also configured to discard images with unwanted content (such as "person"). Valid images retweeted, saved in a S3 bucket, and displayed on the web app, as well as their tweet time and user location. The site is responsively designed. All hours are based in GMT+0.

## How It Works
This site is deployed on Heroku, connects to the Twitter API to get information. This information is sent to a Postgres database as well as a S3 bucket to host photos.

#### Database
The database contains information on the tweet time, user location, tweet content, and S3 image link. It is indexed by the hour of tweet retrieval by this bot. Therefore if the hour of retrieval is 3:00, the tweet is indexed at `ID: 3`. For the purposes of hosting this site on Heroku, a Heroku Postgres database add-on is used here.

#### Scripts
`bot.py` contains logic for the twitter bot and associated functions.
`app.py` contains the route for the flask app and retrieval of tweet information from the database.

#### Functions in bot.py
`search()` uses the `tweepy` library to conduct a Twitter search based on keywords. It stores the associated information of a tweet, such as time, image, and user location in the database. The Twitter API returns a list of tweets from which we use to define labels.
`define(image)` uses the AWS Rekognition service to define what the image contains. For the ease of use, it prints out a list of the labels detected in the image to the console. When inappropriate labels are detected, the function discords the current tweet.
`getimage(imageurl)` fetches the image contents.
`uploadimage(imageurl)` as titled, uploads the image into a S3 bucket.
`gethour()` gets the current hour in GMT+0.
`retweet()` contains Twitter interactions and passes information to update the datebase.
`updateDb()` sends a query to Postgres to update information from the tweet, indexed by the hour tweeted. The query is set to only update data when an existing `ID` is found. 
`start()` initiates the search and continues the search until there is a valid hit, after which, a sleep function kicks in.

## How to Run
To run this project, Twitter developer and AWS security credentials are needed - here they have been stored in the Heroku environment vars. To run locally they can be stored in a `dotenv` or whichever method you choose.