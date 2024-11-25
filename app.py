from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
import plotly.express as px

meta = pd.read_csv('metadata.csv')
df = pd.read_csv('data.csv', dtype={'id_entidad':str}, index_col=['var', 'id_entidad'])
gdf = gpd.read_file('geo.gpkg')
gdf = gdf.set_index('id_entidad', drop=False)
last_year = pd.to_numeric(df.columns).max()

img_datos = []
for img in meta.loc[:3, 'img']:
    img_datos.append(
        html.Div(
            html.Img(src=f'{img}', className='resumen_img'),
            className='resumen_col'
        )
    )

text_datos = []
for var_name in meta.loc[:3, 'var_name']:
    text_datos.append(
        html.Div(
            var_name,
            className='resumen_text'
        )
    )

cont_datos = [
    html.Div(id='text-acci', className='resumen_cont'),
    html.Div(id='text-vict', className='resumen_cont'),
    html.Div(id='text-peat', className='resumen_cont'),
    html.Div(id='text-cicl', className='resumen_cont')
]

fig_datos = [
    html.Div(
        dcc.Graph(id='graph-acci', config={'displayModeBar':False}),
        className='resumen_col'
    ),
    html.Div(
        dcc.Graph(id='graph-fata', config={'displayModeBar':False}),
        className='resumen_col'
    ),
    html.Div(
        dcc.Graph(id='graph-peat', config={'displayModeBar':False}),
        className='resumen_col'
    ),
    html.Div(
        dcc.Graph(id='graph-cicl', config={'displayModeBar':False}),
        className='resumen_col'
    )
]

img_cond = []
for img in meta.loc[4:, 'img']:
    img_cond.append(
        html.Div(
            html.Img(src=f'{img}', className='resumen_img'),
            className='resumen_col'
        )
    )

text_cond = []
for var_name in meta.loc[4:, 'var_name']:
    text_cond.append(
        html.Div(
            var_name,
            className='resumen_text'
        )
    )

cont_cond = [
    html.Div(id='text-cint', className='resumen_cont'),
    html.Div(id='text-alie', className='resumen_cont'),
    html.Div(id='text-edad', className='resumen_cont'),
    html.Div(id='text-sexo', className='resumen_cont')
]

fig_cond = [
    html.Div(
        dcc.Graph(id='graph-cint', config={'displayModeBar':False}),
        className='resumen_col'
    ),
    html.Div(
        dcc.Graph(id='graph-alie', config={'displayModeBar':False}),
        className='resumen_col'
    ),
    html.Div(
        dcc.Graph(id='graph-edad', config={'displayModeBar':False}),
        className='resumen_col'
    ),
    html.Div(
        dcc.Graph(id='graph-sexo', config={'displayModeBar':False}),
        className='resumen_col'
    )
]

tab1_resumen = html.Div(
    children=[
        html.Div(dcc.Slider(min=1997, max=last_year, step=1,
                            marks={i:str(i) for i in range(1997, last_year+1)},
                            value=last_year,
                            id='dropdown-anio')),
        html.Div('Datos de colisiones con víctimas fatales', className='title'),
        html.Div(img_datos),
        html.Div(text_datos),
        html.Div(cont_datos),
        html.Div(fig_datos),
        html.Div('Datos de los conductores presuntamente culpables', className='title'),
        html.Div(img_cond),
        html.Div(text_cond),
        html.Div(cont_cond),
        html.Div(fig_cond)
        ]
)

@callback(
    Output('text-acci', 'children'),
    Output('text-vict', 'children'),
    Output('text-peat', 'children'),
    Output('text-cicl', 'children'),
    Output('text-cint', 'children'),
    Output('text-alie', 'children'),
    Output('text-edad', 'children'),
    Output('text-sexo', 'children'),
    Input('dropdown-anio', 'value')
)
def update_cont(anio):
    anio = str(anio)
    cont_acci = '{:,.0f}'.format(df.loc['acci', anio].sum())
    cont_vict = '{:,.0f}'.format(df.loc['fata', anio].sum())
    cont_peat = '{:,.0f}'.format(df.loc['peat', anio].sum())
    cont_cicl = '{:,.0f}'.format(df.loc['cicl', anio].sum())
    cont_cint = '{:,.0f}'.format(df.loc['cint', anio].sum())
    cont_alie = '{:,.0f}'.format(df.loc['alie', anio].sum())
    cont_edad = '{:,.0f}'.format(df.loc['edad', anio].sum())
    cont_sexo = '{:,.0f}'.format(df.loc['sexo', anio].sum())
    return cont_acci, cont_vict, cont_peat, cont_cicl, cont_cint, cont_alie, cont_edad, cont_sexo

@callback(
    Output('graph-acci', 'figure'),
    Output('graph-fata', 'figure'),
    Output('graph-peat', 'figure'),
    Output('graph-cicl', 'figure'),
    Output('graph-cint', 'figure'),
    Output('graph-alie', 'figure'),
    Output('graph-edad', 'figure'),
    Output('graph-sexo', 'figure'),
    Input('dropdown-anio', 'value')
)
def updateFig(anio):
    anio = str(anio)
    fig_acci = figResumen(df.loc['acci'], anio)
    fig_fata = figResumen(df.loc['fata'], anio)
    fig_peat = figResumen(df.loc['acci'], anio)
    fig_cicl = figResumen(df.loc['fata'], anio)
    fig_cint = figResumen(df.loc['cint'], anio)
    fig_alie = figResumen(df.loc['alie'], anio)
    fig_edad = figResumen(df.loc['edad'], anio)
    fig_sexo = figResumen(df.loc['sexo'], anio)
    return fig_acci, fig_fata, fig_peat, fig_cicl, fig_cint, fig_alie, fig_edad, fig_sexo

def figResumen(dff, anio):
    max_val = dff.sum().max()
    min_val = dff.sum().min()
    range = max_val - min_val
    upper = max_val + range * 0.05
    lower = min_val - range * 0.05
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pd.to_numeric(dff.columns), y=dff.sum(), line_color='white', line_width=0.5, showlegend=False))
    fig.add_trace(go.Scatter(x=[int(anio)], y=[dff[anio].sum()], marker_color='pink', showlegend=False))
    fig.update_xaxes(showgrid=False, fixedrange=True, range=[1996.5, last_year+0.5], showticklabels=False)
    fig.update_yaxes(showgrid=False, fixedrange=True, range=[lower, upper], showticklabels=False, zeroline=False)
    fig.update_layout({'plot_bgcolor':'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)',})
    fig.update_layout(height=100, margin_b=0, margin_t=0)
    return fig


#Tab2 Mapa
options = []
for i, j in meta[['var_name', 'var']].values:
    options.append({'label':i, 'value':j})
options_ent = []
for i, j in gdf[['nom_entidad', 'id_entidad']].values:
    options_ent.append({'label':i, 'value':j})

tab2_mapa = [
    html.Div([
        html.Div(className='prueba'),
        html.Div([
            dcc.Slider(
                min=1997, max=last_year, step=1,
                marks={i:str(i) for i in range(1997, last_year+1)},
                value=2022,
                id='slice-mapa'
            )],
            className='prueba1'
        ),
        html.Div(className='prueba')
    ], className='prueba2'
    ),
    html.Div([
        html.Div(className='prueba'),
        html.Div(
            dcc.Dropdown(
                options=options,
                value='acci',
                id='dropdown-mapa'
            ), className='prueba1'
        ),
        html.Div(className='prueba')
        ],
        className='preuba2'
    ),
    html.Div(
        [
            html.Div(
                children=dcc.Graph(id='graph-mapa', config={'displayModeBar':False}),
                className='mapa_mapa',
                style={'vertical-align': 'bottom'}
            ),
            html.Div([
                html.Div([
                    html.Div(className='prueba'),
                    dcc.Dropdown(
                        options=options_ent,
                        value='01',
                        id='dropdown-estado',
                        className='prueba1'
                    ),
                    html.Div(className='prueba')],
                    className='prueba2'
                ),
                html.Div(
                    children=dcc.Graph(id='graph-scatter', config={'displayModeBar':False})
                )
                ],
                className='mapa_scatter'
            )
        ]
    )
]

@callback(
    Output('graph-mapa', 'figure'),
    Input('slice-mapa', 'value'),
    Input('dropdown-mapa', 'value'),
)
def update_mapa(anio, var):
    anio=str(anio)
    dff = df.loc[var]
    fig_mapa = px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color=dff[anio],
        mapbox_style='open-street-map',
        center={'lat':23.5, 'lon':-102},
        zoom=3.3,
        color_continuous_scale='reds'
    )
    fig_mapa.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin={'b':0, 't':0, 'l':0, 'r':0},
        coloraxis_colorbar={
            'title_text':'',
            'title_font':{'color':'white','size':25},
            'tickfont':{'color':'white', 'size':20},
            'bgcolor':'rgba(0, 0, 0, 0)'
        }
    )
    fig_mapa['data'][0]['text'] = gdf['nom_entidad']
    fig_mapa['data'][0]['hovertemplate'] = '<b>%{text}</b><br>%{z}'

    return fig_mapa

@callback(
    Output('graph-scatter', 'figure'),
    Input('slice-mapa', 'value'),
    Input('dropdown-mapa', 'value'),
    Input('dropdown-estado', 'value')
)
def update_scatter(anio, var, estado):
    anio=str(anio)
    dff = df.loc[var]
    fig_scatter = go.Figure()
    fig_scatter.add_trace(
        go.Scatter(
            x=pd.to_numeric(dff.columns),
            y=dff.loc[estado],
            mode='markers',
            marker={'color':'rgb(200, 0, 0)', 'symbol':'0', 'size':8},
        )
    )
    fig_scatter.update_xaxes(
        title={'text':'Año',
               'font':{'color':'white', 'size':20}},
        tickfont={'color':'white', 'size':15},
        fixedrange=True,
        range=[1996.5, last_year+0.5],
        griddash='dot',
        gridwidth=0.01,
        gridcolor='gray',
        showline=True,
    )
    fig_scatter.update_yaxes(
        title={'text':meta.loc[meta['var']==var, 'var_name'].iloc[0],
               'font':{'color':'white', 'size':20}},
        tickfont={'color':'white', 'size':15},
        fixedrange=True,
        range=[0, None],
        griddash='dot',
        gridwidth=0.01,
        gridcolor='gray',
        showline=True,
        zeroline=False
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin={'b':50, 't':50, 'l':50, 'r':50},
    )
    return fig_scatter

# App
app = Dash()
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(
            label='Resumen',
            children=tab1_resumen
        ),
        dcc.Tab(
            label='Mapa',
            children=tab2_mapa
        )
    ]),
    html.Div(id='tabs-with-classes-2')
],
className='body')

if __name__ == '__main__':
    app.run(debug=True)