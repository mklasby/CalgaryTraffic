'''
FRONT END DISPATCHER - PART OF CONTROLLER
This module recieves input calls from layout fields and outputs updated data based on user selections
See dash user guide: https://dash.plotly.com/
TODO: Optimize performance with flash-cacheing and memoization. 
See: https://dash.plotly.com/performance 
TODO: Consider pre-rendering map and graphs as static assets. 
'''


from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from app import app, ctrl
import pandas as pd
import plotly.express as px
import dash_html_components as html


# Update Home Page Content
@app.callback(
    Output('content', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     Input('total_switch', 'value'), ])
def display_selection(data, year, switch):
    return f'You have selected {switch} {data} for {year}'


# Update hidden data div based on user dropdown selections
@app.callback(
    Output('data', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     Input('total_switch', 'value'), ])
def update_data(data, year, switch):
    return [switch, data, year]


# NEW READ TABLE
@ app.callback(
    Output('read_table', 'children'),
    [Input('data', 'children')])
def update_read_table(data_children):
    data = ctrl.get_data(data_children)
    table = dbc.Table.from_dataframe(
        data, striped=True, bordered=True, hover=True)
    return table


# new sort table
# If called on annual max option, will be the same as READ view
@app.callback(
    Output('sort_table', 'children'),
    [Input('data', 'children')])
def update_sort_table(data_children):
    data = ctrl.get_data(data_children, True)
    table = dbc.Table.from_dataframe(
        data, striped=True, bordered=True, hover=True)
    return table


# new analysis view
@app.callback(
    Output('analysis_view', 'children'),
    [Input('data', 'children')])
def update_analysis_view(data_children):
    # GET TOP 10 FOR ANNUAL COUNTS
    fig = ctrl.get_fig(data_children, n=10)
    return dcc.Graph(figure=fig, style={'height': '800px', 'width': '1000px'})


# update map view
@ app.callback(
    Output('map_view', 'children'),
    [Input('data', 'children')])
def update_map(data_children):
    ctrl.get_map(data_children, n=10)
    n = 10
    data = data_children[1]
    if data == "inc":
        data = "Automobile Accidents"
    else:
        data = "Automobile Volume"
    year = data_children[2]
    switch = data_children[0]
    if switch == 'total':
        switch = 'Annual Total'
    else:
        switch = "Annual Maximum"
    return (html.H4(f'Map of {switch} {data} by location in {year}'),
            html.Hr(),
            html.Iframe(srcDoc=open(
                './assets/map.html', 'r').read(), height=600, width=1000, style={'position': 'absolute'}))


# update status bar depending on page
@ app.callback(Output('status_bar', 'children'),
               [Input('url', 'pathname'),
                Input('data', 'children')])
def display_page(pathname, data_children):
    switch = data_children[0]
    data = data_children[1]
    year = data_children[2]
    if (year or data or switch) == None or (year or data or switch) == "":
        return "PLEASE SELECT A TYPE OF DATA AND YEAR"
    if pathname == "/":
        return 'WELCOME'
    elif pathname == '/read':
        return 'Data Read Successful'
    elif pathname == '/sort':
        return 'Data Sort Successful'
    elif pathname == '/analysis':
        return 'Analysis Successful'
    elif pathname == '/map':
        return "Map Load Successful"
    else:
        return 'ERROR', {'color': 'danger'}
