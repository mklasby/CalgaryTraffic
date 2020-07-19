# create map.py
import folium

CALGARY = (51.0447, -114.0719)

calgary_map = folium.Map(location=CALGARY)

calgary_map.save('map.html', zoom_start=100)
