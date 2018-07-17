#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plotly.plotly as py
import plotly.tools as tl
import pandas as pd


tl.set_credentials_file(username='karldivad', api_key='GaryfedxFZETaXe3Dj2V')

df = pd.read_csv('tweetsData')

print(type(df))
print(type(df['CODE']))

data = [ dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = df['Tweets'],
        text = df['COUNTRY'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = '# de tweets'),
      ) ]

layout = dict(
    title = 'Cantidad de Tweets por país entre el 9 y 10 de julio de 2018 con el hashtag #Rusia2018',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='d3-world-map' )