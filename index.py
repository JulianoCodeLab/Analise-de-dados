import dash                                                     # Gerencia a dashboard e cria o servidor 
from dash import dcc                                            # Responsável por todos os componentes úteis na dash
from dash import html                                           # Permite colocar códigos HTML na dash
from dash.dependencies import Input, Output                     # Permite interação com o usuário
import dash_bootstrap_components as dbc                         # Permite utilizar HTML, CSS e JS para formatar a interface web

import plotly.express as px                                     # Permite criação dos gráficos dos plotly de forma mais fácil
import plotly.graph_objects as go                               # Nos dá mais controle sobre as ferramentas plotly

import numpy as np                                              # Oferece suporte para array, coleção de funções matemáticas etc.
import json                                                     # Para leitura de dados ".json"
import pandas as pd

# Para ler o CSV
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")

df_states_ = df_states[df_states["data"] == "2020-05-13"]
df_data = df_states[df_states["estado"] == "RJ"]

# Lê o GeoJSON
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

#==================================================================================================
#----------------------------Iniciando a criação da dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Contém o mapa mais moderno, e melhor para estilizar
fig = px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos",
                            center={"lat": -16.95, "lon": -47.78}, zoom=4,
                            geojson=brazil_states, color_continuous_scale="Redor",
                            opacity=0.4, hover_data={"casosAcumulado": True, "casosNovos": True, 
                            "obitosNovos": True, "estado": True})

fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

# Criação da figura correta
fig2 = go.Figure(layout={"template": "plotly_dark"})

fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

#==================================================================================================
#----------------------------Layout

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="line-graph", figure=fig2)
        ]),
        dbc.Col([
            dcc.Graph(id="choropleth-map", figure=fig)
        ])
    ])
)

if __name__ == "__main__":
    app.run_server(debug=True)
