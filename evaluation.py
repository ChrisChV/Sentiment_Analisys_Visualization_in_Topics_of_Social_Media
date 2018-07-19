import math


def person(rusell_sents_vector):
	xMean = 0
	yMean = 0
	numerador = 0
	raiz1 = 0;
	raiz2 = 0;
	for point in rusell_sents_vector:
		xMean += point[0]
		yMean += point[1]
	xMean /= len(rusell_sents_vector)
	yMean /= len(rusell_sents_vector)
	for point in rusell_sents_vector:
		numerador += (point[0] - xMean) * (point[1] - yMean)
		raiz1 += math.pow(point[0] - xMean, 2)
		raiz2 += math.pow(point[1] - yMean, 2)
	return float(numerador) / float(math.sqrt(raiz1) * math.sqrt(raiz2))


def getTopic(tweet, topics, dictionaryWord, dictByTopic):
	valores = []
	suma = 0
	for i in range(0,len(topics)):
		suma = 0
		topic = topics[i]
		for word in tweet:
			suma += dictByTopic[i][word]
		valores.append(suma)

	#for topic in topics:
	#	dictByTopic = {}
	#	for i in range(0,len(topic)):
	#		dictByTopic[dictionaryWord[i]] = topic[i]
	#	suma = 0
		
	i_max = -1
	valor_max = -1	
	for i in range(0, len(valores)):
		if(i_max == -1 or valor_max < valores[i]):
			i_max = i
			valor_max = valores[i]
	return i_max

def loadUserCommunities(fileName):	
	userDic = {}
	communitiesDic = {}
	with open(fileName) as infile:
		for line in infile:
			line = line.rstrip('\n').split()	
			userDic[line[0]] = line[2]
			if not(line[2] in communitiesDic):
				communitiesDic[line[2]] = []
			communitiesDic[line[2]].append(line[0])
	return userDic, communitiesDic

def getUserCommunitySet(userDic, user_set):
	user_community_set = {}
	for userID, communityId in userDic.iteritems():
		if not(communityId in user_community_set):
			user_community_set[communityId] = []
		if(userID in user_set):
			user_community_set[communityId].append(user_set[userID])
	return user_community_set


def getShanonEntropy(user_community_set, communityId, numOfTopics):
	generalSentValues = [0.0] * 19
	topicSentValues = []
	for i in range(0,numOfTopics):
		topicSentValues.append([0.0] * 19)
	generalSentProbs = [0.0] * 19
	topicSentProbs = []
	numOfUsersInTopics = [0.0] * numOfTopics
	for user in user_community_set[communityId]:
		numOfUsersInTopics[user.principal_topic] += 1
		for tweet in user.tweet_set:
			generalSentValues[tweet.polaritySent] += 1
			generalSentValues[tweet.primarySent] += 1
			topicSentValues[user.principal_topic][tweet.topicSent] += 1
	sumPrincipalSents = 0.0
	sumPolaritySents = 0.0
	sumTopicSents = [sum(values) for values in topicSentValues]
	for i in range(0,19):
		if(i == 17 or i == 18):
			sumPolaritySents += generalSentValues[i]
		else:
			sumPrincipalSents += generalSentValues[i]
	for i in range(0,19):
		if(i == 17 or i == 18):
			generalSentProbs[i] = generalSentValues[i] / sumPolaritySents
		else:
			generalSentProbs[i] = generalSentValues[i] / sumPrincipalSents	
	for i in range(0,numOfTopics):
		if(sumTopicSents[i] != 0):
			topicSentProbs.append([val / float(sumTopicSents[i]) for val in topicSentValues[i]])
		else:
			topicSentProbs.append([0] * len(topicSentValues[i]))
	polarityShanonEntropy = 0
	principalShanonEntropy = 0
	for i in range(17,18):
		if(generalSentProbs[i] != 0):
			polarityShanonEntropy +=  -(generalSentProbs[i]) * math.log(generalSentProbs[i],2)
	for i in range(0,17):
		if(generalSentProbs[i] != 0):
			principalShanonEntropy +=  -(generalSentProbs[i]) * math.log(generalSentProbs[i],2)

	#polarityShanonEntropy =  -1 * sum([generalSentProbs[i] * math.log(generalSentProbs[i],2) for i in range(17,19)])
	#principalShanonEntropy = -1 * sum([generalSentProbs[i] * math.log2(generalSentProbs[i],2) for i in range(0,17)])
	topicShanonEntropy = []
	for i in range(0, numOfTopics):
		tempSum = 0
		for prob in topicSentProbs[i]:
			if(prob != 0):
				tempSum += -(prob) * math.log(prob,2)
		topicShanonEntropy.append(tempSum)
		#topicShanonEntropy.append(-1 * sum([prob * math.log(prob,2) for prob in topicSentProbs[i]]))
	return polarityShanonEntropy, principalShanonEntropy, topicShanonEntropy, numOfUsersInTopics





