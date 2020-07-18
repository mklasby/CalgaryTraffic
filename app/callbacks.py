from dash.dependencies import Input, Output
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

# #if read data, then load read page with graph of requested data
# @app.callback(path_name
#     Output('content','children')
# )


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
