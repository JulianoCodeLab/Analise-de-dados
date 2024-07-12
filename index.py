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

df_states_ = df_states[df_states["data"] == "2020-05-13"]


#le o geojason
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))


#==================================================================================================
#----------------------------Iniciando a criação da dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#Contem o mapa mais moderno, e melhor para estilizar
fig = px.choropleth_mapbox(df_states_, locations= "estado", color= "casosNovos",
                            center={"lat": -16.95, "lon": -47.78}, zoom= 4,
                            geojson= brazil_states, color_continuous_scale= "Redor",
                            opacity= 0.4, hover_data={"casosAcumulado": True, "casosNovos": True, 
                            "obitosNovos": True, "estado": True})

fig.update_layout(
    paper_bgcolor = "#242424",
    autosize = True,
    margin = go.Margin(l=0, r=0, t=0, b=0),
    showlegend = False,
    mapbox_style = "carto-darkmatter"
)

#==================================================================================================
#----------------------------Layout

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dcc.Graph(id= "choropleth-map", figure= fig)
        ])
    ])
)


if __name__ == "__main__":
    app.run_server(debug = True)