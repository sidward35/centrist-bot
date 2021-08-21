import tweepy

def run(generated_tweets):
	api = set_up()
	for tweet in generated_tweets:
		api.update_status(tweet)
		# post to Twitter

def set_up():
	consumer_key = 'XXXX'
	consumer_secret_key = 'XXXX'
	access_token = 'XXXX'
	access_token_secret = 'XXXX'
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api
