import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
from module import filetotable,groupdata
import pandas as pd
file='/Users/jordanlange/Documents/projects/profitanalysis/uploads1/pl.csv'
df=pd.read_csv('/Users/jordanlange/Documents/projects/profitanalysis/uploads1/pl.csv')

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='input',
        options=[
            {'label': "test", 'value': "test"},
            {'label': "test2", 'value': "test2"}
        ]),
    html.Div(id='output'),
    html.H3("Explore Your Transaction Data"),
    dcc.Graph(id='transaction-graph',
    figure={
        'data':[
            {'x':df['Account'],'y':df['Amount'],'type':'bar','name':'pl'}
            ],
        'layout':{
            'title':'Transactional Analysis'
            }
        })
])

@app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='input',component_property='value')])


def update_value(input_group,input_sum):
    return dcc.Graph(
        id='example-graph',
        figure=groupdata(file,input_group,input_sum)
    )
    #return "Input: {}".format(input_data)








#  dcc.Dropdown(
#         id='my-dropdown',
#         options=[
#             {'label':'Coke','value':'COKE'},
#             {'label':'Tesla','value':'TSLA'},
#             {'label':'Apple','value':'AAPL'}
#         ],
#         value='COKE'
#     ),
# @app.react('my-graph',['my-dropdown'])
# def updategraph(dropdown_properties):
#     selected_value=dropdown_properties['value']

#     df=web.DataReader(
#         dropdown_properties['value'],'yahoo',
#         dt(2016,1,1), dt.now()
#     )
#     return {
#         'figure': go.Figure( 
#             data=[
#                 Scatter(
#                     x=df.index,
#                     y=df.Close,
#                     name=selected_value
#                 )
#             ]
#         )
#     }


app.run_server(debug=True, use_reloader=False)