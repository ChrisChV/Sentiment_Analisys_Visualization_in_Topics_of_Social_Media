from __future__ import print_function
from sentiments import *

class UserClass:
 	userId = ""
	tweet_set = []
	users_connections = []
	principal_topic = 0

	def __init__(self, userId):
		self.userId = userId
		self.tweet_set = []
		self.users_connections = []
		self.principal_topic = 0

	def addTweet(self, tweet):
		self.tweet_set.append(tweet)
	def addUser(self, user):
		self.users_connections.append(user)
	def setPrincipalTopic(self, numOfTopics):
		count = [0] * numOfTopics
		for tweet in self.tweet_set:
			count[tweet.topic] += 1
		i_max = -1
		val_max = -1
		for i in range(0,numOfTopics):
			if(i_max == -1 or val_max < count[i]):
				i_max = i
				val_max = count[i]
		self.principal_topic = i_max
		return i_max
	def saveClass(self, outFile):
		print(self.userId, file=outFile)
		print(len(self.users_connections), file=outFile)
		for user_con in self.users_connections:
			print(user_con.userId , file=outFile)
		print(self.principal_topic, file=outFile)

class TweetClass:
	#def __init__(self, originalTweet):
	#	self.originalTweet = originalTweet
	def __init__(self, originalTweet, user):
		self.originalTweet = originalTweet
		self.usuario = user
		self.wordSet = []
		self.russell_tuple = []
		self.russell_tuple_topic = []
		self.characteristic_vector = []
		self.topic_characteristic_vector = []
		self.polaritySent = 0
		self.primarySent = 0
		self.topicSent = 0
		self.topic = 0
		self.tweetId = ""


	def printClass(self):
		print(self.originalTweet)
		print(self.wordSet)
		print(self.russell_tuple)
		print(self.russell_tuple_topic)
		print(self.topic)
		print(getStrOfSentiment(self.polaritySent))
		print(getStrOfSentiment(self.primarySent))
		print(self.characteristic_vector)

		print

	def saveClass(self, outFile):
		#print(self.originalTweet, file=outFile)
		print(self.usuario.userId, file=outFile)
		print(self.wordSet, file=outFile)
		print(self.russell_tuple, file=outFile)
		print(self.russell_tuple_topic, file=outFile)
		print(self.polaritySent, file=outFile)
		print(self.primarySent, file=outFile)
		print(self.topic, file=outFile)

	def updateTweet(self, collection):
		collection.update_one({'_id': self.tweetId}, {'$set': {'sentiment': self.primarySent}})

	def saveVector(self, outFile):
		outFile.write(str(self.tweetId) + getStrOfSentiment(self.primarySent) + ';')
		for i in range(0, len(self.characteristic_vector)):
			if(i != len(self.characteristic_vector) - 1):
				outFile.write(str(i) + ":" + str(self.characteristic_vector[i]) + ";")
			else:
				outFile.write(str(i) + ":" + str(self.characteristic_vector[i]) + ";0.0\n")

	def saveVectorTopic(self, outFile):
		outFile.write(str(self.tweetId) + getStrOfSentiment(self.topicSent) + ';')
		for i in range(0, len(self.topic_characteristic_vector)):
			if(i != len(self.topic_characteristic_vector) - 1):
				outFile.write(str(i) + ":" + str(self.topic_characteristic_vector[i]) + ";")
			else:
				outFile.write(str(i) + ":" + str(self.topic_characteristic_vector[i]) + ";0.0\n")		

	def saveRusellTuple(self, outFile):
		outFile.write(str(self.russell_tuple[0]) + "," + str(self.russell_tuple[1]) + '\n')

	def saveRusellTupleTopic(self, outFile):
		outFile.write(str(self.russell_tuple_topic[0]) + "," + str(self.russell_tuple_topic[1]) + '\n')		

	tweetId = ""
	originalTweet = ""
	usuario = ""
	wordSet = []
	russell_tuple = []
	russell_tuple_topic = []
	characteristic_vector = []
	topic_characteristic_vector = []
	polaritySent = 0
	primarySent = 0
	topicSent = 0
	topic = 0

def saveCharacteristicVectors(tweet_set, fileName):
	outFile = open(fileName, 'w')
	numOfTweets = 0
	for tweet in tweet_set:
		if(tweet.primarySent != Sentiments.INDETERMINADO.value):
			numOfTweets += 1
	outFile.write('SY\n')
	outFile.write(str(numOfTweets) + '\n')
	outFile.write('16\n')
	outFile.write('happy;elated;excited;alert;tense;nervous;stressed;upset;sad;unhappy;depressed;bored;calm;relaxed;serene;contented\n')
	for tweet in tweet_set:
		if(tweet.primarySent != Sentiments.INDETERMINADO.value):
			tweet.saveVector(outFile)
	outFile.close()

def saveTopicCharacteristicVectors(tweet_set, fileName, topicID):
	outFile = open(fileName, 'w')
	numOfTweets = 0
	for tweet in tweet_set:
		if(tweet.topic == topicID and tweet.topicSent != Sentiments.INDETERMINADO.value):
			numOfTweets += 1
	outFile.write('SY\n')
	outFile.write(str(numOfTweets) + '\n')
	outFile.write('16\n')
	outFile.write('happy;elated;excited;alert;tense;nervous;stressed;upset;sad;unhappy;depressed;bored;calm;relaxed;serene;contented\n')
	for tweet in tweet_set:
		if(tweet.topic == topicID and tweet.topicSent != Sentiments.INDETERMINADO.value):
			tweet.saveVectorTopic(outFile)	
	outFile.close()

def saveRussellTuples(tweet_set, fileName):
	outFile = open(fileName, 'w')
	for tweet in tweet_set:
		if(tweet.primarySent != Sentiments.INDETERMINADO.value):
			tweet.saveRusellTuple(outFile)
	outFile.close()

def saveRusellTuplesTopic(tweet_set, fileName, topicID):
	outFile = open(fileName, 'w')
	for tweet in tweet_set:
		if(tweet.topic == topicID and tweet.primarySent != Sentiments.INDETERMINADO.value):
			tweet.saveRusellTupleTopic(outFile)
	outFile.close()	

def updateTweets(tweet_set, collection):
	for tweet in tweet_set:
		tweet.updateTweet(collection)

def saveTweets(tweet_set, fileName):
	outFile = open(fileName, 'w')
	print(len(tweet_set), file=outFile)
	for tweet in tweet_set:
		tweet.saveClass(outFile)

def saveUsers(dic_user, fileName):
	outFile = open(fileName, 'w')
	print(len(dic_user), file=outFile)
	for userId , user in dic_user.iteritems():
		user.saveClass(outFile)

def loadTweetsAndUsers(userFileName , tweetFileName):
	dic_user = {}
	tweet_set = []
	userFile = open(userFileName, "r")
	userLines = userFile.readlines()
	userLines = [x.strip() for x in userLines]
	numOfUsers = int(userLines[0])
	i = 1
	for j in range(0, numOfUsers):
		userId = userLines[i]
		i += 1
		if not(userId in dic_user):
			dic_user[userId] = UserClass(userId)
		numConUsers = int(userLines[i])
		i += 1
		for k in range(0, numConUsers):
			userIdCon = userLines[i]
			i += 1
			if not(userIdCon in dic_user):
				dic_user[userIdCon] = UserClass(userIdCon)
			dic_user[userId].addUser(dic_user[userIdCon])
		principalTopic = int(userLines[i])
		i += 1
		dic_user[userId].principal_topic = principalTopic

	tweetFile = open(tweetFileName, 'r')
	tweetLines = tweetFile.readlines()
	tweetLines = [x.strip() for x in tweetLines]
	numOfTweets = int(tweetLines[0])
	print(tweetLines)
	i = 1

	#for j in range(0, numOfTweets):
	#	userId = userLines[i]		
	#	i += 1
	#	tweet_set.append(TweetClass("Tweet", dic_user[userId]))











