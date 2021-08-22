import nltk
import random

def run(words, count):
	pos_dict = {}
	for word in words:
		tag = tokenize(word)
		for i in range(len(tag)):
			value = tag[i][0]
			key = tag[i][1]
			if key not in pos_dict:
				pos_dict[key] = [value]
			else:
				list = pos_dict[key]
				list.append(value)
				pos_dict[key] = list
	sentence_template = ["NN", "VB", "NN"]
	tweet = ""
	for i in sentence_template:
		tweet+=pos_dict[i][random.randint(0,len(pos_dict[i])-1)] + " "
	print(tweet)
	new_tweets = ['']
	return new_tweets

def tokenize(word):
	tokens = nltk.word_tokenize(word)
	tagged = nltk.pos_tag(tokens)
	return tagged
