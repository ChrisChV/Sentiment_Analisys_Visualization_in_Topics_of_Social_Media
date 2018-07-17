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
                fi(localizacion=="Espana"):
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
            standard_names = cc.convert(names=localizacion, to='ISO2')
            if(len(standard_names) == 3):
                my_dict[standard_names]+=1
                i+=1


for key,value in my_dict.items():
    array_paises.append({"name":cc.convert(names=key, to='short_name'),"id":key,"tweetsCount":value})
    #tweetsData.write(cc.convert(names=key, to='short_name') + ',' + str(value) + ',' + key + '\n')


#tweetsData.close()

print("encontrados: " + str(i))

dict_paises = {
  "map": {
    "enabled": True,
    "title": {
      "enabled": True,
      "useHtml": True,
      "text": "Tweets por país",
      "padding": {
        "left": 0,
        "top": 10,
        "bottom": 10,
        "right": 0
      }
    },
    "padding": {
      "left": 0,
      "top": 0,
      "bottom": 0,
      "right": 0
    },
    "credits": {
      "text": "Data source: Twitter",
      "url": "https://twitter.com/",
      "logoSrc": "http://http://abs.twimg.com/favicons/favicon.ico",
      "enabled": True
    },
    "interactivity": {
      "selectionMode": "none"
    },
    "defaultSeriesType": "choropleth",
    "dataArea": {
      "enabled": True
    },
    "type": "map",
    "colorRange": {
      "enabled": True,
      "title": {
        "zIndex": 50,
        "enabled": False
      },
      "labels": {
        "zIndex": 50,
        "enabled": True,
        "padding": {
          "left": 0,
          "top": 3,
          "bottom": 0,
          "right": 0
        }
      },
      "minorLabels": {
        "zIndex": 50,
        "enabled": False
      },
      "ticks": {
        "zIndex": 50,
        "enabled": True,
        "stroke": {
          "color": "#ffffff",
          "thickness": 3
        },
        "length": 7,
        "position": "center"
      },
      "minorTicks": {
        "zIndex": 50,
        "enabled": False
      },
      "marker": {
        "zIndex": 51,
        "enabled": True
      },
      "colorLineSize": 5
    },
    "geoScale": {
      "type": "geo",
      "precision": [
        2,
        2
      ],
      "gap": 0,
      "xTicks": {
        "minCount": 4,
        "maxCount": 6
      },
      "xMinorTicks": {
        "minCount": 4,
        "maxCount": 6
      },
      "yTicks": {
        "minCount": 4,
        "maxCount": 6
      },
      "yMinorTicks": {
        "minCount": 4,
        "maxCount": 6
      }
    },
    "geoData": "anychart.maps.world",
    "series": [
      {
        "enabled": True,
        "seriesType": "choropleth",
        "tooltip": {
          "useHtml": True
        },
        "normal": {
          "labels": {
            "enabled": False
          }
        },
        "hovered": {
          "fill": "#f48fb1",
          "stroke": "#ab647c"
        },
        "selected": {
          "fill": "#c2185b",
          "stroke": "#881140",
          "lowFill": {
            "color": "#333",
            "opacity": 0.85
          },
          "highFill": {
            "color": "#333",
            "opacity": 0.85
          }
        },
        "data" : array_paises,
        "overlapMode": None,
        "colorScale": 0
      }
    ],
    "colorScales": [
      {
        "type": "ordinal-color",
        "inverted": False,
        "ticks": {
          "maxCount": 100
        },
        "ranges": [
          {
            "less": 10
          },
          {
            "from": 10,
            "to": 30
          },
          {
            "from": 30,
            "to": 50
          },
          {
            "from": 50,
            "to": 100
          },
          {
            "from": 100,
            "to": 200
          },
          {
            "from": 200,
            "to": 300
          },
          {
            "from": 300,
            "to": 500
          },
          {
            "from": 500,
            "to": 1000
          },
          {
            "greater": 1000
          }
        ],
        "colors": [
          "#81d4fa",
          "#4fc3f7",
          "#29b6f6",
          "#039be5",
          "#0288d1",
          "#0277bd",
          "#01579b",
          "#014377",
          "#000000"
        ]
      }
    ],
    "gridsSettings": {
      "vertical": {
        "enabled": None
      },
      "horizontal": {
        "enabled": None
      },
      "palette": {
        "type": "distinct",
        "items": [
          "none"
        ]
      },
      "enabled": False
    },
    "crosshair": {
      "enabled": False,
      "xLabels": [
        {
          "enabled": True,
          "fontSize": 12,
          "fontFamily": "Verdana, Helvetica, Arial, sans-serif",
          "fontColor": "#ffffff",
          "fontOpacity": 1,
          "fontDecoration": "none",
          "fontStyle": "normal",
          "fontVariant": "normal",
          "fontWeight": 400,
          "letterSpacing": "normal",
          "textDirection": "ltr",
          "lineHeight": "normal",
          "textIndent": 0,
          "vAlign": "top",
          "hAlign": "start",
          "wordWrap": "normal",
          "wordBreak": "normal",
          "textOverflow": "",
          "selectable": False,
          "disablePointerEvents": True,
          "useHtml": False,
          "text": "Label text",
          "width": None,
          "height": None,
          "anchor": None,
          "offsetX": 0,
          "offsetY": 0,
          "rotation": 0,
          "adjustFontSize": {
            "width": False,
            "height": False
          },
          "minFontSize": 8,
          "maxFontSize": 16,
          "background": {
            "zIndex": 0,
            "enabled": True,
            "fill": {
              "color": "#212121",
              "opacity": 0.7
            },
            "stroke": "none",
            "disablePointerEvents": True,
            "cornerType": "round"
          },
          "padding": {
            "left": 10,
            "top": 5,
            "bottom": 5,
            "right": 10
          },
          "axisIndex": 2
        }
      ],
      "yLabels": [
        {
          "enabled": True,
          "fontSize": 12,
          "fontFamily": "Verdana, Helvetica, Arial, sans-serif",
          "fontColor": "#ffffff",
          "fontOpacity": 1,
          "fontDecoration": "none",
          "fontStyle": "normal",
          "fontVariant": "normal",
          "fontWeight": 400,
          "letterSpacing": "normal",
          "textDirection": "ltr",
          "lineHeight": "normal",
          "textIndent": 0,
          "vAlign": "top",
          "hAlign": "start",
          "wordWrap": "normal",
          "wordBreak": "normal",
          "textOverflow": "",
          "selectable": False,
          "disablePointerEvents": True,
          "useHtml": False,
          "text": "Label text",
          "width": None,
          "height": None,
          "anchor": None,
          "offsetX": 0,
          "offsetY": 0,
          "rotation": 0,
          "adjustFontSize": {
            "width": False,
            "height": False
          },
          "minFontSize": 8,
          "maxFontSize": 16,
          "background": {
            "zIndex": 0,
            "enabled": True,
            "fill": {
              "color": "#212121",
              "opacity": 0.7
            },
            "stroke": "none",
            "disablePointerEvents": True,
            "cornerType": "round"
          },
          "padding": {
            "left": 10,
            "top": 5,
            "bottom": 5,
            "right": 10
          },
          "axisIndex": 3
        }
      ]
    }
  }
}


with open('worldMapCount.json', 'w') as fp:
    fp.write("<document>")
    json.dump(dict_paises,fp)
    fp.write("</document>")

print(array_paises)