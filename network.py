#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TweetClass import *

def generateGraph(user_set, numOfTopics , outFileName):
	outFile = open(outFileName, 'w')
	srtRelacion = " "
	srtTopic = "topic"
	for userId, user in user_set.iteritems():
		for i in range(0, numOfTopics):
			for j in range(0, numOfTopics):
				outFile.write(str(user.userId) + srtTopic + str(i) + srtRelacion + str(user.userId) + srtTopic + str(j) + '\n')
			for user_con in user.users_connections:
				outFile.write(str(user.userId) + srtTopic + str(i) + srtRelacion + str(user_con.userId) + srtTopic + str(i) + '\n')
	outFile.close()