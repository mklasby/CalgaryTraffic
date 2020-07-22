# https://python-visualization.github.io/folium/modules.html#module-folium.map
# NOT USED
import folium
from mainframe import Mainframe
from controller import Controller
import re

CALGARY = (51.0447, -114.0719)


def rgb_to_hex(rgb):
    '''Method converts (r,g,b) to hex color'''
    return '#'+'%02x%02x%02x' % rgb  # '%' format operator, '02x' hexadecimal form. This line says get hexidecimal by parsing three items from tuple


def get_inc_map(ctrl, year='2016'):
    '''get incidents map
    @args: ctrl of mainframe to be used, year: str
    @return folium map NOTE: front end will simply pull up view that this script writes to.
    '''
    calgary_map = folium.Map(location=CALGARY)
    incident_frame = ctrl.get_incident('Traffic_Incidents')
    for index, info, desc, date, mod_date, quad, lon, lat, location, count, id in incident_frame.itertuples():
        # print(info, lat, lon, date)
        folium.map.Marker(location=[lat, lon],
                          popup=f'{desc}\n {info}\n {date}\n').add_to(calgary_map)
    calgary_map.save('./assets/map.html', zoom_start=10)
    return calgary_map


def get_vol_map(ctrl, year='2016'):
    '''get volume map
    @args: ctrl of mainframe to be used: Controller, year: str
    @return folium map NOTE: front end will simply render map.html from assets
    '''
    calgary_map = folium.Map(location=CALGARY)
    volume_frame = ctrl.get_volume(year, sort=True)
    color_increments = 256  # 0-255
    color_steps = len(volume_frame)  # number of data entries
    n_color = color_steps // color_increments  # change color every n_color steps
    step_counter = 0
    r = 255  # since we sorted above, the largest volume will be red, green lightest volume
    g = 0
    b = 0

    for index, items in volume_frame.iterrows():
        secname = items['secname']
        volume = items['volume']
        the_geom = items['the_geom']
        year = items['year_vol']
        if step_counter > n_color:  # Check if we need to change color
            r -= 1
            g += 1
            step_counter = 0
        point_cloud = []
        color = rgb_to_hex((r, g, b))
        location = re.search(r'\(\((.*?)\)\)', the_geom)
        for loc in location.groups(1):
            loc = loc.split(',')
            for point in loc:
                point = point.strip().split(' ')
                lon = point[0].strip(')').strip('(')
                lon = float(lon)
                lat = point[1].strip('(').strip(')')
                lat = float(lat)
                point_cloud.append([lat, lon])
        polyline = folium.PolyLine(
            locations=point_cloud, tooltip=f'{secname}\n {volume} number of cars in {year}', color=color).add_to(calgary_map)
        step_counter += 1
    calgary_map.save('./assets/map.html', zoom_start=10)
    return calgary_map


if __name__ == '__main__':
    print("Running folium_helpers.main()....")
    mainframe = Mainframe('calgaryTraffic')
    mainframe.drop_db()
    mainframe.load_data("./data/Traffic_Incidents.csv")
    mainframe.load_data("./data/TrafficFlow2016_OpenData.csv")
    mainframe.load_data("./data/2017_Traffic_Volume_Flow.csv")
    mainframe.load_data("./data/Traffic_Volumes_for_2018.csv")
    mainframe.push_data()
    ctrl = Controller(mainframe)
    # get_inc_map('2018')
    get_vol_map(ctrl, '2018')
