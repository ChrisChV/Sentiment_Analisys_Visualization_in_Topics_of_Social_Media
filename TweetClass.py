from sentiments import *

class UserClass:
 	userId = ""
	tweet_set = []
	users_connections = []
	principat_topic = 0

	def __init__(self, userId):
		self.userId = userId
		self.tweet_set = []
		self.users_connections = []
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
		principat_topic = i_max
		return i_max


class TweetClass:
	#def __init__(self, originalTweet):
	#	self.originalTweet = originalTweet
	def __init__(self, originalTweet, user):
		self.originalTweet = originalTweet
		self.usuario = user
	def printClass(self):
		print(self.originalTweet)
		print(self.wordSet)
		print(self.russell_tuple)
		print(self.russell_tuple_topic)
		print(self.topic)
		print(getStrOfSentiment(self.polaritySent))
		print(getStrOfSentiment(self.primarySent))

		print

	originalTweet = ""
	usuario = ""
	wordSet = []
	russell_tuple = []
	russell_tuple_topic = []
	polaritySent = 0
	primarySent = 0
	topic = 0
