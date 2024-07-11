import dash                                                     #Gerencia a dashboard e cria o servidor 
from dash import dcc                                            #resonsavel por todos os componentes uteis na dash
from dash import html                                           #Permite colocar codigos html na dash
from dash.dependencies import Input, Output                     #Permite interação com o usuario
import dash_bootstrap_components as dbc                         #Permite utilizar html,css e JS para formatar a interface web


import plotly.express as px                                     #Permite criação dos graficos dos plotly de forma mais faceis
import plotly.graph_objects as go                               #Nos da mais controle sobre as ferranentas plotly

import numpy as np                                              #Oferece  suporte oara array, coleção de funções matematicas etc.
import json                                                     #Para leitura de dados ".json"
import pandas as pd


#Para ler o csv
#df = pd.read_csv('/home/juliano/Documentos/projeto/Python/Dashboard/COVID-19/HIST_PAINEL_COVIDBR_13mai2021.csv', sep= ';')

#le apenas as info do dataframe que contem estado
#df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]

#le apenas as info do dataframe que contem estado
#df_brasil = df[df["regiao"] == "Brasil"]

#Para ler o csv
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")


#le o geojason
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

#Para ver qual o tipo do dado
type(brazil_states)

brazil_states.keys()

brazil_states["features"]
