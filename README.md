# Sunset Bot
This bot looks for images of sunsets posted in Twitter and retweets them. These images are showcased in a simple single-purpose website.

### Video
https://youtu.be/W0o_OXk5hXk

## What Is It?
Sunset Bot is a single-page web app that displays photos of sunsets by Twitter users. Tweepy is used to search for tweets with the keyword `sunset`. Each tweet image is passed to AWS to evaluate the contents of the image. If the confidence level of the image containing a sunset is above 60%, the bot retweets the tweet. As well as recognizing sunsets, the bot is also configured to discard images with unwanted content. Valid images are saved and displayed on the gallery, as well as their tweet time and user location.

## How It Works
This site is hosted on Heroku, connects to the Twitter API to get information and  sends it to a Postgresql database as well as a S3 bucket to host photos.

#### Scripts
`bot.py` contains logic for the twitter bot and associated functions.
`app.py` contains routes for the flask app.

#### Functions in bot.py
`search()` uses the `tweepy` library to conduct a Twitter search based on keywords. It stores the associated information of a tweet, such as time, image, and user location in the database.
`define(image)` uses the AWS Rekognition service to define what the image contains.
`getimage(imageurl)` fetches the image contents.
`uploadimage(imageurl)` as titled, uploads the image into a S3 bucket.
`gethour()` gets the current hour in GMT.
`retweet()` contains Twitter interactions.
`updateDb()` sends a query to Postgres to update information from the tweet, indexed by the hour tweeted.
`start()` initiates the search and continues the search until there is a valid hit.

## How to Run 
Input security credentials for Twitter and AWS as environment variables.