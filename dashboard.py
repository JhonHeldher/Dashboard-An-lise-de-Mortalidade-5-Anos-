#======================================================================================================================
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from pandas._libs import properties
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

df_card = pd.read_csv('concatenados/df_card.csv')

df_melt_mes_mnd = pd.read_csv('concatenados/df_melt_mes_mnd.csv')

df_mapa = pd.read_csv('concatenados/df_mapa.csv')

# brazil_geo = json.load(open("Json/brazil_geo.json", "r"))
brazil_geo = json.load(open("Json/brazil_geo.json", "r"))
state_geo = json.load(open("Json/uf.json", "r", encoding='latin-1'))

for feature in state_geo['features']:
    feature['properties']['GEOCODIGO'] = int(feature['properties']['GEOCODIGO'])


select_columns_mn = {
                "Mortos": "Mortos",
                "nascidos": "nascidos",
                }
select_columns_ano = ["todos os anos", "2018", "2019", "2020", "2021", "2022"]


# Criação do app Dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# ↧ layout ↧ ========================================================================================================================================

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
    
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Col([
                            dbc.Row([
                                dbc.Row([
                                    dbc.Col(html.Legend("Análise de Mortalidade (5 Anos)", style={'font-weight': 'bold', 'font-size': '18px', 'height': '25px', 'margin-left' : '20px'}), width=9),
                                    dbc.Col(ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]), width=3),
                                ]),

                                dbc.Card([
                                    dbc.CardBody([
                                        html.Div([
                                    
                                            html.Div([
                                                html.P("Selecione o ano:", style={"margin-top": "-15px",'font-size': '12px'}),
                                                dcc.Dropdown(
                                                    id="year-dropdown",
                                                    options=[{"label": str(year), "value": year} for year in select_columns_ano],
                                                    value="todos os anos",  # Selecionar "todos" como valor inicial
                                                    style={"margin-top": "-10px"},
                                                ),
                                            ]),
                                            
                                            html.Div([
                                                html.P("Selecione o estado:", style={"margin-top": "5px",'font-size': '12px'}),
                                                dcc.Dropdown(
                                                    id="state-dropdown",
                                                    options=[{"label": "Brasil", "value": "BR"}] +
                                                            [{"label": state, "value": state} for state in df_mapa["localidade"].unique()],
                                                    value="BR",
                                                    style={"margin-top": "-10px"},
                                                ),
                                            ]),

                                            html.Div([
                                                html.P("Selecione entre Mortos e Nascidos:", style={"margin-top": "5px",'font-size': '12px'}),
                                                dcc.Dropdown( 
                                                    id="location-dropdown_mn",
                                                    options=[{"label": j, "value": i} for i, j in select_columns_mn.items()],
                                                    value="Mortos",
                                                    style={"margin-top": "-10px"},
                                                ),
                                            ]),
                                        ], id="teste"),
                                    ]),
                                ]),
                            ])
                        ])
                    ])
                ]),
            ], className='g-2 my-auto'),
            
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='graph6', className='dbc', config=config_graph)
                    ])
                ], style=tab_card),
            ], className='g-2 my-auto', style={'margin-top': '37px'}),
        ], sm=12, lg=4),  

    # ↧ 4 Cards e dois grafico  ↧======================↥ Filtro e Mapa ↥===================================================================================================================
     
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='graph1', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='graph2', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                    ])
                ], sm=12, lg=6),
                
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='graph3', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='graph4', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                    ])
                ], sm=12, lg=6),
            ], className='g-2 my-auto'),
            dbc.Row([  
                dbc.Col([  
                    dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph5', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card),     
                    ]),    
            ], className='g-2 my-auto', style={'margin-top': '7px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph7', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card),
                ]), 
            ], className='g-2 my-auto', style={'margin-top': '7px'}),
        ], sm=12, lg=8, className='g-2 my-auto'),         
    ]), 
], fluid=True, style={'height': '95vh'})

# ↧ callback e Graficos ↧==================↥ layout ↥=======================================================================================================================

#===============================================
    
def create_indicator(title, value, reference):
    return go.Figure(
        go.Indicator(
            mode='number+delta',
            title={"text": title},
            value=value,
            number={'prefix': ""},
            delta={'relative': True, 'valueformat': '.1%', 'reference': reference}
        )
    )

#=========================================================================================================================================

@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    # Input('radio-ano', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def update_graphs(toggle):
    template = template_theme1 if toggle else template_theme2
  
    df_card_m = df_card[['ano', 'Mortes']].copy()
    df_card_m.sort_values(by='Mortes', ascending=False, inplace=True)
    
    figText = go.Figure()
    figText.add_trace(go.Indicator(
        mode='number+delta',
        title= {"text": f"<span style='font-size:70%'>{df_card_m['ano'].iloc[0]} - Mortes</span><br>"},
        value = df_card_m['Mortes'].iloc[0],
        number = {'prefix': ""},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card_m['Mortes'].mean()},
        delta_increasing_color = "red" # add this line
    ))

   
    
    df_card_n = df_card[['ano', 'nascidos']].copy()
    df_card_n.sort_values(by='nascidos', ascending=False, inplace=True)

    figTextN = go.Figure()
    figTextN.add_trace(go.Indicator(mode='number+delta',
            title= {"text":f"<span style='font-size:70%'>{df_card_n['ano'].iloc[0]} - Nascimento</span><br>"},
            value = df_card_n['nascidos'].iloc[0],
            number = {'prefix': ""},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card_n['nascidos'].mean()}
    ))
        
    df_card_d = df_card[['ano', 'diferenca']].copy()
    df_card_d.sort_values(by='diferenca', ascending=False, inplace=True)

    figTextD = go.Figure()
    figTextD.add_trace(go.Indicator(mode='number+delta',
            title= {"text":f"<span style='font-size:70%'>{df_card_d['ano'].iloc[0]} - Aumento população</span><br>"},
            value = df_card_d['diferenca'].iloc[0],
            number = {'prefix': ""},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card_d['diferenca'].mean()}
    ))
    
    df_card.sort_values(by='valor', ascending=False, inplace=True)

    figProjPop = go.Figure()
    figProjPop.add_trace(go.Indicator(mode='number+delta',
            title = {"text": f"<span style='font-size:70%'>{df_card['ano'].iloc[0]} - Pupulação</span><br>"},
            value = df_card['valor'].iloc[0],
            delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card['valor'].mean()}
    ))
    
    figures = [figText, figTextN, figTextD, figProjPop]
    
    for fig in figures:
        fig.update_layout(main_config, height=75, template=template)
        fig.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})

    return figures

# ↧ Grafico de linha Natalidade e Mortalidade ↧ ====================↥ cards Brazil ↥=====================================================================================================================

@app.callback(
    Output('graph5', 'figure'),
    Input('year-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def graph5(selected_year, toggle):
    template = template_theme1 if toggle else template_theme2
    
    if selected_year == 'todos os anos':  
        filtered_df = df_melt_mes_mnd 
    else:
        selected_year = str(selected_year)  # Converter para string
        filtered_df = df_melt_mes_mnd[df_melt_mes_mnd['data'].astype(str).str.startswith(selected_year)]
  
    figline = go.Figure()

    figline.add_trace(go.Line(x=filtered_df['data'], y=filtered_df['Mortos'], name='Mortos'))
    figline.add_trace(go.Line(x=filtered_df['data'], y=filtered_df['nascidos'], name='Nascidos', line=dict(color='lightblue')))

    figline.update_layout(
        title='Natalidade e Mortalidade',
    )
    figline.update_layout(main_config, height=250, template=template)
    figline.update_layout({"margin": {"l":0, "r":0, "t":30, "b":0}})
    return figline

# ↧ Mapa ↧=============↥ Grafico de linha Natalidade e Mortalidade ↥============================================================================================================================

@app.callback(
    Output('graph6', 'figure'),
    Input('state-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def graph6(selected_state, selected_year, toggle):
    template = template_theme1 if toggle else template_theme2
    
    if selected_year == "todos os anos":  # Verifica se a opção selecionada é "todos os anos"
        filtered_df = df_mapa  # Mantém o dataframe completo
    elif selected_state == "BR":
        filtered_df = df_mapa[df_mapa["ano"] == int(selected_year)]
    else:
        filtered_df = df_mapa[(df_mapa["ano"] == int(selected_year)) & (df_mapa["localidade"] == selected_state)]
    
    figMap = px.choropleth(filtered_df, geojson=state_geo, color="Mortos",
                        locations="localidade",
                        featureidkey='properties.NOME_UF',
                        color_continuous_scale="Blues",
                        projection="mercator",
                        labels= {'Mortos':'Mortalidade'},
                        hover_data={'localidade' : True, 'nascidos': True},
                        )
    figMap.update_geos(fitbounds="locations", visible=False)
    figMap.update_geos(showcountries=False, showcoastlines=False, showland=False, showrivers=False)
    figMap.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    
    figMap.update_layout(main_config, height=415, template=template)
    return figMap


# ↧ Grafico de barra Aumento populacional ↧===============↥ Mapa ↥=========================================================================================================================================
@app.callback(
    Output('graph7', 'figure'),
    Input('year-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(selected_year, toggle):
    template = template_theme1 if toggle else template_theme2
    
    if selected_year == 'todos os anos':  
        filtered_df = df_melt_mes_mnd 
    else:
        selected_year = str(selected_year)  # Converter para string
        filtered_df = df_melt_mes_mnd[df_melt_mes_mnd['data'].astype(str).str.startswith(selected_year)]
    
    figBarPop = go.Figure(go.Bar(
        x=filtered_df['data'],
        y=filtered_df['diferencia'],
        orientation='v',
        textposition='auto',
        insidetextfont=dict(family='Times', size=12))
    )

    figBarPop.update_layout(
        title='Variação Populacional',
    )


    figBarPop.update_layout(main_config, height=290, template=template)
    figBarPop.update_layout({"margin": {"l": 0, "r": 0, "t": 30, "b": 0}})
    return figBarPop
# ↥ Grafico de barra Aumento populacional ↥=========================================================================================================================================

if __name__ == '__main__':
 app.run_server(debug=True)







