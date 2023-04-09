import ssl
import dash
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.offline as py
import plotly.colors as colors
import plotly.graph_objs as go
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash import Input, Output
import dash_bootstrap_components as dbc

colorscale = colors.sequential.RdBu
ssl._create_default_https_context = ssl._create_unverified_context


###################################################### Data ##############################################################
# load data
path = "https://raw.githubusercontent.com/AnaOttavi/Data_Visualization_Project/master/"
df = pd.read_csv(path + 'dataset.csv')

########################################## Plots #####################################################################

# Image of Seattle Fig
fig = go.Figure()
# Constants
img_width = 2850
img_height = 700
scale_factor = 0.5
# This trace is added to help the autoresize logic work.
fig.add_trace(
    go.Scatter(x=[0, img_width * scale_factor], y=[0, img_height * scale_factor], mode="markers", marker_opacity=0))
# Axes
fig.update_xaxes(visible=False, range=[0, img_width * scale_factor])
fig.update_yaxes(visible=False, range=[0, img_height * scale_factor], scaleanchor="x")
fig.add_layout_image(
    dict(
        x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source="https://raw.githubusercontent.com/AnaOttavi/Data_Visualization_Project/master/seattle.jpg")
)
# Layout
fig.update_layout(
    width=img_width * scale_factor,
    height=img_height * scale_factor,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)
# ------------------------------
# Line Chart - Fig 1
df1 = df[['price', 'yr_built']].groupby('yr_built').mean().reset_index()
fig1 = px.line(df1, x="yr_built", y="price", color_discrete_sequence=['#6f83a7'], height=300, width=1150)
fig1.update_layout(plot_bgcolor='rgb(255,255,255)')
fig1.update_xaxes(title='Year Built')
fig1.update_yaxes(title='Price')

# ScatterPlot Fig 3
fig3 = px.scatter(df, x="bathrooms", y="price", color="price", size='sqft_living')
fig3.update_layout(height=400, width=900)

# BarChart Condition Fig4
df['condition_'] = df['condition'].apply(lambda x: 'low' if x == 2 else 'medium' if x == 3 or x == 4 else 'high')
df1 = df[['price', 'condition_']].groupby('condition_').mean().reset_index()
fig4 = px.bar(df1, x='condition_', y='price', color_discrete_sequence=['#6f83a7'])
fig4.update_layout(plot_bgcolor='rgb(255,255,255)')
fig4.update_layout(height=450, width=650)
fig4.update_xaxes(title_text="Type of Condition")
fig4.update_yaxes(title_text="Price")

# BarChart Fig5
x_data = df['waterfront']
y_data = df['price']
fig5 = go.Figure(data=[go.Bar(x=x_data, y=y_data)])
fig5.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                   marker_line_width=1.5, opacity=0.6)
fig5.update_layout(height=300, width=650)

###################################################### Interactive Components ############################################
# Interaction between Bedrooms and Bathrooms
dropdown1 = dcc.Dropdown(
    id='x-axis-dropdown',
    options=[
        {'label': 'Bedrooms', 'value': 'bedrooms'},
        {'label': 'Bathrooms', 'value': 'bathrooms'}
    ],
    value='bedrooms',
    clearable=False
)

# Interaction between waterfront and view
dropdown2 = dcc.Dropdown(
    id='x-dropdown',
    options=[
        {'label': 'Waterfront', 'value': 'waterfront'},
        {'label': 'View', 'value': 'view'},
    ],
    value='waterfront',
    clearable=False
)

########################################## Footer #########################################################################

footer = html.Div([html.Div([html.Hr(), html.P(
    '----------Ana Carolina Ottavi nº 20220541-----Carolina Bezerra nº 20220392-----Carolina Confraria nº 20220711-----Daniella Camilato nº 20221641 ---------------------------------- Nova IMS - Master Degree in Data Science and Advanced Analytics---------------------------------',
    style={'font-size': '13px'})], style={'font-size': '13px'})
                   ], style={'position': 'fixed', 'bottom': '0','height': '2,1%', 'width': '100%', 'background-color': '#8c9cc1'})

################################# Dash APP ##################################################################
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([

    # Row 1 Introduction

    html.Div([
        dcc.Graph(figure=fig)
    ], className="six columns"),


    html.Div([
        html.H3('Average prices for the year of construction of the properties',
                style={'color': 'black', 'text-align': 'center', 'fontSize': '20px'}),
        dcc.Graph(id='fig1', figure=fig1)
    ], className='box', style={'width': '85%','height': '400px', 'float': 'right', 'text-align': 'center'}),

    # Price range filter in the map
    html.Div([html.Div([html.Label('Map Price (in millions)'),
                        dcc.RangeSlider(id='price-filter', min=1, max=10, step=0.1, value=[2, 10],
                                        marks={
                                            1: '1M',
                                            2: '2M',
                                            3: '3M',
                                            4: '4M',
                                            5: '5M',
                                            6: '6M',
                                            7: '7M',
                                            8: '8M',
                                            9: '9M',
                                            10: '10M'
                                        })
                        ], className="six columns")
              ], style={'width': '50%', 'margin': 'auto', 'padding-top': '100px'}),

    # Third Row
    # Map
    html.Div([
        html.H3('Location of the houses by price',
                style={'color': 'black', 'text-align': 'center', 'fontSize': '20px'}),
        dcc.Graph(id='scatter-plot'),
    ], className='box', style={'width': '50%', 'float': 'left'}),
    # Scatter Plot
    html.Div([
        html.H3('Relationship between bedrooms or bathrooms per price and sqrt living',
                style={'color': 'black', 'text-align': 'center', 'fontSize': '20px'}),
        dropdown1,
        dcc.Graph(id='fig3', figure=fig3)
    ], className='box', style={'width': '50%', 'float': 'right'}),

    # Fourth Row
    # Mean per condition
    html.Div([
        html.H3('Mean price per condition', style={'color': 'black', 'text-align': 'center', 'fontSize': '20px'}),
        dcc.Graph(id='fig4', figure=fig4),
    ], className='box', style={'width': '55%', 'float': 'right'}),
    #
    html.Div([
        html.H3('Waterfront and View ver price',
                style={'color': 'black', 'text-align': 'center', 'fontSize': '20px'}),
        dropdown2,
        dcc.Graph(id='fig5', figure=fig5),
    ], className='box', style={'width': '45%', 'float': 'right'}),

    # End
    footer
])


#####################################################Callbacks#########################################################
# CallBack ScatterPlot Map Filter
@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    dash.dependencies.Input('price-filter', 'value'))
def update_scatter_plot(price_range):
    # Filter price range
    df_filtered = df[(df['price'] >= price_range[0] * 1000000) & (df['price'] <= price_range[1] * 1000000)]

    # Scatter plot on a Mapbox
    fig = px.scatter_mapbox(df_filtered,
                            lat='lat', lon='long', hover_name='id', hover_data=['price'], size="sqft_living",
                            color='price', zoom=8, height=1000, width=620, color_continuous_scale='RdBu')
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=400, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    # Set the center and zoom level of the Mapbox map
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=47.5015, lon=-121.972),
            style='open-street-map',
            zoom=8.1
        )
    )

    # Return the updated figure
    return fig


# CallBack ScatterPlot
@app.callback(
    Output('fig3', 'figure'),
    Input('x-axis-dropdown', 'value')
)
def update_graph(x_column_name):
    fig = px.scatter(df, x=x_column_name, y='price',
                        color='price', size="sqft_living", color_continuous_scale=colorscale)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)',yaxis_title='Price')
    return fig


# CallBack View/WaterFront
@app.callback(
    Output('fig5', 'figure'),
    Input('x-dropdown', 'value')
)
def update_graph(x_column_name):
    if x_column_name == 'waterfront':
        x_data = df['waterfront'].apply(lambda x: 'Waterfront' if x == 1 else 'Non-Waterfront')
    else:
        x_data = df['view'].apply(lambda x:
                                  'Very Bad' if x == 0 else
                                  'Bad' if x == 1 else
                                  'Satisfactory' if x == 2 else
                                  'Good' if x == 3 else
                                  'Very Good' if x == 4 else 'Very Bad View')
    y_data = df['price']
    fig5 = go.Figure(data=[go.Bar(x=x_data, y=y_data)])
    fig5.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig5.update_layout(height=450, width=650, yaxis_title='Price',xaxis_title='Waterfront/View', plot_bgcolor='rgb(255,255,255)')
    return fig5


# Return the dash
if __name__ == '__main__':
    app.run_server(debug=True)
