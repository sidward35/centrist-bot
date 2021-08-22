import fetch_tweets, create_tweets, post_tweets

users = ['tedcruz', 'marcorubio', 'johncornyn', 'senjoniernst', 'repdancrenshaw', 'edmarkey','dickdurbin', 'senatorshaheen', 'chrismurphyct', 'corybooker']
max_results = 25 # max tweets to fetch from a single user

unique_words = fetch_tweets.run(users, max_results) # get politicians' tweets from usernames above
new_tweets = create_tweets.run(unique_words) # generate new tweets from politicians' tweets
#post_tweets.run(new_tweets) # post generated tweets to Twitter
