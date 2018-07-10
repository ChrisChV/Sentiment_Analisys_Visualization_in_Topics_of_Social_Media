#!/usr/bin/env python
# -*- coding: utf-8 -*-
from preprocessing import *
from LDA import * 
from pymongo import MongoClient
from rusell import *
from evaluation import * 
from TweetClass import *

doc_a = u'Hola mundo este es el mensaje uno y dos por dos. Queremos'
doc_b = u'Adios mundo voy a ir a comer. Fin del mensaje 2.'
doc_c = u'La canción y el ratón están en la región y en la casa, :).'

doc_set = [doc_a, doc_b, doc_c]

print('Obteniendo Datos...')

doc_set = []
tweet_set = []
client = MongoClient('mongodb://twitter:twitter@10.42.0.1/twitter')
db = client['twitter']
collection = db['Rusia2018']
c = 0
for tweet in collection.find({},{"text":1}):
	doc_set.append(tweet['text'])
	tweet_set.append(TweetClass(tweet['text']))
	c += 1
	if c == 100:
		break


k_topics = 3
LDA_iterations = 100
sentimentPoints = getSentimentPoints()

dictionary, corpus, out_set = preprocessing(doc_set)

for i in range(0,len(out_set)):
	tweet_set[i].wordSet = out_set[i]


sentimentsOfTweets = getSentimentScoreOfTweets(out_set)

model = LDA(dictionary, corpus, k_topics, LDA_iterations)

sentimentsOfTopics =  getSentimentsScoreOfTopics(out_set, model.get_topics(), dictionary)

print(sentimentsOfTweets)
print(sentimentsOfTopics)

for i in range(0,len(sentimentsOfTweets)):
	tweet_set[i].russell_tuple = sentimentsOfTweets[i]


print (model.print_topics(num_topics=k_topics, num_words=3))

print(getStrOfSentiment(getPolaritySent(sentimentsOfTweets[0])))
print(getStrOfSentiment(getPrimarySent(sentimentsOfTweets[0], sentimentPoints)))

for i in range(0,len(tweet_set)):
	tweet_set[i].polaritySent = getPolaritySent(tweet_set[i].russell_tuple)
	tweet_set[i].primarySent = getPrimarySent(tweet_set[i].russell_tuple, sentimentPoints)

for tweet in tweet_set:
	tweet.printClass()

print(person(sentimentsOfTweets))
