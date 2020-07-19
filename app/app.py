import dash
import dash_bootstrap_components as dbc
from mainframe import Mainframe
from controller import Controller

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.CYBORG], suppress_callback_exceptions=True)
server = app.server

mainframe = Mainframe('calgaryTraffic')
mainframe.drop_db()
mainframe.load_data("./data/Traffic_Incidents.csv")
mainframe.load_data("./data/TrafficFlow2016_OpenData.csv")
mainframe.load_data("./data/2017_Traffic_Volume_Flow.csv")
mainframe.load_data("./data/Traffic_Volumes_for_2018.csv")
mainframe.push_data()
ctrl = Controller(mainframe)
