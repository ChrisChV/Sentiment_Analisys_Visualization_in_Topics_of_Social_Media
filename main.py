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


doc_a = u'Hola mundo este es el mensaje uno y dos por dos. Queremos'
doc_b = u'Adios mundo voy a ir a comer. Fin del mensaje 2.'
doc_c = u'La canción y el ratón están en la región y en la casa, :).'

doc_set = [doc_a, doc_b, doc_c]

print('Obteniendo Datos...')

doc_set = []
tweet_set = []
dic_user = {}
client = MongoClient('mongodb://twitter:twitter@cs.csunsa.win/twitter')
db = client['twitter']
collection = db['Rusia2018']
c = 0
for tweet in collection.find({},{"_id":1, "text":1,"user":1, "in_reply_to_user_id":1}):
	userId = tweet['user']['id']
	userIdConnec = tweet['in_reply_to_user_id']
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
#	if c == 500:
#		break

#for userId, user in dic_user.iteritems():
#	print(str(userId) + " " + str(len(user.tweet_set)))


print(str(c) + " tweets cargados")
print(str(len(dic_user)) + " usuarios cargados")


k_topics = 3
LDA_iterations = 500
sentimentPoints = getSentimentPoints()

dictionary, corpus, out_set = preprocessing(doc_set)

fileOut = open("out_dic", 'w')
print(dictionary, file = fileOut)
fileOut.close()

for i in range(0,len(out_set)):
	tweet_set[i].wordSet = out_set[i]


sentimentsOfTweets = getSentimentScoreOfTweets(out_set)

model = LDA(dictionary, corpus, k_topics, LDA_iterations)

#sentimentsOfTopics =  getSentimentsScoreOfTopics(out_set, model.get_topics(), dictionary)

print(sentimentsOfTweets)
#print(sentimentsOfTopics)

for i in range(0,len(sentimentsOfTweets)):
	tweet_set[i].russell_tuple = sentimentsOfTweets[i]

fileOut = open("out_model", 'w')
print (model.print_topics(num_topics=k_topics, num_words=10), file = fileOut)
fileOut.close()

#print(getStrOfSentiment(getPolaritySent(sentimentsOfTweets[0])))
#print(getStrOfSentiment(getPrimarySent(sentimentsOfTweets[0], sentimentPoints)))
	
sentDic = loadDict()

print("Evaluando...")

dictByTopic = []
tempDic = {}
topics = model.get_topics()


for topic in topics:
	tempDic = {}
	for i in range(0,len(topic)):
		tempDic[dictionary[i]] = topic[i]
	dictByTopic.append(tempDic)
	

for i in range(0,len(tweet_set)):
	print(str(i) + "/" + str(len(tweet_set)))
	tweet_set[i].polaritySent = getPolaritySent(tweet_set[i].russell_tuple)
	#tweet_set[i].characteristic_vector = getCharacteristicVector(tweet_set[i].russell_tuple, sentimentPoints)
	#tweet_set[i].primarySent = getPrimarySent(tweet_set[i].characteristic_vector)
	tweet_set[i].primarySent, tweet_set[i].characteristic_vector = getPrimarySent(tweet_set[i].russell_tuple, sentimentPoints)
	tweet_set[i].topic = getTopic(tweet_set[i].wordSet, model.get_topics(), dictionary, dictByTopic)
	tweet_set[i].russell_tuple_topic = getSentimentScore(tweet_set[i].wordSet, dictByTopic[tweet_set[i].topic], sentDic)
	tweet_set[i].topicSent, tweet_set[i].topic_characteristic_vector = getPrimarySent(tweet_set[i].russell_tuple_topic, sentimentPoints)
	#tweet_set[i].russell_tuple_topic = getSentimentsScoreOfTopics(tweet_set[i].wordSet, model.get_topics(), dictionary, tweet_set[i].topic, sentDic)


print("Guardando Tweets...")
saveTweets(tweet_set, "out_tweets")
saveUsers(dic_user, "out_users")
#updateTweets(tweet_set, collection)

print("End...")

for tweet in tweet_set:
	tweet.printClass()

sentimentsOfTopics = []
valoresPersonOfTopics = []
TweetInTopicCount = [0] * k_topics
UserInTopicCount = [0] * k_topics
for tweet in tweet_set:
	TweetInTopicCount[tweet.topic] += 1
for userId, user in dic_user.iteritems():
	UserInTopicCount[user.setPrincipalTopic(k_topics)] += 1

for i in range(0, k_topics):
	sentimentsOfTopics.append([])
for tweet in tweet_set:
	sentimentsOfTopics[tweet.topic].append(tweet.russell_tuple_topic)
for i in range(0,k_topics):
	valoresPersonOfTopics.append(person(sentimentsOfTopics[i]))


print(str(len(tweet_set)) + " " + str(len(dic_user)) + " " + str(person(sentimentsOfTweets)))
for i in range(0,k_topics):
	print(str(TweetInTopicCount[i]) + " " + str(UserInTopicCount[i]) + " " + str(valoresPersonOfTopics[i]))


generateGraph(dic_user, k_topics, "out_graph")
saveCharacteristicVectors(tweet_set, "out_chac")
for i in range(0, k_topics):
	saveTopicCharacteristicVectors(tweet_set, "out_chacTopic" + str(i), i)


