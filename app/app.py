'''FRONT END PREREQUISITE
ase module for loading database and dash app
See: https://dash.plotly.com/
App layout based on: https://dash.plotly.com/urls
See footnote from above URL: 
    "It is worth noting that in both of these project structures,
    the Dash instance is defined in a separate app.py, while the entry point for running 
    the app is index.py. This separation is required to avoid circular imports: the files
    containing the callback definitions require access to the Dash app instance however 
    if this were imported from index.py, the initial loading of index.py would 
    ultimately require itself to be already imported, which cannot be satisfied."
'''
import dash
import dash_bootstrap_components as dbc
from mainframe import Mainframe
from controller import Controller

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.CYBORG], suppress_callback_exceptions=True)
server = app.server

# Loading data from csv to MongoDB
mainframe = Mainframe('calgaryTraffic')
mainframe.drop_db()
mainframe.load_data("./data/Traffic_Incidents.csv")
mainframe.load_data("./data/TrafficFlow2016_OpenData.csv")
mainframe.load_data("./data/2017_Traffic_Volume_Flow.csv")
mainframe.load_data("./data/Traffic_Volumes_for_2018.csv")
mainframe.push_data()
ctrl = Controller(mainframe)
