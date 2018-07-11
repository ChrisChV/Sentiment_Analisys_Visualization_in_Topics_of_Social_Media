#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from pattern.web import Twitter, plaintext

#from pattern.es import parse

#twitter = Twitter(language = 'es')
#for tweet in twitter.search('"muy importante"', cached = False):
#	print(plaintext(tweet.text))

#s = u'Recuerda que estar pendientes de nuestra salud es muy importante, realizate chequeos constantemente'
#s = parse(s, lemmata = True)
#print(s)

#ss = s.split(" ")
#print(ss)

#sss = [t.split("/") for t in ss]
#print(sss)

#ssss = [t[4] for t in sss]
#print(ssss)

#res = [a[4] for a in [b.split("/") for b in s.split(" ")]]
#print(res)

#from preprocessing import *


#doc_set = [u'Recuerda que estar pendientes de nuestra salud es muy importante, realizate chequeos constantemente']

#preprocessing(doc_set)

from TweetClass import *

tweet1_t = "Hola"
tweet2_t = "Adios"

dicUsers = {}
dicUsers['usuario1'] = UserClass()

tweet1_t = TweetClass(tweet1_t, dicUsers['usuario1'])
tweet2_t = TweetClass(tweet2_t, dicUsers['usuario1'])


if('usuario1' in dicUsers):
	dicUsers['usuario1'].addTweet(tweet1_t)
	dicUsers['usuario1'].addTweet(tweet2_t)

print(dicUsers['usuario1'].tweet_set)
print(tweet1_t.usuario.tweet_set)





