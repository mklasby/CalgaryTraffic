import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "height": "100%",
    "width": "16rem",  # Set the width of the sidebar
    "position": "fixed",  # Fixed Sidebar (stay in place on scroll)
    "z-index": 1,  # Stay on top
    "top": 0,  # Stay at the top
    "left": 0,
    "overflow-x": "hidden",  # Disable horizontal scroll
    "padding": "4rem 2rem",
    "background-color": "#2A9FD6",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "4rem",
    "padding": "4rem 2rem",
}
sidebar = html.Div(
    [
        html.H4("Calgary Traffic Analysis",
                ),
        html.Hr(),
        html.P(
            "ENSF 592 Final Project",
        ),
        dcc.Dropdown(
            id='data_selection',
            options=[
                {'label': 'Traffic Volume', 'value': 'vol'},
                {'label': 'Incidents', 'value': 'inc'},
            ],
            value='vol'
        ),
        dcc.Dropdown(
            id='year_selection',
            options=[
                {'label': '2016', 'value': 2016},
                {'label': '2017', 'value': 2017},
                {'label': '2018', 'value': 2018},
            ],
            value=2016
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
    ],
    style=SIDEBAR_STYLE,
)


# home = html.Div([
#     html.H1("Welcome to the home page"),
#     html.Div(id='content')
#  ], style=CONTENT_STYLE])


home = html.Div(
    [
        html.H4('HOME PAGE'),
        html.Hr(),
        html.Div(id="content"),
    ],
    style=CONTENT_STYLE
)

read_view = html.Div(
    [
        html.H4('READ PAGE'),
        html.Hr(),
        html.Div(id="content"),
    ],
    style=CONTENT_STYLE
)

sort_view = html.Div(
    [
        html.H4('SORT PAGE'),
        html.Hr(),
        html.Div(id="content"),
    ],
    style=CONTENT_STYLE
)

map_view = html.Div(
    [
        html.H4('MAP PAGE'),
        html.Hr(),
        html.Div(id="content"),
    ],
    style=CONTENT_STYLE
)

analysis_view = html.Div(
    [
        html.H4('ANALYSIS PAGE'),
        html.Hr(),
        html.Div(id="content"),
    ],
    style=CONTENT_STYLE
)


layout1 = html.Div([
    html.H3('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2')
],
    style=CONTENT_STYLE,
)

layout2 = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    # html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])
