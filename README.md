# Sunset Bot
This bot looks for images of sunsets posted in Twitter and retweets them. These images are showcased in a simple single-purpose website.

### Video
- [ ] To do

## What Is It?
Sunset Bot is a single-page web app that displays photos of sunsets by Twitter users. Tweepy is used to search for tweets with the keyword `sunset`. Each tweet image is passed to AWS Rekognition service to evaluate the contents of the image. If the confidence level of the image containing a sunset is above 60%, the bot retweets the tweet. As well as recognizing sunsets, the bot is also configured to discard images with unwanted content. Valid images are saved and displayed on the gallery, as well as their tweet time and user location.

## How It Works
The python script uses Twitter API to obtain relevant images. The image is saved and the 
`bot.py` contains logic for the twitter bot and associated functions.
`app.py` contains routes for the flask app.
`index.js` has a minimal Javascript fading effect applied on images.

#### Functions in bot.py
`search()` uses the `tweepy` library to conduct a Twitter search based on keywords.
`define(image)` uses the AWS services to upload an image attached to tweets and define them using AWS AI.
`loadimage()`
`getimage(imageurl)`
`downloadimage(imageurl)`
`start()` initiates the search and continues the search until there is a valid hit.

#### Libraries Used
Tweepy, flask, boto3, urllib, sqlite3, pathlib, requests, jQuery

## How to Run 
### Locally
Input your environment variables in `config.env`. Type the following into terminal to set the `.env` file source. Use `flask run` to initate the app locally.
```
set -a
source config.env
set +a
flask run
```

### On Heroku
Obtain on Twitter and AWS your unique API keys and configure them as environment variables for deployment individually.
