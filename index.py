import dash  # Gerencia a dashboard e cria o servidor 
from dash import dcc  # Responsável por todos os componentes úteis na dash
from dash import html  # Permite colocar códigos HTML na dash
from dash.dependencies import Input, Output  # Permite interação com o usuário
import dash_bootstrap_components as dbc  # Permite utilizar HTML, CSS e JS para formatar a interface web

import plotly.express as px  # Permite criação dos gráficos dos plotly de forma mais fácil
import plotly.graph_objects as go  # Nos dá mais controle sobre as ferramentas plotly

import numpy as np  # Oferece suporte para array, coleção de funções matemáticas etc.
import json  # Para leitura de dados ".json"
import pandas as pd


#=================================== Para ler o CSV
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")



df_states_ = df_states[df_states["data"] == "2020-05-13"]
df_data = df_states[df_states["estado"] == "RJ"]

select_columns = {
    "casosAcumulado": "Casos Acumulados",
    "casosNovos": "Novos Casos",
    "obitosAcumulado": "Óbitos Totais",
    "obitosNovos": "Óbitos por dia"
}

# Lê o GeoJSON
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# =========================== Iniciando a criação da dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# ===========================Contém o mapa mais moderno, e melhor para estilizar
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

# Criação da figura
fig2 = go.Figure(layout={"template": "plotly_dark"})

fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)

#======================================== Layout da aplicação
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url("python-covid.png"), height=50),
                html.H5("Evolução COVID-19"),
                dbc.Button("Brasil", color="primary", id="location-button", size="lg")
            ], style={}),
            html.P("Informe a data na qual deseja obter informações: ", style={"margin-top": "40px"}),
            html.Div(id="div-test", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brasil["data"].min(),
                    max_date_allowed=df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="MMMM D, YYYY",
                    style={"border": "0px solid black"}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos recuperados"),
                            html.H3(style={"color": "#adfc92"}, id="casos-recuperados-text"),
                            html.Span("Em acompanhamento"),
                            html.H5(id="em-acompanhamento-text"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px",
                                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                        "color": "#FFFFFF"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Total de casos confirmados"),
                            html.H3(style={"color": "#389fd6"}, id="casos-confirmados-text"),
                            html.Span("Novos casos na data"),
                            html.H5(id="novos-casos-text"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px",
                                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                        "color": "#FFFFFF"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Óbitos confirmados"),
                            html.H3(style={"color": "#DF2935"}, id="obitos-text"),
                            html.Span("Óbitos na data"),
                            html.H5(id="obitos-na-data-text"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px",
                                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                        "color": "#FFFFFF"})
                ], md=4),
            ]),

            html.Div([
                html.P("Selecione o tipo de informação: ", style={"margin-top": "25px"}),
                dcc.Dropdown(id="location-dropdown",
                            options=[{"label": j, "value": i} for i, j in select_columns.items()],
                            value="casosNovos",
                            style={"margin-top": "10px"}
                            ),
                dcc.Graph(id="line-graph", figure=fig2)
            ])

        ], md=5, style={"padding": "25px", "background-color": "#242424"}),

        dbc.Col([
                dcc.Loading(id="loading-1", type="default",
                children=[
                    dcc.Graph(id="choropleth-map", figure=fig, style={"height": "100vh", "margin-right": "10px"})
                ]
            ),            
        ], md=7, style={"padding-right": "opx", "padding-left": "0px",})
    ], style={"margin-right": "0px", "margin-left": "0px"})
, fluid=True)


#======================================Interatividadade

@app.callback(
        [
            Output("casos-recuperados-text", "children"),
            Output("em-acompanhamento-text", "children"),
            Output("casos-confirmados-text", "children"),
            Output("novos-casos-text", "children"),
            Output("obitos-text", "children"),
            Output("obitos-na-data-text", "children"),
        ],

        [Input("date-picker", "date"), Input("location-button", "children")]
)
def display_status(date, location):
    if location == "BRASIL": 
        df_date_on_date = df_brasil[df_brasil["date"] == date]
    else:
        df_date_on_date = df_states[(df_states["estado"] == location) & (df_states["date"] == date)]
        
    df_date_on_date["Recuperadosnovos"]
    recuperados_novos = "-" if df_date_on_date["Recuperadosnovos"].isna().value[0] else f'{int(df_date_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".")
    acompanhamentos_novos = "-" if df_date_on_date["emAcompanhamentoNovos"].isna().value[0] else f'{int(df_date_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".")
    casos_acumulados = "-" if df_date_on_date["casosAcumulado"].isna().value[0] else f'{int(df_date_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
    casos_novos = "-" if df_date_on_date["casosNovos"].isna().value[0] else f'{int(df_date_on_date["casosNovos"].values[0]):,}'.replace(",", ".")
    obitos_acumulado = "-" if df_date_on_date["obitosAcumulado"].isna().value[0] else f'{int(df_date_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".")
    obitos_novos = "-" if df_date_on_date["obitosNovos"].isna().value[0] else f'{int(df_date_on_date["obitosNovos"].values[0]):,}'.replace(",", ".")
    
    return (recuperados_novos,
        acompanhamentos_novos,
        casos_acumulados,
        casos_novos,
        obitos_acumulado,
        obitos_novos,)
if __name__ == "__main__":
    app.run_server(debug=True)
