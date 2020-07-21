# https://python-visualization.github.io/folium/modules.html#module-folium.map
import folium
from mainframe import Mainframe
from controller import Controller
import re

mainframe = Mainframe('calgaryTraffic')
mainframe.drop_db()
mainframe.load_data("./data/Traffic_Incidents.csv")
mainframe.load_data("./data/TrafficFlow2016_OpenData.csv")
mainframe.load_data("./data/2017_Traffic_Volume_Flow.csv")
mainframe.load_data("./data/Traffic_Volumes_for_2018.csv")
mainframe.push_data()
ctrl = Controller(mainframe)

CALGARY = (51.0447, -114.0719)
calgary_map = folium.Map(location=CALGARY)


incident_frame = ctrl.get_incident('Traffic_Incidents')

for index, info, desc, date, mod_date, quad, lon, lat, location, count, id in incident_frame.itertuples():
    # print(info, lat, lon, date)
    folium.map.Marker(location=[lat, lon],
                      popup=f'{desc}\n {info}\n {date}\n').add_to(calgary_map)


year = '2016'
volume_frame = ctrl.get_volume(year, sort=True)

for secname, the_geom, year_vol, shape_len, volume in volume_frame.itertuples(index=False):
    # print(the_geom, shape_len, volume)
    point_cloud = []
    location = re.search(r'\(\((.*?)\)\)', the_geom)
    for loc in location.groups(1):
        loc = loc.split(',')
        for point in loc:
            point = point.strip().split(' ')
            lon = point[0]
            lat = point[1]
            point_cloud.append([lat, lon])
    print(point_cloud, volume)
    polyline = folium.polyline(
        locations=point_cloud, tooltip=volume).add_to(calgary_map)

calgary_map.save('map.html', zoom_start=10)

# print(location.groups(0))

# for coords, info in geo_data.get('location'), geo_data.get('INCIDENT INFO'):
#     print(coords, info)
# # lat = entry.split(',')[0][1:]
# # longitude = entry.split(',')[1][:-1]
# # folium.Marker([lat, lon],)
