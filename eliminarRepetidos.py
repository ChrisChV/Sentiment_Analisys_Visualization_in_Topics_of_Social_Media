#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pymongo import MongoClient
client = MongoClient('mongodb://twitter:twitter@127.0.0.1/twitter')

db = client['twitter']
collection = db['Rusia2018']

repetidos = collection.aggregate([{"$group": {"_id": { "text": "$text"},"uniqueIds": { "$addToSet": "$_id" },"count": { "$sum": 1 }}},{ "$match": { "count": { "$gt": 1 } } }])


for i in repetidos:
	x = i["uniqueIds"]
	borrar = 0;
	while(len(x)!=1):
		borrar = x.pop(x.index(max(x)))
		collection.remove({"_id":borrar})
		print "Borrado ", borrar, '\n'

