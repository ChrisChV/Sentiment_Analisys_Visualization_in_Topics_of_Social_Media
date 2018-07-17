#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from twython import Twython
from urlparse import urlparse
import sys
import json
import pymongo


if(len(sys.argv) != 2):
    print "Argumentos invalidos"
    exit()

print sys.argv[1]

hashtag = sys.argv[1]

client = MongoClient('mongodb://twitter:twitter@127.0.0.1/twitter')

db = client['twitter']
collection = db[hashtag+"tmp"]

APP_KEY = '8iuErv802dm1q9YQnOrtrcgIG'
APP_SECRET = 'dMnTqnQvUwOk0foTcSl0yDp8MDThsgdsgAD0W5Ox6qrOw3QnsY'

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

try:
    results = twitter.search(q=hashtag,lang='es',count='100')

except TwythonError as e:
    print e

for tweet in results['statuses']:
    print 'Usuario @%s Fecha: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['created_at'])
    ultimo = tweet
    print 'Geo: ' + tweet['user']['location']
    print 'Contenido: ' + tweet['text'].encode('utf-8'), '\n\n'
    collection.insert(tweet)

#print json.dumps(ultimo, indent=4, sort_keys=True)
