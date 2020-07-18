# app.py - view

from mainframe import Mainframe
from controller import Controller
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# external style sheet url: https://bootswatch.com/cyborg/
# sidebar GUI design tutorial: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

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
content = html.Div(id="content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# if pathname == '/':
#     return html.P('root page!')

# )
# def toggle_active_links(pathname):
#     if pathname == "/":
#         # Treat page 1 as the homepage / index
#         return True, False, False
#     return [pathname == f"/page-{i}" for i in range(1, 4)]
# @ app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname in ["/", "/page-1"]:
#         return html.P("This is the content of page 1!")
#     elif pathname == "/page-2":
#         return html.P("This is the content of page 2. Yay!")
#     elif pathname == "/page-3":
#         return html.P("Oh cool, this is page 3!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )
# app = dash.Dash(__name__)
# app.layout = html.Div([html.Label('Dropdown'),
#                        dcc.Dropdown(
#     options=[
#         {"label": "Volume", "value": "vol"},
#         {"label": "Incidents", "value": "inc"},
#     ],
#     value='vol'
# ),
#     html.Label('Multi-Select Dropdown'),
#     dcc.Dropdown(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value=['MTL', 'SF'],
#         multi=True
# ),
#     html.Label('Radio Items'),
#     dcc.RadioItems(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value='MTL'
# ),
#     html.Label('Checkboxes'),
#     dcc.Checklist(
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': u'Montréal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value=['MTL', 'SF']
# ),
#     html.Label('Text Input'),
#     dcc.Input(value='MTL', type='text'),
#     html.Label('Slider'),
#     dcc.Slider(
#         min=0,
#         max=9,
#         marks={i: 'Label {}'.format(i) if i == 1 else str(i)
#                for i in range(1, 6)},
#         value=5,
# ),
# ], style={'columnCount': 2})


def main():
    app.run_server(debug=True)

    # mainframe= Mainframe("calgaryTraffic")
    # mainframe.drop_db()
    # mainframe.load_data("Traffic_Incidents.csv")
    # mainframe.load_data("TrafficFlow2016_OpenData.csv")
    # mainframe.load_data("2017_Traffic_Volume_Flow.csv")
    # mainframe.load_data("Traffic_Volumes_for_2018.csv")
    # mainframe.push_data()
    # ctrl= Controller(mainframe)
    # vol16= ctrl.get_volume("2016")
    # print(vol16)
    # vol17= ctrl.get_volume("2017")
    # print(vol17)
    # vol18= ctrl.get_volume("2018")
    # print(vol18)
    # inc16= ctrl.get_incident("incidents", "2016")
    # print(inc16)
    # inc17= ctrl.get_incident("incidents", "2017")
    # print(inc17)

    # html_out= vol16.to_html()
    # print(html_out)


if __name__ == "__main__":
    print("Running app.main()...\n")
    main()
