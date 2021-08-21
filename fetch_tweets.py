import requests
import time
import json
import os
import pandas as pd

users = ['tedcruz', 'marcorubio', 'johncornyn', 'senjoniernst', 'repdancrenshaw', 'edmarkey','dickdurbin', 'senatorshaheen', 'chrismurphyct', 'corybooker']

for i in range(len(users)):
	os.system("snscrape --jsonl --max-results 1000 twitter-search 'from:"+users[i]+"'>> tweets.json")

tweets_df = pd.read_json('tweets.json', lines=True)
print(tweets_df)