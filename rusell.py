#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import unicodedata

DICTONARY_FILE_ = "DICT_v1.csv"
F_D_ = {'w': 1, 'v_m': 2, 'v_o': 3, 'a_m': 5, 'a_o': 6}
SEPARATOR_ = ","

def removeAccents(s):
	nfkd_form = unicodedata.normalize('NFKD', s.decode('unicode-escape'))
	return str(u"".join([c for c in nfkd_form if not unicodedata.combining(c)]))

def loadDict():
	dicty = dict()
	i = 0
	infile = open(DICTONARY_FILE_, 'r')
	infile.readline().strip('\n')
	for line in infile:
		row = line.strip('\n').split(SEPARATOR_)
		if (row[F_D_['v_o']] != 'NA'):
			s = removeAccents(row[F_D_['w']])
			dicty[s] = {'v': [float(row[F_D_['v_m']]), float(row[F_D_['v_o']])], 'a': [float(row[F_D_['a_m']]), float(row[F_D_['a_o']])]}
			i += 1
	print `i` + " words loaded"
	return dicty

def getSentimentScore(tokens, dictByTopic, dictTokens):
	num_v, den_v, num_a, den_a = 0, 0, 0, 0
	for i in range(0, len(tokens)):
		if (tokens[i] in dictTokens):
			td = dictByTopic[tokens[i]] if type(dictByTopic) is dict else dictByTopic
			num_v += ((td * dictTokens[tokens[i]]['v'][0]) / dictTokens[tokens[i]]['v'][1])
			den_v += (td / dictTokens[tokens[i]]['v'][1])
			num_a += ((td * dictTokens[tokens[i]]['a'][0]) / dictTokens[tokens[i]]['a'][1])
			den_a += (td / dictTokens[tokens[i]]['a'][1])
	return num_v / den_v if den_v != 0 else 0, num_a / den_a if den_a != 0 else 0

d = loadDict()
v, a = getSentimentScore(['odio', 'tristeza', 'amor'], 1, d)
print v, a
