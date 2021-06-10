import tweepy
import time
from os import environ
from replit import db
from keep_alive import keep_alive

consumer_key = environ['consumer_key']
consumer_secret = environ['consumer_secret']
access_key = environ['access_key']
access_secret = environ['access_secret']
keep_alive()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def reply_to_tweets():
	last_seen_id = db['value']
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
	for mention in reversed(mentions):
		db['value'] = mention.id
		text = mention.full_text.lower()
		if '#scrap' in text:

			original_id = mention.in_reply_to_status_id
			tweet = api.get_status(original_id, tweet_mode='extended')
			a = tweet.full_text
			recipient_name = mention.user.screen_name
			user = api.get_user(recipient_name)
			id = user.id_str
			api.send_direct_message(id, a)
while True:
	reply_to_tweets()
	time.sleep(15)
