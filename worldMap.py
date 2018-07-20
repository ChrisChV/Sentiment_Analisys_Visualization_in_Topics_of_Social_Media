#!/usr/bin/env python
# -*- coding: utf-8 -*-

import country_converter as coco
from pymongo import MongoClient
from collections import defaultdict
import pycountry as pyco
import unidecode
import json
import sys


if(len(sys.argv)!=2):
    "Argumentos incorrectos"
    exit()

hashtag = sys.argv[1]
print(hashtag)

array_paises = []

#tweetsData = open("tweetsData","w")

#tweetsData.write("COUNTRY,Tweets,CODE\n")

cc = coco.CountryConverter()

client = MongoClient('mongodb://twitter:twitter@127.0.0.1/twitter')

db = client['twitter']
collection = db[hashtag]

my_dict = defaultdict(int)

allUsers = collection.find({},{"user":1})
i=0
localizacion = ""
for doc in allUsers:
    if(doc["user"]["location"] != ""):
        localizacion = unidecode.unidecode(doc["user"]["location"]).capitalize()
        try:
            if(localizacion.find(', ') != -1):
                localizacion = localizacion.split(', ')[1].capitalize()
                if(localizacion=="Espana"):
                    my_dict["ES"]+=1
                    i+=1
                else: 
                    a= pyco.countries.get(name=localizacion).alpha_2
                    my_dict[a]+=1
                    i+=1
            elif(localizacion.find('- ') != -1):
                localizacion = localizacion.split('- ')[1].capitalize()
                if(localizacion=="Espana"):
                    my_dict["ES"]+=1
                    i+=1
                else: 
                    a= pyco.countries.get(name=localizacion).alpha_2
                    my_dict[a]+=1
                    i+=1
            elif(localizacion.find('-') != -1):
                localizacion = localizacion.split('-')[1].capitalize()
                if(localizacion=="Espana"):
                    my_dict["ES"]+=1
                    i+=1
                else: 
                    a= pyco.countries.get(name=localizacion).alpha_2
                    my_dict[a]+=1
                    i+=1
            else:
                if(localizacion=="Espana"):
                    my_dict["ES"]+=1
                    i+=1
                else: 
                    a= pyco.countries.get(name=localizacion.capitalize()).alpha_2
                    my_dict[a]+=1
                    i+=1
            
        except KeyError as e:
            if(")" in localizacion):
                continue
            standard_names = cc.convert(names=localizacion, to='ISO2')
            if(len(standard_names) == 3):
                my_dict[standard_names]+=1
                i+=1


for key,value in my_dict.items():
    array_paises.append({"name":cc.convert(names=key, to='short_name'),"id":key,"tweetsCount":value})
    #tweetsData.write(cc.convert(names=key, to='short_name') + ',' + str(value) + ',' + key + '\n')


#tweetsData.close()

print("encontrados: " + str(i))

with open('worldMapCount.json', 'w') as fp:
    json.dump(array_paises, fp)
