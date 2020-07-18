from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app, mainframe, ctrl
import pandas as pd
import plotly.express as px


@app.callback(
    Output('content', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'), ])
def display_selection(data, year):
    return f"You have selected {data} for {year}"


# if URL is changed, get current values of selections and return to hidden data Div
@app.callback(
    Output('data', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     ])
def update_data(data, year):
    if data == 'inc':
        filtered_data = ctrl.get_incident('Traffic_Incidents', year)
    if data == 'vol':
        filtered_data = ctrl.get_volume(year)
    return filtered_data.to_json(date_format='iso', orient='split')


# update read_table
@app.callback(
    Output('read_table', 'children'),
    [Input('data', 'children')])
def update_read_table(filtered_data):
    updated_data = pd.read_json(filtered_data, orient='split')
    table = dbc.Table.from_dataframe(
        updated_data, striped=True, bordered=True, hover=True)
    return table


# update sort_table
@app.callback(
    Output('sort_table', 'children'),
    [Input('data', 'children')])
def update_sort_table(filtered_data):
    updated_data = pd.read_json(filtered_data, orient='split')
    sorted_data = ctrl.sort_volume(updated_data)
    table = dbc.Table.from_dataframe(
        sorted_data, striped=True, bordered=True, hover=True)
    return table


@ app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@ app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
