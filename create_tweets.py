import markov
import language_tool_python

def fix_grammar(new_tweets):
	tool = language_tool_python.LanguageTool('en-US')
	for i in range(len(new_tweets)):
		new_tweets[i] = tool.correct(new_tweets[i])
	return new_tweets

def run_markov(count):
	markov.parseGen(['', 'parse', 'pol_tweets', '2', 'tweets.txt'])
	new_tweets = markov.parseGen(['', 'gen', 'pol_tweets', str(count)])

	new_tweets = fix_grammar(new_tweets)
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
	new_tweet = r.json().get('output').replace(base_string,'').replace('\\xa0','')
	new_tweet = new_tweet[0:280] if len(new_tweet)>280 else new_tweet
	new_tweet = new_tweet[0:new_tweet.rfind('.')+1]

	new_tweet = fix_grammar([new_tweet])[0]
	print(new_tweet)
	return [new_tweet]
