import markov

def run(count):
	markov.parseGen(['', 'parse', 'pol_tweets', '2', 'tweets.txt'])
	new_tweets = markov.parseGen(['', 'gen', 'pol_tweets', str(count)])
	print(new_tweets)
	return new_tweets