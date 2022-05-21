import tweepy
import config

def run(generated_tweets):
	api = set_up()
	for tweet in generated_tweets:
		if len(tweet) >= 15 and len(tweet) <= 280:
			api.update_status(tweet)
			break

def set_up():
	consumer_key = 'uCoW2hmwo7TebEuxUkYTX46x1'
	consumer_secret_key = '7EesIQ2Gzmdx6K8XmWJQ0pde4Z7bOx9oYPzFj8xhtCzrKyO5Tn'
	access_token = '1428945741758668801-NZcHXaob4X7vRl8H2lSWuapTH24N5D'
	access_token_secret = '3f8JEHGuwGPovFhEACXLxnJYBKILGo5tpaifOjsec2n8h'
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret_key)
	auth.set_access_token(config.access_token, config.access_token_secret)
	api = tweepy.API(auth)
	return api
