import markov
import language_tool_python

def run(count):
	markov.parseGen(['', 'parse', 'pol_tweets', '2', 'tweets.txt'])
	new_tweets = markov.parseGen(['', 'gen', 'pol_tweets', str(count)])

	tool = language_tool_python.LanguageTool('en-US')
	for i in range(len(new_tweets)):
		new_tweets[i] = tool.correct(new_tweets[i])

	print(new_tweets)
	return new_tweets