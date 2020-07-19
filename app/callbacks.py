from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from app import app, mainframe, ctrl
import pandas as pd
import plotly.express as px


# # error catching. Display to status bar
# @app.server.errorhandler(Exception)
# def error_handler(e):
#     return "<h1>ERROR!</h1>"


@app.callback(
    Output('content', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'), ])
def display_selection(data, year):
    return f"You have selected {data} for {year}"


# if dropdown selections are changed, get current values of selections and return to hidden data Div
@app.callback(
    Output('data', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'),
     ])
def update_data(data, year):
    if (data or year) == None:
        #raise dash.exceptions.PreventUpdate
        return dash.no_update()
    elif data == 'inc':
        filtered_data = ctrl.get_incident('Traffic_Incidents', year)
    elif data == 'vol':
        filtered_data = ctrl.get_volume(year)
    return filtered_data.to_json(date_format='iso', orient='split')


# update read_table
@app.callback(
    Output('read_table', 'children'),
    [Input('data', 'children')])
def update_read_table(filtered_data):
    if filtered_data == None:
        print("No filtered_data")
        return dash.no_update()
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


# update analysis_view
@app.callback(
    Output('analysis_view', 'children'),
    [Input('data_selection', 'value')])
def update_analysis_view(data):
    if data == 'inc':
        inc_16 = ctrl.get_incident('Traffic_Incidents', '2016')
        sum_16 = len(inc_16)
        inc_17 = ctrl.get_incident('Traffic_Incidents', '2017')
        sum_17 = len(inc_17)
        inc_18 = ctrl.get_incident('Traffic_Incidents', '2018')
        sum_18 = len(inc_18)
        y_axis_title = 'Total Automobile Incidents'
    elif data == 'vol':
        y_axis = "Total "
        vol_16 = ctrl.get_volume('2016')
        sum_16 = vol_16.get('volume').sum()
        vol_17 = ctrl.get_volume('2017')
        sum_17 = vol_17.get('volume').sum()
        vol_18 = ctrl.get_volume('2018')
        sum_18 = vol_18.get('volume').sum()
        y_axis_title = 'Total Automobile Volume'
    else:
        fig = None
    fig_dict = {'Year': [2016, 2017, 2018],
                y_axis_title: [sum_16, sum_17, sum_18]}
    fig = px.scatter(fig_dict, x='Year', y=y_axis_title, trendline='ols')
    return dcc.Graph(figure=fig)

# update status bar depending on page
# TODO: Add exception handling


@app.callback(Output('status_bar', 'children'),
              [Input('url', 'pathname'),
               Input('data_selection', 'value'),
               Input('year_selection', 'value')])
def display_page(pathname, data, year):
    if (year or data) == None or (year or data) == "":
        return "PLEASE SELECT A TYPE OF DATA AND YEAR", {'color': 'danger'}
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
