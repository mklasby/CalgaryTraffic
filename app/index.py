import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, mainframe, ctrl
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
    # '''NOTE: if running server in debug mode,the db will be loaded on each 'hot update'''
    # mainframe = callbacks.load_data(
    #     'calgaryTraffic')  # inits DB and controler object
    print(mainframe)
    app.run_server(debug=True)
