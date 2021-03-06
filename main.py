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

IP_MONGO_SERVER = "192.168.1.13"


doc_a = u'Hola mundo este es el mensaje uno y dos por dos. Queremos'
doc_b = u'Adios mundo voy a ir a comer. Fin del mensaje 2.'
doc_c = u'La canción y el ratón están en la región y en la casa, :).'

doc_set = [doc_a, doc_b, doc_c]

print('Obteniendo Datos...')

doc_set = []
tweet_set = []
dic_user = {}
client = MongoClient('mongodb://twitter:twitter@' + IP_MONGO_SERVER + '/twitter')
db = client['twitter']
collection = db['FinalRusia2018']
c = 0
#for tweet in collection.find({},{"_id":1, "text":1,"user":1, "in_reply_to_user_id":1}):
for tweet in collection.find({},{"_id":1, "text":1,"user":1, "retweeted_status":1}):
	userId = str(tweet['user']['id'])
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
#saveUsers(dic_user, "out_users")
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


sentAssorFilr = open("out_sentAssort.csv", 'w')
print(",#tweets,#usuarios,Sentiment Assortativity", file=sentAssorFilr)
print("Conversación principal," + str(len(tweet_set)) + "," + str(len(dic_user)) + "," + str(person(sentimentsOfTweets)), file=sentAssorFilr)	
for i in range(0,k_topics):
	print("Topico " + str(i+1) + "," + str(TweetInTopicCount[i]) + "," + str(UserInTopicCount[i]) + "," + str(valoresPersonOfTopics[i]), file=sentAssorFilr)

sentAssorFilr.close()

generateGraph(dic_user, k_topics, "out_graph")
saveCharacteristicVectors(tweet_set, "out_chac.data")
saveRussellTuples(tweet_set, "out_rusell")
for i in range(0, k_topics):
	saveTopicCharacteristicVectors(tweet_set, "out_chacTopic" + str(i) + ".data", i)
	saveRusellTuplesTopic(tweet_set, "out_rusellTopic" + str(i), i)	


userDicCom, communitiesDic = loadUserCommunities("userCommunities")
user_community_set = getUserCommunitySet(userDicCom, dic_user)
#shannonFile = open("out_shannon", 'w')
polaritySE = []
principalSE = []
topicSE = []
numOfUsersInTopicsSE = []
for communityId, temp in user_community_set.iteritems():
	polarityShanonEntropy, principalShanonEntropy, topicShanonEntropy, numOfUsersInTopics = getShanonEntropy(user_community_set, communityId, k_topics)
	polaritySE.append(polarityShanonEntropy)
	principalSE.append(principalShanonEntropy)
	topicSE.append(topicShanonEntropy)
	numOfUsersInTopicsSE.append(numOfUsersInTopics)
	#print(communityId, file=shannonFile)
	#print(polarityShanonEntropy, file=shannonFile)
	#print(principalShanonEntropy, file=shannonFile)
	#print(topicShanonEntropy, file=shannonFile)

shannonFile = open("out_shannon.csv",'w')
shannonFile.write('Comm,')
for i in range(1,16):
	shannonFile.write(str(i))
	if(i != 15):
		shannonFile.write(',')
	else:
		shannonFile.write('\n')
shannonFile.write('Polarity,')
#for i in range(0,15):
i = 0
for communityId, temp  in user_community_set.iteritems():
	val = polaritySE[i]
	shannonFile.write(str(val) + " (" + str(len(temp)) + ")")
	if(i != 14):
		shannonFile.write(',')
	else:
		shannonFile.write('\n')
	i += 1
shannonFile.write('PrimarySent,')
i = 0
#for i in range(0,15):
for communityId, temp  in user_community_set.iteritems():
	val = principalSE[i]
	shannonFile.write(str(val) + " (" + str(len(temp)) + ")")
	if(i != 14):
		shannonFile.write(',')
	else:
		shannonFile.write('\n')
	i += 1
iVal = 0

for i in range(0, k_topics):
	shannonFile.write("Topic " + str(i + 1) + ",")
	j = 0
	for communityId, temp  in user_community_set.iteritems():
		shannonFile.write(str(topicSE[j][i]) + " (" + str(int(numOfUsersInTopicsSE[j][i])) + ")")
		if(j != 14):
			shannonFile.write(',')
		else:
			shannonFile.write('\n')
		j += 1
shannonFile.close()







