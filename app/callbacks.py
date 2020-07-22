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


# # update analysis_view
# @ app.callback(
#     Output('analysis_view', 'children'),
#     [Input('data_selection', 'value')])
# def update_analysis_view(data):
#     if data == 'inc':
#         inc_16 = ctrl.get_incident('Traffic_Incidents', '2016')
#         sum_16 = len(inc_16)
#         inc_17 = ctrl.get_incident('Traffic_Incidents', '2017')
#         sum_17 = len(inc_17)
#         inc_18 = ctrl.get_incident('Traffic_Incidents', '2018')
#         sum_18 = len(inc_18)
#         y_axis_title = 'Total Automobile Incidents'
#     elif data == 'vol':
#         y_axis = "Total "
#         vol_16 = ctrl.get_volume('2016')
#         sum_16 = vol_16.get('volume').sum()
#         vol_17 = ctrl.get_volume('2017')
#         sum_17 = vol_17.get('volume').sum()
#         vol_18 = ctrl.get_volume('2018')
#         sum_18 = vol_18.get('volume').sum()
#         y_axis_title = 'Total Automobile Volume'
#     else:
#         fig = None
#     fig_dict = {'Year': [2016, 2017, 2018],
#                 y_axis_title: [sum_16, sum_17, sum_18]}
#     fig = px.scatter(fig_dict, x='Year', y=y_axis_title, trendline='ols')
#     return dcc.Graph(figure=fig)


# update map view
@ app.callback(
    Output('map_view', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value')])
def update_map(data, year):
    print(f'From map view callback {year} {data}')
    if data == 'inc':
        ctrl.get_inc_map(year=year)
    if data == 'vol':
        ctrl.get_vol_map(year=year)
    return html.Iframe(srcDoc=open(
        './assets/map.html', 'r').read(), height=600, width=900, style={'position': 'absolute'})

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
