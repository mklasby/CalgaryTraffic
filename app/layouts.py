# Views

from mainframe import Mainframe
from controller import Controller
from app import mainframe, ctrl
import folium as fm
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

SIDEBAR_STYLE = {
    'height': '100%',
    'width': '16rem',  # Set the width of the sidebar
    'position': 'fixed',  # Fixed Sidebar (stay in place on scroll)
    'z-index': 1,  # Stay on top
    'top': 0,  # Stay at the top
    'left': 0,
    'overflow-x': 'hidden',  # Disable horizontal scroll
    'padding': '4rem 2rem',
    'background-color': '#2A9FD6',
}

CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '4rem',
    'padding': '4rem 2rem',
}
sidebar = html.Div(
    [
        html.H4('Calgary Traffic Analysis',
                ),
        html.Hr(),
        html.P(
            [
                'ENSF 592 Final Project', html.Br(), 'By: Mike Lasby'],
            style={'color': 'white'}
        ),
        dcc.Dropdown(
            id='data_selection',
            options=[
                {'label': 'Traffic Volume', 'value': 'vol'},
                {'label': 'Incidents', 'value': 'inc'},
            ],
            value='inc',
        ),
        dcc.Dropdown(
            id='year_selection',
            options=[
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
            ],
            value='2016'
        ),
        dbc.Nav(
            [
                dbc.NavLink('Read Data', href='/read', id='read'),
                dbc.NavLink('Sorted Data Table', href='/sort', id='sort'),
                dbc.NavLink('Data Analysis', href='/analysis', id='analysis'),
                dbc.NavLink('Map View', href='/map', id='map'),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div([
            dbc.Alert(
                'WELCOME',
                id='status_bar',
                color='success',
            ),
            html.Div(id='alert_container'),
        ]),

        # HIDDEN DIV USED TO STORE FILTERED DATA ACROSS PAGES
        # SEE: https://dash.plotly.com/sharing-data-between-callbacks
        html.Div(id='data', style={'display': 'none'})
    ],
    style=SIDEBAR_STYLE,
)

home = html.Div(
    [
        html.H4('HOME PAGE'),
        html.Hr(),
        html.Div(id='content'),
    ],
    style=CONTENT_STYLE
)

read_view = html.Div(
    [
        html.H4('READ PAGE'),
        html.Hr(),
        html.Div(id='read_table')  # container target for callback response
    ],
    style=CONTENT_STYLE
)

sort_view = html.Div(
    [
        html.H4('SORT PAGE'),
        html.Hr(),
        html.Div(id='sort_table'),
    ],
    style=CONTENT_STYLE
)

map_view = html.Div(
    [
        html.H4('MAP PAGE'),
        html.Hr(),
        html.Iframe(id='map_view', srcDoc=open(
            './assets/map.html', 'r').read(), height=600, width=900, style={'position': 'absolute'})
    ],
    style=CONTENT_STYLE
)

analysis_view = html.Div(
    [
        html.H4('ANALYSIS PAGE'),
        html.Hr(),
        html.Div(id='analysis_view'),
    ],
    style=CONTENT_STYLE
)
