'''FRONTEND NAVIGATION AND APP ENTRY POINT
Entry module for app. Index will be called on entry to home page. Starts flask
server and acts as router to generate new page-content on input from NavLinks in 
layouts.py
See: See dash user guide: https://dash.plotly.com/
App layout based on: https://dash.plotly.com/urls
TODO: Add __init__.py to load index if app is packaged as module 
NOTE: Total lines of code for complete project: 858
'''
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, ctrl
from layouts import *
import callbacks


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return sidebar, home
    elif pathname == '/read':
        return sidebar, read_view
    elif pathname == '/sort':
        return sidebar, sort_view
    elif pathname == '/analysis':
        return sidebar, analysis_view
    elif pathname == '/map':
        return sidebar, map_view
    else:
        return '404'


if __name__ == '__main__':
    '''NOTE: if running server in debug mode,the db will be loaded on each 'hot update'''
    app.run_server(debug=False)
