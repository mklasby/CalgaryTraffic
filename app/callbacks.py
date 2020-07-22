from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from app import app, mainframe, ctrl
import pandas as pd
import plotly.express as px
import dash_html_components as html


# # error catching. Display to status bar
# @app.server.errorhandler(Exception)
# def error_handler(e):
#     return "<h1>ERROR!</h1>"

# Update Home Page Debug Content
# TODO: Update on test_data only
@app.callback(
    Output('content', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     Input('total_switch', 'value'), ])
def display_selection(data, year, switch):
    return f'You have selected {switch} {data} for {year}'


# Update hidden test_data div based on user dropdown selections
# TODO: Change test_data to data
@app.callback(
    Output('test_data', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     Input('total_switch', 'value'), ])
def update_test_data(data, year, switch):
    return [switch, data, year]


# if dropdown selections are changed, get current values of selections and return to hidden data Div
# TODO: DElete
@ app.callback(
    Output('data', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     ])
def update_data(data, year):
    if data == 'inc':
        filtered_data = ctrl.get_incident('Traffic_Incidents', year)
    elif data == 'vol':
        filtered_data = ctrl.get_volume(year)
    return filtered_data.to_json(date_format='iso', orient='split')


# NEW READ TABLE
@ app.callback(
    Output('read_table', 'children'),
    [Input('test_data', 'children')])
def update_read_table(data_children):
    data = ctrl.get_data(data_children)
    table = dbc.Table.from_dataframe(
        data, striped=True, bordered=True, hover=True)
    return table


# new sort table
# If called on annual max option, will be the same as READ view
# TODO: Replace test_data with data
@app.callback(
    Output('sort_table', 'children'),
    [Input('test_data', 'children')])
def update_sort_table(data_children):
    data = ctrl.get_data(data_children, True)
    table = dbc.Table.from_dataframe(
        data, striped=True, bordered=True, hover=True)
    return table


# new analysis view
# TODO: replace test_data with data
@app.callback(
    Output('analysis_view', 'children'),
    [Input('test_data', 'children')])
def update_analysis_view(data_children):
    # GET TOP 10 FOR ANNUAL COUNTS
    fig = ctrl.get_fig(data_children, n=10)
    return dcc.Graph(figure=fig, style={'height': '800px', 'width': '1000px'})


# update map view
# TODO: Update test_data to data
@ app.callback(
    Output('map_view', 'children'),
    [Input('test_data', 'children')])
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
        switch = 'Annual Totals'
    else:
        switch = "Annual Maximum"
    return (html.H4(f'Map of {switch} {data} in {year}'),
            html.Hr(),
            html.Iframe(srcDoc=open(
                './assets/map.html', 'r').read(), height=700, width=1000, style={'position': 'absolute'}))

# update status bar depending on page
# TODO: Add exception handling


@ app.callback(Output('status_bar', 'children'),
               [Input('url', 'pathname'),
                Input('data_selection', 'value'),
                Input('year_selection', 'value')])
def display_page(pathname, data, year):
    if (year or data) == None or (year or data) == "":
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
