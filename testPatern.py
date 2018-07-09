#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from pattern.web import Twitter, plaintext

from pattern.es import parse

#twitter = Twitter(language = 'es')
#for tweet in twitter.search('"muy importante"', cached = False):
#	print(plaintext(tweet.text))

s = u'Recuerda que estar pendientes de nuestra salud es muy importante, realizate chequeos constantemente'
s = parse(s, lemmata = True)
print(s)

#ss = s.split(" ")
#print(ss)

#sss = [t.split("/") for t in ss]
#print(sss)

#ssss = [t[4] for t in sss]
#print(ssss)

res = [a[4] for a in [b.split("/") for b in s.split(" ")]]
print(res)

