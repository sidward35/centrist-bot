import os
import pandas as pd
import string

def run(users, max_results):
	for i in range(len(users)):
		print('['+str(i+1)+'/'+str(len(users))+'] Fetching '+users[i]+'\'s tweets...')
		os.system("snscrape --jsonl --max-results "+str(max_results)+" twitter-search 'from:"+users[i]+"'>> tweets.json")

	tweets_df = pd.read_json('tweets.json', lines=True)
	os.remove('tweets.json')
	tweets_list = tweets_df.content.tolist()
	tweets_string = "".join(tweets_list)
	tweets_words_list = tweets_string.split(' ')
	tweets_words_list = list(set(tweets_words_list))

	tweets_unique_words = []
	for item in tweets_words_list:
		item = item.strip().lower().replace('&amp;','&')
		item = item.translate(str.maketrans('', '', string.punctuation))
		if not 'https' in item and not item in tweets_unique_words:
			tweets_unique_words.append(item)

	return tweets_unique_words