import tweepy

def run(generated_tweets):
	api = set_up()
	for tweet in generated_tweets:
		api.update_status(tweet)

def set_up():
	consumer_key = '{KEY}'
	consumer_secret_key = '{SECRET}'
	access_token = '{KEY}'
	access_token_secret = '{SECRET}'
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api
