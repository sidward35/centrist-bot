import random
import nltk
nltk.download('averaged_perceptron_tagger')

def run(words):
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
	sentence_template_options = [['PRP', 'VB', 'PRP$', 'JJ', 'JJ', 'NNS', 'IN', 'VB', 'NNP']]
	sentence_template = sentence_template_options[random.randint(0,len(sentence_template_options)-1)]
	tweet = ""
	for i in sentence_template:
		tweet+=pos_dict[i][random.randint(0,len(pos_dict[i])-1)] + " "
	print(tweet)
	return tweet

def tokenize(word):
	tokens = nltk.word_tokenize(word)
	tagged = nltk.pos_tag(tokens)
	return tagged
