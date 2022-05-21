import os
import pandas as pd

def run(users, max_results):
	try:
		os.remove('tweets.json')
	except:
		pass
	for i in range(len(users)):
		print('['+str(i+1)+'/'+str(len(users))+'] Fetching '+users[i]+'\'s tweets...')
		os.system("snscrape --jsonl --max-results "+str(max_results)+" twitter-search 'from:"+users[i]+"'>> tweets.json")

	tweets_df = pd.read_json('tweets.json', lines=True)
	tweets_list = tweets_df.content.tolist()

	with open('tweets.txt', 'w', encoding="utf-8") as  text_file_1:
		for item in tweets_list:
			if 'https://t.co/' in item:
				item = item[0:item.index('https://t.co/')]
			text_file_1.write('%s\n' % item.replace('&amp;','&'))