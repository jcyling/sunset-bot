# Sunset Bot

This bot looks for images of sunsets posted in Twitter and retweets them.

# How It Works
Tweepy is used to search for tweets. Each tweet image is passed to AWS Rekognition service to evaluate the contents of the image. If the confidence level is above 60%, the bot retweets the tweet. As well as recognizing sunsets, the bot is also configured to discard images with unwanted content.
