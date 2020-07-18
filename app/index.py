import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from mainframe import Mainframe
from controller import Controller
from app import app
from layouts import *
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
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
    elif pathname == '/apps/app1':
        return layout1
    elif pathname == '/apps/app2':
        return layout2
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
    mainframe = Mainframe("calgaryTraffic")
    mainframe.drop_db()
    mainframe.load_data("Traffic_Incidents.csv")
    mainframe.load_data("TrafficFlow2016_OpenData.csv")
    mainframe.load_data("2017_Traffic_Volume_Flow.csv")
    mainframe.load_data("Traffic_Volumes_for_2018.csv")
    mainframe.push_data()
    ctrl = Controller(mainframe)
