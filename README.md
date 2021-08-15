# Sunset Bot
This bot looks for images of sunsets posted in Twitter and retweets them. These images are showcased in a simple single-purpose website.

### Video
- [ ] To do

### How It Works In Brief
Tweepy is used to search for tweets with the keyword `sunset`. Each tweet image is passed to AWS Rekognition service to evaluate the contents of the image. If the confidence level is above 60%, the bot retweets the tweet. As well as recognizing sunsets, the bot is also configured to discard images with unwanted content. Valid images are saved and displayed in a gallery.

### Libraries Used
Flask, boto3, tweepy, urllib.

### APIs
Configure API keys as environment variables for deployment in Heroku.
- Twitter
- AWS Rekognition

### Structure

