import markov
import language_tool_python

def run_markov(count):
	markov.parseGen(['', 'parse', 'pol_tweets', '2', 'tweets.txt'])
	new_tweets = markov.parseGen(['', 'gen', 'pol_tweets', str(count)])

	tool = language_tool_python.LanguageTool('en-US')
	for i in range(len(new_tweets)):
		new_tweets[i] = tool.correct(new_tweets[i])

	print(new_tweets)
	return new_tweets

import requests
import random
import config

def random_line(afile):
	lines = open(afile).read().splitlines()
	myline = random.choice(lines)
	return myline

def run(count):
	base_string = ''
	while len(base_string)<30:
		base_string=random_line('tweets.txt')

	r = requests.post("https://api.deepai.org/api/text-generator", data={'text': base_string}, headers={'api-key': config.deepai_key})
	new_tweet = r.json().get('output').replace(base_string,'')

	print(new_tweet)
	return [new_tweet[0:280]] if len(new_tweet)>280 else [new_tweet]
