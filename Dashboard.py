#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:57:52 2022

@author: johnrohanputhotaignatius
"""


import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from dash import dcc as dcc
from dash import html as html
import plotly.express as px
from dash import dash_table as dt


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

df = pd.read_csv('/Users/johnrohanputhotaignatius/Desktop/MA 705 - Data Science/NetflixOriginals.csv', encoding = "ISO-8859-1")


app.layout = html.Div([
    html.H1('Netflix Dashboard!',
            style={'textAlign' : 'center'}),
    html.H5("By John Rohan",
            style={'textAlign' : 'right'}, id = 'author'),
    html.Div([
        html.H3('Introduction:'),
        html.P('This dashboard is about a dataset consisting all Netflix original films released as of June 1st, 2021. Additionally, it also includes all Netflix documentaries and specials. The data was webscraped off of a Wikipedia page, which was then integrated with a dataset consisting of all of their corresponding IMDB scores. IMDB scores are voted on by community members, and the majority of the films have 1,000+ reviews.'),
        ]),
    
    html.H5("Select Genre:"),
    dcc.Dropdown(
        id='genrename',
        options=[{'label': b, 'value': b} for b in sorted(df.Genre.unique())],
        value='Documentary',
        clearable=False
    ),
             html.Br(),
     html.H5("Select Language:"),
    dcc.Dropdown(id='languagename',
                 options=[{'label': b, 'value': b} for b in sorted(df.Language.unique())],
                 value='English',
                 multi=True),
    dcc.Graph(id='displayscatter', figure={}),
             html.Br(),
    
    html.Div([
        html.H5('Search Results'),
        
        dt.DataTable(id = 'my_datatable',
                     columns =[{'id': c, 'name':c} for c in df.columns.values],
                     virtualization = True,
                     page_action = 'native',
                     page_size=15,
                     style_table={'height': '300px', 'overflowY': 'auto'},
                     style_header={'backgroundColor': 'LightGrey'},
                     style_cell={
                         'backgroundColor': 'AliceBlue',
                         'color': 'black'
                    }
    
                     )]),
    html.Div([
        html.H3('Source:'),
        html.A('Dataset Source',href='https://www.kaggle.com/datasets/luiscorter/netflix-original-films-imdb-scores?resource=download',
               target='_blank'),
        ])
    ])


@app.callback(
    Output('my_datatable', 'data'),
    Input('genrename', 'value'),
    Input('languagename', 'value')

)

def display_table(select_genre, select_language):
    table = df[(df.Genre == select_genre) & (df.Language.isin(select_language))]
    return table.to_dict('records')


@app.callback(
    Output('languagename', 'options'),
    Input('genrename', 'value')
)
def set_title_options(chosen_genre):
    dff = df[df.Genre==chosen_genre]
    return [{'label': c, 'value': c} for c in sorted(dff.Language.unique())]

@app.callback(
    Output('languagename', 'value'),
    Input('languagename', 'options')
)

def set_title_value(title_names):
    print(title_names)
    return [x['value'] for x in title_names]

@app.callback(
    Output('displayscatter', 'figure'),
    Input('languagename', 'value'),
    Input('genrename', 'value')
)
def update_graph(selected_language, selected_genre):
    if len(selected_language) == 0:
        return dash.no_update
    else:
        dff = df[(df.Genre==selected_genre) & (df.Language.isin(selected_language))]
        
        fig = px.scatter(dff, x='Runtime', y='IMDBScore', color='IMDBScore',
                         hover_name='Title',
                         title = 'Scatter Plot of Runtime and IMDB Score of Titles')
        
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    
    