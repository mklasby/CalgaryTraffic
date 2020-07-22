# create map.py
# https://python-visualization.github.io/folium/modules.html#module-folium.map
# NOT USED
import folium
from mainframe import Mainframe
from controller import Controller

mainframe = Mainframe('calgaryTraffic')
mainframe.drop_db()
mainframe.load_data("./data/Traffic_Incidents.csv")
mainframe.load_data("./data/TrafficFlow2016_OpenData.csv")
mainframe.load_data("./data/2017_Traffic_Volume_Flow.csv")
mainframe.load_data("./data/Traffic_Volumes_for_2018.csv")
mainframe.push_data()
ctrl = Controller(mainframe)

CALGARY = (51.0447, -114.0719)
could
calgary_map = folium.Map(location=CALGARY)


incident_frame = ctrl.get_incident('Traffic_Incidents')

for index, info, desc, date, mod_date, quad, lon, lat, location, count, id in incident_frame.itertuples():
    print(info, lat, lon, date)
    folium.map.Marker(location=[lat, lon],
                      popup=f'{desc}\n {info}\n {date}\n').add_to(calgary_map)

calgary_map.save('map.html', zoom_start=10)
