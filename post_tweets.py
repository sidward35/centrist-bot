import tweepy
import config

def run(generated_tweets):
	api = set_up()
	for tweet in generated_tweets:
		if len(tweet) >= 15 and len(tweet) <= 280:
			api.update_status(tweet)
			break

def set_up():
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret_key)
	auth.set_access_token(config.access_token, config.access_token_secret)
	api = tweepy.API(auth)
	return api
