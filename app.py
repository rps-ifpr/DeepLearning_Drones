# Dashboard Analítico Interativo de Vendas com Dash em Python

# Execute: pip install -r requirements.txt

# Imports
import dash
import plotly
import locale
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import warnings
warnings.filterwarnings("ignore")

# Carregando os dados
df = pd.read_csv('dados/dataset.csv')

# Cálculo da margem de lucro bruto
df['Margem_Lucro'] = np.multiply(np.divide(df['Lucro'], df['Venda']), 100).round(2)

# Função para agrupamento
def group_by(df,col):

    # Agregação
    grouped = df.groupby(by = col, as_index = False).agg({'Venda':'sum',
                                                          'Lucro':'sum',
                                                          'Quantidade':'sum',
                                                          'Desconto':'mean'})

    # Calculando a margem de lucro
    grouped['Margem_Lucro'] = np.multiply(np.divide(grouped['Lucro'], grouped['Venda']), 100).round(2)
    
    return grouped

# Variáveis para formatação
title_font = {'size':20,'color':'black'}
legend_font = {'size':16,'color':'black'}
global_font = dict(family = "Roboto")

# BoxPlot de desconto vs margem de lucro bruto
figura_1 = px.box(df, 
               x = 'Desconto', 
               y = 'Margem_Lucro',
               title = 'Comportamento da Margem de Lucro Bruto Por Faixa de Desconto',
               labels = {'Desconto':'Desconto do Produto',
                         'Margem_Lucro':'Margem de Lucro Bruto'}).update_traces(marker = {'color':'#3399CC'}).update_layout(height = 500, 
                                                                                                                      width = 900, 
                                                                                                                      title = {'font':title_font, 
                                                                                                                               'x':0.5, 
                                                                                                                               'y':0.9, 
                                                                                                                               'xanchor':'center', 
                                                                                                                               'yanchor':'middle'},
                                                                                                                      font = global_font,
                                                                                                                      legend = {'font':legend_font}, 
                                                                                                                      font_color = 'black',
                                                                                                                      plot_bgcolor = 'rgba(0,0,0,0)',
                                                                                                                      paper_bgcolor = 'rgba(0,0,0,0)')
figura_1.add_hline(y = 0, 
                line_dash = "dot", 
                annotation_text = "Lucro Zero", 
                annotation_position = "bottom right")

figura_1.add_vrect(x0 = 0.35, 
                x1 = 0.45, 
                annotation_text = "Declínio", 
                annotation_position = "top left", 
                fillcolor = "red", 
                opacity = 0.20, 
                line_width = 0)

figura_1.add_vline(x = 0.41, 
                line_width = 1, 
                line_dash = "dash", 
                line_color = "red")
    
# Sunburst Plot
figura_2 = px.sunburst(data_frame = df, 
                    path = ['Categoria', 'Sub-Categoria'], 
                    values = 'Quantidade', 
                    color = 'Lucro', 
                    color_continuous_scale = 'rainbow', 
                    hover_data = {'Quantidade':True, 'Lucro':True},)

figura_2.update_traces(textfont = {'family':'arial'}, 
                    textinfo = 'label+percent entry', 
                    insidetextorientation = 'radial', 
                    marker = {'line':{'color':'black'}})   

figura_2.update_layout(title = {'text':'Quantidade Vendida e Lucro Para Cada Tipo de Produto', 'font':title_font, 'x':0.5, 'y':0.02, 'xanchor':'center', 'yanchor':'bottom'},
                    legend = {'font':legend_font}, 
                    font_color = 'black',
                    font = global_font,
                    plot_bgcolor = 'rgba(0,0,0,0)',
                    paper_bgcolor = 'rgba(0,0,0,0)')

# Função para agrupar os dados por estado
def agrupa_estados(dataframe):

    # Dataframe de estados agrupados
    estados = dataframe.groupby(['Estado', 'Codigo_Estado', 'Regiao'], as_index = False).agg({'Venda':'sum', 
                                                                                              'Lucro':'sum', 
                                                                                              'Desconto':'mean',
                                                                                              'Quantidade':'sum'})
    # Calculando a margem de lucro relativo
    estados['Margem_Lucro'] = np.multiply(np.divide(estados['Lucro'], estados['Venda']), 100).round(2)
    
    # Ordenação
    estados = estados.sort_values('Venda', ascending = False, ignore_index = True)
    
    return estados

# Agrupa os dados por estado
estados_usa = agrupa_estados(df)

# Choropleth Map
us_map = px.choropleth(data_frame = estados_usa,
                       locationmode ='USA-states',
                       locations = 'Codigo_Estado',
                       scope = 'usa',
                       color = 'Margem_Lucro',
                       color_continuous_scale = 'greens_r',
                       color_continuous_midpoint = 0,
                       hover_name = 'Estado',
                       hover_data = {'Estado':False, 'Venda':True, 'Desconto':True, 'Codigo_Estado':False, 'Regiao':True},
                       labels = {'Margem_Lucro':'Margem de Lucro Bruto','Desconto_mean':'Desconto Médio'},)

us_map.update_layout(title = {'text':'Margem de Lucro Bruto - Mapa USA', 'font':title_font, 'x':0.5, 'y':0.9, 'xanchor':'center', 'yanchor':'middle'},
                     font = global_font,
                     font_color = 'black',
                     geo = dict(bgcolor = 'rgba(0,0,0,0)'),
                     paper_bgcolor = 'rgba(0,0,0,0)',
                     plot_bgcolor = 'rgba(0,0,0,0)')


##### App Dash #####

# Criando app dash
app = dash.Dash(__name__, 
                external_stylesheets = [dbc.themes.YETI], 
                suppress_callback_exceptions = True, 
                meta_tags = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

server = app.server


##### Barra Lateral #####

# Componente sidebar
sidebar = html.Div(
    [      
        html.H4("Dashboard Analítico", className = "text-white p-1", style = {'marginTop':'1rem'}),
        html.Hr(style = {"borderTop": "1px dotted white"}),
        dbc.Nav(
            [
                dbc.NavLink("Visão Geral", href="/", active="exact"),
                dbc.NavLink("Análise Financeira", href="/pagina-1", active="exact"),
                dbc.NavLink("Conclusão", href="/pagina-2", active="exact"),
            ],
            vertical = True,
            pills = True,
            style = {'fontSize':16}
        ),
        html.P(u"Versão 1.0", className = 'fixed-bottom text-white p-2'),

    ],
    className = 'bg-dark',

    style = {"position": "fixed",
             "top": 0,
             "left": 0,
             "bottom": 0,
             "width": "14rem",
             "padding": "1rem",},
)


##### Home Page #####

# Tabs Style
tab_style = {'border': '1px solid black', 'padding': '6px', 'fontWeight': 'bold', 'margin':'0.5rem',}
tab_selected_style = {'border': '1px solid white', 'background-color': '#3298CC', 'padding': '6px', 'margin':'0.5rem'}

# Formatar os números decimais
locale.setlocale(locale.LC_ALL, '')

# Container
h_container = dbc.Container(
    [        
        dbc.Row(
            [
                dbc.Col(
                    dcc.Tabs(id = "radio_options",
                             value = 'Transactions',
                             children = [dcc.Tab(label='Total de Transações',
                                                 value='Transactions',
                                                 style=tab_style, 
                                                 selected_style = tab_selected_style,),
                                         dcc.Tab(label = 'Vendas',
                                                 value = 'Venda',
                                                 style = tab_style, 
                                                 selected_style = tab_selected_style,),
                                         dcc.Tab(label = 'Lucro',
                                                 value = 'Lucro', 
                                                 style = tab_style, 
                                                 selected_style  =tab_selected_style,),
                                         dcc.Tab(label = 'Quantidade',
                                                 value = 'Quantidade',
                                                 style = tab_style, 
                                                 selected_style = tab_selected_style,),
                                         dcc.Tab(label = 'Desconto Médio',
                                                 value = 'Desconto',
                                                 style = tab_style, 
                                                 selected_style = tab_selected_style,),
                                      ],
                            )
                )
            ],no_gutters = True, justify = 'around',
        ),       
        
        dbc.Row(
            [     
                dbc.Col(
                    [
                        html.P('Total de Vendas', 
                                style = {'margin':'1rem', 'textAlign':'center', 'border':'1px solid white'},
                                className = 'text-white rounded-lg shadow p-1 bg-dark',
                               ),
                        html.P('R$ {}'.format(str(locale.format("%.4f", df.Venda.sum().round(2), grouping=True))),
                                style = {'textAlign':'center','fontColor':'black'}),
                        
                        html.P('Lucro Total', 
                                style = {'margin':'1rem', 'textAlign':'center', 'border':'1px solid white'},
                                className='text-white rounded-lg shadow p-1 bg-dark',
                               ),
                        html.P('R$ {}'.format(str(locale.format("%.4f", df.Lucro.sum().round(2), grouping=True))),
                                style = {'textAlign':'center','color':'black'}),
                    ],width = 2, style = {"border": "2px solid black", 'borderRight':False},
                ),
                
                dbc.Col(
                    [
                        dcc.Graph(id = 'subplot',figure = {})
                    ],width = {'size':5, 'offset':0}, style = {"border": "2px solid black"},
                ),
                
                dbc.Col(
                    [
                        dcc.Graph(id = 'map',figure = us_map)
                    ],width = {'size':5, 'offset':0}, style = {"border": "2px solid black", 'borderLeft':False})
            ],no_gutters = True, justify = 'around',
        ), 
        
        dbc.Row([
            dbc.Col(dcc.Graph(id = 'bar',figure = {}), style={"border": "2px solid black", 'borderTop':False})
        ],no_gutters = True, justify = 'around',),
    ], fluid = True,
)


##### Layout da Página 1 #####

# Tab style
tab_style = {'border': '1px solid black', 'padding': '6px', 'margin':'1rem', 'fontWeight': 'bold',}
tab_selected_style = {'border':'1px solid white', 'background-color': '#3399CC', 'color':'white', 'margin':'1rem', 'padding': '6px'}

# Container
p1_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([
                    dcc.Graph(id = 'heat', figure = {}),
                    
                    dcc.Tabs(id = "tabs",
                             value = "Lucro",
                             children = [dcc.Tab(label = "Quantidade", value = "Quantidade", style = tab_style,selected_style = tab_selected_style),
                                         dcc.Tab(label = "Lucro", value = "Lucro", style = tab_style, selected_style = tab_selected_style)],
                             vertical = False,)
                ], width = {'size':6},style={"border": "1px solid black",}),
                
                dbc.Col(
                    dcc.Graph(id = 'sunburst', figure = figura_2, responsive = True),
                    width = {'size':6}, style = {"border": "1px solid black",},
                ),
            ],no_gutters = True, justify = 'around',
        ),
        
        dbc.Row(
            [
                    dcc.Graph(id = 'box', figure = figura_1, responsive = True),

            ], no_gutters = True, justify = 'around',
        ),
    ], fluid = True,
)


##### Layout da Página de Insights #####

# Cria os cards

# Card 1
card_main = dbc.Card(
    [
        dbc.CardHeader(html.H4("Insights", className = "card-title"), className = 'bg-primary text-white',),
        dbc.CardBody(
            [         
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("1) Total de 9960 transações."),
                        dbc.ListGroupItem("2) Média de Vendas de R$ 230.14 por transação."),
                        dbc.ListGroupItem("3) Média de Lucro de R$ 28.69 por transação"),
                    ],
                ),
            ], className = 'bg-info',
        ),
    ],
)

# Card 2
card_con = dbc.Card(
    [
        dbc.CardHeader(html.H4("Problemas Detectados", className = "card-title"), className = 'bg-primary text-white',),
        dbc.CardBody(
            [
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("1) A margem de lucro bruto parece estar diminuindo com o aumento do desconto nos produtos."),
                        dbc.ListGroupItem("2) Além de 40% de desconto, a loja sofreu apenas perdas."),
                        dbc.ListGroupItem("3) As quantidades vendidas não estão aumentando com o desconto maior."),
                    ],
                ),
            ],className='bg-info',
        ),
    ],
)

# Card 3
card_final = dbc.Card(
    [
        dbc.CardHeader(html.H4("Conclusão", className = "card-title"), className = 'bg-primary text-white',),
        dbc.CardBody(
            [
                html.P(["A loja tem um bom desempenho quando nenhum desconto ou desconto inferior a 20% é aplicado.", html.Hr(), 
                        "A loja pode se beneficiar reduzindo o desconto em itens de produtos deficitários.", html.Hr(),
                        "O marketing e a propaganda em regiões com menor base de clientes podem ajudar a aumentar a presença da marca.",               
                ],
                    className = "card-text",
                ),
            ],className = 'bg-info',
        ),
        
        dbc.CardLink("Suporte", className = 'text-center font-weight-bold', href = "https://www.datascienceacademy.com.br")
    ],
    color = 'primary',
    outline = True,
)

# Container
p2_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(card_main, width = {'size':4,'offset':1}, style={'marginTop':'2rem'}),
                dbc.Col(card_con, width = {'size':4,'offset':1}, style={'marginTop':'2rem'}),
            ], no_gutters = True, justify = "around"
        ),
        
        dbc.Row(
            [
                dbc.Col(card_final, width = {'size':6}, style={'marginTop':'2rem', 'marginBottom':'2rem'}),
            ], no_gutters=True,justify="around"
        ),
    ]
)


##### Layout Principal #####

CONTENT_STYLE = {"marginLeft": "13rem",
                 "margin-right": "1rem",
                 "padding": "0rem 0rem",
                 'background-color':'#F0F4F5',}

content = html.Div(id = "page-content", children = [], style = CONTENT_STYLE )


##### Layout Geral #####

app.layout = html.Div(
    [
        dcc.Location(id = "url"),
        sidebar,
        content
    ]
)


### App Callback Functions ###

# Calback para renderização das páginas
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return [h_container]
    elif pathname == "/pagina-1":
        return [p1_container,]
    elif pathname == "/pagina-2":
        return [p2_container,]

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"O caminho {pathname} não foi reconhecido..."),
        ]
    )

# Callback para update dos gráficos de barras
@app.callback(
    [Output(component_id = 'subplot', component_property = 'figure'),
     Output(component_id = 'bar', component_property = 'figure'),],
    [Input(component_id = 'radio_options', component_property = 'value')]
)

# Função para update do layout
def update_output(option):
    
    dff = df.copy()

    dff.round(2)
    
    if option == 'Transactions':
        
        fig = make_subplots(rows = 2, cols = 2, shared_yaxes = True)
        
        fig.add_trace(go.Histogram(x = dff['Tipo Entrega'], name = 'Tipo Entrega'), row = 1, col = 1)
        
        fig.add_trace(go.Histogram(x = dff['Segmento'], name = 'Segmento'), row = 1, col = 2)
        
        fig.add_trace(go.Histogram(x = dff['Regiao'], name = 'Região'), row = 2, col = 1)
        
        fig.add_trace(go.Histogram(x = dff['Categoria'], name = 'Categoria de Produto'), row = 2, col = 2)
        
    else:
        fig = make_subplots(rows = 2, cols = 2, shared_yaxes = True)
        
        ship = group_by(dff,'Tipo Entrega') 
        
        fig.add_trace(go.Bar(x = ship['Tipo Entrega'], y = ship[option], name = 'Tipo Entrega'), row = 1, col = 1)
        
        seg = group_by(dff,'Segmento')
        
        fig.add_trace(go.Bar(x = seg['Segmento'], y = seg[option], name = 'Segmento'), row = 1, col = 2)
        
        reg = group_by(dff,'Regiao')
        
        fig.add_trace(go.Bar(x = reg['Regiao'], y = reg[option], name = 'Região'), row = 2, col = 1)
        
        cat = group_by(dff,'Categoria')
        
        fig.add_trace(go.Bar(x = cat['Categoria'], y = cat[option], name = 'Categoria de Produto'), row = 2, col = 2)
        
    fig.update_layout(legend = dict(orientation = "h",
                                    yanchor="bottom", y=1.2, 
                                    xanchor="left",x=0),
                      font = global_font,
                      font_color = 'black',
                      paper_bgcolor = 'rgba(0,0,0,0)', 
                      plot_bgcolor = 'rgba(0,0,0,0)')
    
    if option=='Transactions':
        option='Venda'
        
    figura_3 = px.bar(data_frame = estados_usa, 
                   x = 'Estado', 
                   y = option, 
                   color='Margem_Lucro', 
                   color_continuous_scale = 'blues_r',
                   color_continuous_midpoint = 0,
                   title = ('{} Através dos Estados Americanos'.format(option))).update_traces(marker_line_color = 'rgb(8,48,107)',
                                                                                               marker_line_width = 1).update_layout(title = {'font':title_font, 'x':0.5, 'y':0.9, 'xanchor':'center', 'yanchor':'middle'},
                                                                                                                                    font = global_font,
                                                                                                                                    legend = {'font':legend_font}, 
                                                                                                                                    font_color = 'black',
                                                                                                                                    paper_bgcolor = 'rgba(0,0,0,0)', 
                                                                                                                                    plot_bgcolor = 'rgba(0,0,0,0)')
    
    return fig, figura_3

# Callback do mapa de calor (gráfico de pixels)
@app.callback(Output(component_id = 'heat', component_property = 'figure'), [Input(component_id = 'tabs', component_property = 'value')])

def update_output(tab):
    dff = df.copy()
    dff['Margem_Lucro'] = np.multiply(np.divide(dff['Lucro'],dff['Venda']),100).round(2)
    dff.round(2)
    
    pro = pd.crosstab(index = dff['Desconto'], columns = dff['Sub-Categoria'], values = dff[tab], aggfunc = np.sum )
    
    figura_3 = px.imshow(pro, 
                      color_continuous_scale = 'greens_r', 
                      title = '{} em Toda a Gama de Descontos em Produtos'.format(tab),
                      labels = {'color':tab}
                    ).update_layout(title = {'font':title_font, 
                                             'x':0.5, 'y':0.9,
                                             'xanchor':'center', 'yanchor':'middle'},
                                    font = global_font,
                                    legend = {'font':legend_font}, 
                                    font_color = 'black',
                                    plot_bgcolor = 'rgba(0,0,0,0)',
                                    paper_bgcolor = 'rgba(0,0,0,0)')
    
    return figura_3
    
# Executa a app
if __name__=='__main__':
    app.run_server(debug = False, use_reloader = False)  





