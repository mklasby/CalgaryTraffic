# controller.py - controller
'''This module provides app.py with a controller interface to interact with
data model.
'''
import folium
import re
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
CALGARY = (51.0447, -114.0719)


class Controller():
    '''class to act as middle man b/w app and mainframe. Need to be passes these
    as references'''

    def __init__(self, mainframe):
        self.mainframe = mainframe  # mainframe class

    def find_table(self, name):
        '''returns text string of collection name in db'''
        if name == "2016":
            return "TrafficFlow2016_OpenData"
        elif name == "2017":
            return "2017_Traffic_Volume_Flow"
        elif name == "2018":
            return "Traffic_Volumes_for_2018"
        elif name == "incidents" or "Traffic_Incidents" or "inc":
            return "Traffic_Incidents"
        else:
            # TODO: Raise excpetion on bad input / not found
            print("NO YEAR FOUND")
            return -1

    def get_data(self, data_children, sort=False):
        switch = data_children[0]
        data = data_children[1]
        year = data_children[2]

        if data == "inc":
            name = self.find_table(data)
            incidents = self.mainframe.get_collection(name,
                                                      {"START_DT": {'$regex': year}})
            del incidents['Count']
            del incidents['id']
            if switch == 'total':
                if sort:
                    return self.sort_inc(incidents)
                else:
                    return incidents
            else:
                sorted_inc = self.sort_inc(incidents)
                max_inc = self.get_max_inc(sorted_inc)
                return max_inc  # return df of all locations with with counters = to max

        if data == "vol":
            unordered_vol = self.get_volume(year)
            del unordered_vol['year_vol']
            vol = unordered_vol[['secname',
                                 'volume', 'shape_leng', 'the_geom']]
            if switch == 'total':
                if sort:
                    return self.sort_volume(vol)
                else:
                    return vol
            else:
                max_index = vol['volume'].idxmax(axis=0)
                max_vol = pd.DataFrame(vol.loc[max_index, :])
                return max_vol.T  # return df for max entry

    def get_max_inc(self, sorted_inc):
        '''returns dataframe object with only entries for maximum incidents'''
        max_inc_list = []
        max_counter = sorted_inc['Number of Accidents'].max()
        for index, item in sorted_inc.iterrows():
            if item['Number of Accidents'] >= max_counter:
                max_inc_list.append(item)
        max_inc = pd.DataFrame(max_inc_list)
        return max_inc

    def get_volume(self, year, sort=False):
        '''returns pd.DataFrame object of volume for requested year'''
        name = self.find_table(year)
        vol = self.mainframe.get_collection(name)
        return vol

    def sort_volume(self, vol):
        vol = vol.sort_values(by='volume', ascending=False)
        print('Sorted Collection by volume')
        return vol

    def get_incident(self, name='incidents', year='2016', sort=False):
        name = self.find_table(name)
        if year == 'all':
            incidents = self.mainframe.get_collection(name)
        else:
            incidents = self.mainframe.get_collection(
                name, {"START_DT": {'$regex': year}})
        if sort:
            self.sort_inc(self, incidents)
        return incidents

    def sort_inc(self, incidents):
        dict_hist = {}
        # TODO: combine these loops by reassigning cell value every loop
        for index, item in incidents.iterrows():
            info = item['INCIDENT INFO']
            dict_hist[info] = dict_hist.get(info, 0)+1
        incidents.insert(1, 'Number of Accidents', "")
        for index, item in incidents.iterrows():
            incidents.at[index, 'Number of Accidents'] = dict_hist.get(
                item['INCIDENT INFO'])
        incidents = incidents.sort_values(
            by=['Number of Accidents', 'INCIDENT INFO'], ascending=False)
        print('Sorted Collection by number of accidents')
        return incidents

    def get_view(self, df, name="temp.html"):
        return df.to_html(name)

    def find_worst_inter(self, year):
        data = self.mainframe.get_collection(
            "Traffic_Incidents", {'START_DT': {'$regex': year}})

        info = data.get("INCIDENT INFO")
        hist = {}
        for index, content in info.items():
            hist[content] = hist.get(content, 0) + 1
        sorted_hist = {k: v for k, v in sorted(
            hist.items(), key=lambda x: x[1], reverse=True)}
        print(list(sorted_hist.items())[:10])
        print('\n')

    def get_fig(self, data_children, n):
        switch = data_children[0]
        data = data_children[1]
        year = data_children[2]

        if switch == 'max':
            data_table = self.get_data(('total', data, year))
            if data == 'inc':
                data_table = self.sort_inc(data_table)
                top = {}
                for index, item in data_table.iterrows():
                    if len(top) == n:
                        break
                    if item['INCIDENT INFO'] in top:
                        continue
                    else:
                        top[item['INCIDENT INFO']] = item['Number of Accidents']
                fig_dict = {'Number of Accidents': list(top.values()),
                            'Incident Info': list(top.keys())}
                fig = px.bar(fig_dict, x='Incident Info',
                             y='Number of Accidents', title=f"Top {n} most dangerous locations to be driving in Calgary in {year}")
                return fig
            if data == 'vol':
                data_table = self.sort_volume(data_table)
                top = {}
                for index, item in data_table.iterrows():
                    if len(top) == n:
                        break
                    top[item['secname']] = item['volume']
                fig_dict = {'Sector Name': list(
                    top.keys()), 'Volume - Annual Vehicle Trips': list(top.values())}
                fig = px.bar(fig_dict, x='Sector Name', y='Volume - Annual Vehicle Trips',
                             title=f'Busiest roads in Calgary in {year}')
                return fig

        else:  # switch = totals, get top result and that result from each year
            # will return single row DF for vol or multi-row DF for inc
            this_year = self.get_data(
                ('total', data, year), True)  # sorted df
            data_16 = self.get_data(('total', data, '2016'), True)
            data_17 = self.get_data(('total', data, '2017'), True)
            data_18 = self.get_data(('total', data, '2018'), True)
            years = [data_16, data_17, data_18]
            top = {}
            if data == 'inc':
                for index, item in this_year.iterrows():
                    if len(top) >= 10:  # get top ten
                        break
                    if item['INCIDENT INFO'] in top:
                        continue
                    else:
                        # {info: {year:value}}
                        top[item['INCIDENT INFO']] = {
                            year: item["Number of Accidents"]}
                year_index = 2015
                for date in years:
                    year_index += 1
                    print(f'checking {year_index}')
                    if year_index > 2018:
                        break
                    for index, item in date.iterrows():
                        if item['INCIDENT INFO'] in top:
                            print(
                                f"match on {item['INCIDENT INFO']} from {year_index}")
                            if str(year_index) in top[item['INCIDENT INFO']]:
                                print(
                                    f"found {year_index} in {top[item['INCIDENT INFO']]}, skipping...")
                                continue
                            else:
                                top[item['INCIDENT INFO']][str(
                                    year_index)] = item['Number of Accidents']
                fig = go.Figure()
                print(year)
                for info in list(top.keys()):
                    fig_dict = {
                        'Year': list(top[info].keys()), 'Number of Accidents': list(top[info].values())}
                    fig.add_trace(go.Scatter(
                        x=fig_dict['Year'], y=fig_dict['Number of Accidents'], name=info, hoverinfo='all'))
                fig.update_layout(title=f'Most dangerous locations to be driving in Calgary in {year} plotted from 2016-2018',
                                  xaxis_title='Year', yaxis_title='Number of Accidents', legend_title='Incident Info')
                return fig
            else:  # data == volume TODO
                return None

    def rgb_to_hex(self, rgb):
        '''Method converts (r,g,b) to hex color'''
        return '#'+'%02x%02x%02x' % rgb  # '%' format operator, '02x' hexadecimal form. This line says get hexidecimal by parsing three items from tuple

    def get_inc_map(self, year='2016'):
        '''get incidents map
        @args: year: str
        @return folium map NOTE: front end will simply render map.html from assets
        '''
        calgary_map = folium.Map(location=CALGARY)
        incident_frame = self.get_incident(
            'Traffic_Incidents', year=year, sort=False)
        for index, info, desc, date, mod_date, quad, lon, lat, location, count, id in incident_frame.itertuples():
            # print(info, lat, lon, date)
            folium.map.Marker(location=[lat, lon],
                              popup=f'{desc}\n {info}\n {date}\n').add_to(calgary_map)
        print(f"Saving incident {year} map")
        calgary_map.save('./assets/map.html', zoom_start=10)
        return calgary_map

    def get_vol_map(self, year='2016'):
        '''get volume map
        @args: year: str
        @return folium map NOTE: front end will simply render map.html from assets
        '''
        calgary_map = folium.Map(location=CALGARY)
        volume_frame = self.get_volume(year=year, sort=True)
        color_increments = 256  # 0-255
        color_steps = len(volume_frame)  # number of data entries
        n_color = color_steps // color_increments  # change color every n_color steps
        step_counter = 0
        r = 255  # since we sorted above, the largest volume will be red, green lightest volume
        g = 0
        b = 0

        # TODO: Clean up this spaghetti
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
            color = self.rgb_to_hex((r, g, b))
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
        print(f"Saving volume {year} map")
        calgary_map.save('./assets/map.html', zoom_start=10)
        return calgary_map


def main():
    print("Running controller.main()...\n")


if __name__ == "__main__":
    main()
