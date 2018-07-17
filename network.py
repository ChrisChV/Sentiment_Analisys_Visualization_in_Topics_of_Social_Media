#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TweetClass import *

def generateGraph(user_set, numOfTopics , outFileName):
	outFile = open(outFileName, 'w')
	outFile2 = open("out_test", 'w')
	outFile3 = open(outFileName + "_users", 'w')
	outFile4 = open(outFileName + "_users_topics", 'w')
	srtRelacion = " -- "
	srtTopic = "topic"
	dic_nodes = {}
	actualNode = 0
	#for userId, user in user_set.iteritems():
	#	dic_nodes[userId] = actualNode
	#	actualNode += 1
		#for i in range(0, numOfTopics):
		#	dic_nodes[str(userId) + srtTopic + str(i)] = actualNode
		#	actualNode += 1
	for userId, user in user_set.iteritems():
		#for i in range(0, numOfTopics):
			#for j in range(0, numOfTopics):
			#	if i != j:
			#		outFile.write(str(dic_nodes[str(user.userId) + srtTopic + str(i)]) + srtRelacion + str(dic_nodes[str(user.userId) + srtTopic + str(j)]) + '\n')
			#for user_con in user.users_cocnnections:
			#	outFile.write(str(dic_nodes[str(user.userId) + srtTopic + str(i)]) + srtRelacion + str(dic_nodes[str(user_con.userId) + srtTopic + str(i)]) + '\n')
		for user_con in user.users_connections:
			if not(user.userId in dic_nodes):
				dic_nodes[user.userId] = actualNode
				user.saveClass(outFile2, actualNode)
				outFile3.write(str(user.userId) + " " + str(actualNode) + '\n')
				outFile4.write(str(user.userId) + " " + str(user.principal_topic) + '\n')
				actualNode += 1
			if not(user_con.userId in dic_nodes):
				dic_nodes[user_con.userId] = actualNode
				user_con.saveClass(outFile2, actualNode)
				outFile3.write(str(user_con.userId) + " " + str(actualNode) + '\n')
				outFile4.write(str(user_con.userId) + " " + str(user_con.principal_topic) + '\n')
				actualNode += 1
			outFile.write(str(dic_nodes[user.userId]) + srtRelacion + str(dic_nodes[user_con.userId]) + ';\n')

	outFile.close()
	outFile2.close()
	outFile3.close()
	outFile4.close()