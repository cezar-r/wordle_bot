import tweepy
from auth import *

auth = tweepy.OAuthHandler(API, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def tweet(msg):
	"""This methods tweets a string"""
	api.update_status(msg)

def update_bio(description):
	"""This method updates the bio with a new string"""
	api.update_profile(description = description)