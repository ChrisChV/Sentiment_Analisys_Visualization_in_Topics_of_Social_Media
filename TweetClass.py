from sentiments import *

class TweetClass:
	def __init__(self, originalTweet):
		self.originalTweet = originalTweet
	def printClass(self):
		print(self.originalTweet)
		print(self.wordSet)
		print(self.russell_tuple)
		print(getStrOfSentiment(self.polaritySent))
		print(getStrOfSentiment(self.primarySent))
		print

	originalTweet = ""
	usuario = ""
	wordSet = []
	russell_tuple = []
	polaritySent = 0
	primarySent = 0
	topic = 0
