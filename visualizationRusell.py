#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from preprocessing import *
from LDA import * 
from pymongo import MongoClient
from rusell import *
from evaluation import * 
from TweetClass import *
from network import * 
from pymongo import MongoClient
from twython import Twython
from urlparse import urlparse
import sys
import json
import pymongo

IP_MONGO_SERVER = "172.16.5.59"

def generateJson(tweet_set, fileName):
	outFile = open(fileName, 'w')
	outFile.write('[')
	actual = 0
	for tweet in tweet_set:
		outFile.write('{' + '\n')
		outFile.write("\"x\":" + str(tweet.russell_tuple[0]) + ',\n')
		outFile.write("\"y\":" + str(tweet.russell_tuple[1]) + ',\n')
		outFile.write("\"text\":\"" + tweet.originalTweet.replace('\n',' ').replace('\"', ' ').encode("utf-8") + '\",\n')
		outFile.write("\"sentiment\":\"" + getStrOfSentiment(tweet.primarySent) + '\",\n')
		outFile.write("\"userId\":\"" + str(tweet.usuario.userId) + '\"\n')
		outFile.write('}')
		if(actual != len(tweet_set) - 1):
			outFile.write(',')
		outFile.write('\n')
		actual += 1
	outFile.write(']')
	outFile.close()

def getTweets(hashtag):

	client = MongoClient('mongodb://twitter:twitter@' + IP_MONGO_SERVER + '/twitter')

	db = client['twitter']
	collection = db[hashtag+"tmp"]

	APP_KEY = '8iuErv802dm1q9YQnOrtrcgIG'
	APP_SECRET = 'dMnTqnQvUwOk0foTcSl0yDp8MDThsgdsgAD0W5Ox6qrOw3QnsY'

	twitter = Twython(APP_KEY, APP_SECRET)

	auth = twitter.get_authentication_tokens()

	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

	try:
	    results = twitter.search(q=hashtag,lang='es',count='100')

	except TwythonError as e:
	    print(e) 

	for tweet in results['statuses']:
	    print('Usuario @%s Fecha: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['created_at']))
	    ultimo = tweet
	    print('Geo: ' + tweet['user']['location'])
	    print('Contenido: ' + tweet['text'].encode('utf-8'), '\n\n')
	    collection.insert(tweet)

hashtag = sys.argv[1]
num_tweets = int(sys.argv[2])
num_topics = int(sys.argv[3])
num_iterations = int(sys.argv[4])

getTweets(hashtag)

doc_set = []
tweet_set = []
dic_user = {}
client = MongoClient('mongodb://twitter:twitter@172.16.5.59/twitter')
db = client['twitter']
collection = db[hashtag+"tmp"]
c = 0
#for tweet in collection.find({},{"_id":1, "text":1,"user":1, "in_reply_to_user_id":1}):
for tweet in collection.find({},{"_id":1, "text":1,"user":1, "retweeted_status":1}):
	userId = tweet['user']['id']
	#userIdConnec = tweet['in_reply_to_user_id']
	if('retweeted_status' in tweet):
		userIdConnec = tweet['retweeted_status']['id']
	else:
		userIdConnec = False

	if not(userId in dic_user):
		dic_user[userId] = UserClass(userId)
	if(userIdConnec):
		#print("AAAAAAAAAAAA")
		if not(userIdConnec in dic_user):
			dic_user[userIdConnec] = UserClass(userIdConnec)
		dic_user[userId].addUser(dic_user[userIdConnec])
	doc_set.append(tweet['text'])
	tweet_set.append(TweetClass(tweet['text'], dic_user[userId]))
	tweet_set[len(tweet_set) - 1].tweetId = tweet['_id']
	dic_user[userId].addTweet(tweet_set[len(tweet_set) - 1])

	c += 1
	if c == num_tweets:
		break

#for userId, user in dic_user.iteritems():
#	print(str(userId) + " " + str(len(user.tweet_set)))

k_topics = num_topics
LDA_iterations = num_iterations
sentimentPoints = getSentimentPoints()
print(sentimentPoints)

dictionary, corpus, out_set = preprocessing(doc_set)

for i in range(0,len(out_set)):
	tweet_set[i].wordSet = out_set[i]

sentimentsOfTweets = getSentimentScoreOfTweets(out_set)
model = LDA(dictionary, corpus, k_topics, LDA_iterations)

for i in range(0,len(sentimentsOfTweets)):
	tweet_set[i].russell_tuple = sentimentsOfTweets[i]

sentDic = loadDict()

dictByTopic = []
tempDic = {}
topics = model.get_topics()

for topic in topics:
	tempDic = {}
	for i in range(0,len(topic)):
		tempDic[dictionary[i]] = topic[i]
	dictByTopic.append(tempDic)

for i in range(0,len(tweet_set)):
	tweet_set[i].polaritySent = getPolaritySent(tweet_set[i].russell_tuple)
	tweet_set[i].primarySent, tweet_set[i].characteristic_vector = getPrimarySent(tweet_set[i].russell_tuple, sentimentPoints)

generateJson(tweet_set, "russell_sents.json")

sys.exit(1)