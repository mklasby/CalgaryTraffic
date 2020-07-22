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
        '''Top level controller method for getting requested data tables based on 
        user inputs passed from callbacks.py'''
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
        if sort:
            return self.sort_volume(vol)
        else:
            return vol

    def sort_volume(self, vol):
        '''Sort pd.dataframe by "volume"
        Returns: sorted dataframe object'''
        vol = vol.sort_values(by='volume', ascending=False)
        print('Sorted Collection by volume')
        return vol

    def get_incident(self, name='incidents', year='2016', sort=False):
        '''Method to return incident table based on year argument.
        param:  name: name of colleciton in db
                year: year of data we want
                sort: if you want sorted, set to True NOTE: Resource intensive
        returns: incidents: pd.Dataframe object
        '''
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
        '''Method adds "Number of Accidents" column to incidents dataframe which
         will = the number of rowswith the same 'INCIDENT INFO' value. 
         Returns sorted pd.DataFrame object'''
        dict_hist = {}
        incidents.insert(1, 'Number of Accidents', "")
        for index, item in incidents.iterrows():
            info = item['INCIDENT INFO']
            dict_hist[info] = dict_hist.get(info, 0)+1
        for index, item in incidents.iterrows():
            incidents.at[index, 'Number of Accidents'] = dict_hist.get(
                item['INCIDENT INFO'])
        incidents = incidents.sort_values(
            by=['Number of Accidents', 'INCIDENT INFO'], ascending=False)
        print('Sorted Collection by number of accidents')
        return incidents

    def get_view(self, df, name="temp.html"):
        '''Used for debugging and setting up static views of pd.DataFrame obj'''
        return df.to_html(name)

    def get_fig(self, data_children, n):
        '''top level controller method to create analysis chart based on user inputs pass from callbacks.py
        Returns: px.fig object'''

        switch = data_children[0]
        data = data_children[1]
        year = data_children[2]

        if switch == 'max':
            data_table = self.get_data(('total', data, year))
            if data == 'inc':
                data_table = self.sort_inc(data_table)
                title = f"Top {n} most dangerous locations to be driving in Calgary in {year}"
                fig = self.get_bar_chart(
                    data_table, "INCIDENT INFO", "Number of Accidents", 'Accident Info', 'Number of Accidents', title, n)
                return fig

            if data == 'vol':
                data_table = self.sort_volume(data_table)
                title = f'Busiest roads in Calgary in {year}'
                fig = self.get_bar_chart(
                    data_table, 'secname', 'volume', 'Sector Name', 'Volume - Annual Vehicle Trips', title, n)
                return fig

        else:  # switch = totals, get top result and that result from each year
            this_year = self.get_data(
                ('total', data, year), True)  # sorted df
            # we need to pull all collections of the same dat type to find values where the requested year master_key is present in othery ears
            data_16 = self.get_data(('total', data, '2016'), True)
            data_17 = self.get_data(('total', data, '2017'), True)
            data_18 = self.get_data(('total', data, '2018'), True)
            years = [data_16, data_17, data_18]  # list of these collections
            top = {}
            if data == 'inc':
                top = self.get_top_n(
                    this_year, n, 'INCIDENT INFO', year, 'Number of Accidents')
                top = self.check_other_years(
                    top, year, years, 'INCIDENT INFO', 'Number of Accidents')
                fig = self.get_scatter_fig(top, 'Year', 'Number of Accidents')
                fig.update_layout(title=f'Most dangerous {n} locations to be driving in Calgary in {year} plotted from 2016-2018',
                                  xaxis_title='Year', yaxis_title='Number of Accidents', legend_title='Incident Info')
                return fig
            else:  # data == volume
                top = self.get_top_n(this_year, n, 'secname', year, 'volume')
                top = self.check_other_years(
                    top, year, years, 'secname', 'volume')
                fig = self.get_scatter_fig(top, 'Year', 'Volume of Traffic')
                fig.update_layout(title=f'Busiest {n} sectors in Calgary in {year} plotted from 2016-2018',
                                  xaxis_title='Year', yaxis_title='Volume of Traffic', legend_title='Sector Names')
                return fig

    def get_bar_chart(self, data_table: pd.DataFrame, key: str, value: str, x_title: str, y_title: str, title: str, n: int = 10):
        '''Method to get px.bar chart of n top rows from sorted data frame. '''
        top = {}
        for index, item in data_table.iterrows():
            if len(top) == n:
                break
            if item[key] in top:
                continue
            else:
                top[item[key]] = item[value]
        fig_dict = {y_title: list(top.values()),
                    x_title: list(top.keys())}
        fig = px.bar(fig_dict, x=x_title,
                     y=y_title, title=title)
        return fig

    def get_top_n(self, df: pd.DataFrame, n: int, master_key: str, secondary_key: str, value: str):
        '''Method returns 2D dictionary from dataframe of top n entires of df in form of {master_key: {secondary_key:value}}'''
        top = {}
        for index, item in df.iterrows():
            if len(top) >= n:  # get top n
                break
            if item[master_key] in top:
                continue
            else:
                # {secname: {year:volume}}
                top[item[master_key]] = {
                    secondary_key: item[value]}
        return top

    def check_other_years(self, top: dict, year: str, years: list, master_key: str, value: str):
        '''Checks all years of similar data for other rows that match the master key value.
        Adds the corresponding value to a 2D dictonary in form of {master_key:{year: value}}'''
        # TODO: Could be generalize for a generic secondary key. Out of scope for this project
        year_index = 2015
        year_stop = 2018
        for date in years:
            year_index += 1
            if year_index > year_stop:
                break
            for index, item in date.iterrows():
                if item[master_key] in top:
                    if str(year_index) in top[item[master_key]]:
                        continue
                    else:
                        top[item[master_key]][str(
                            year_index)] = item[value]
        return top

    def get_scatter_fig(self, top: dict, x_values: str, y_values: str):
        '''Method gets scatter plot from 2D dictionary, returns go.Figure() object'''
        fig = go.Figure()
        for info in list(top.keys()):
            fig_dict = {
                x_values: list(top[info].keys()), y_values: list(top[info].values())}
            sorted_years = sorted(fig_dict[x_values])
            sorted_accidents = [accident for _, accident in sorted(
                zip(fig_dict[x_values], fig_dict[y_values]), key=lambda x:x[0])]
            fig_dict = {x_values: sorted_years,
                        y_values: sorted_accidents}
            fig.add_trace(go.Scatter(
                x=fig_dict[x_values], y=fig_dict[y_values], name=info, hoverinfo='all'))
        return fig

    def get_map(self, data_children, n=10):
        '''Top level Controller method for getting map based on user selected parameters 
        passed by callbacks.py. Updates static map asset in ./assets/map.html
        returns None'''
        switch = data_children[0]
        data = data_children[1]
        year = data_children[2]

        if data == "vol":
            volume_dataframe = self.get_vol_map_df(switch, year, n)
            self.draw_vol_map(volume_dataframe)

        else:  # data=='inc'
            incident_dataframe = self.get_inc_map_df(switch, year, n)
            self.draw_inc_map(incident_dataframe, year)

    def rgb_to_hex(self, rgb):
        '''Method converts (r,g,b) to hex color, helper for map functons'''
        # '%' format operator, '02x' hexadecimal form.
        # This line says get hexidecimal by parsing three items from tuple
        return '#'+'%02x%02x%02x' % rgb

    def get_inc_map_df(self, switch='total', year='2016', n=10):
        '''get inc df for map drawing
        @params
        @returns inc df
        '''
        incident_frame = self.get_incident(
            'Traffic_Incidents', year=year, sort=False)
        incident_frame = self.sort_inc(incident_frame)
        if switch == 'total':
            return incident_frame
        else:  # switch == max
            accident_numbers = []
            last_idx = 0
            for index, item in incident_frame.iterrows():
                if len(accident_numbers) >= 10:
                    break
                last_idx += 1
                if item['Number of Accidents'] in accident_numbers:
                    continue
                else:
                    accident_numbers.append(item['Number of Accidents'])
            incident_frame = incident_frame.iloc[:last_idx]
            return incident_frame

    def draw_inc_map(self, incident_frame: pd.DataFrame, year):
        '''get incidents map
        @args: incident_frame: pd.DataFrame
        @return folium map NOTE: front end will simply render map.html from assets
        '''
        calgary_map = folium.Map(location=CALGARY)
        color_increments = 256  # 0-255
        accident_entires = incident_frame['Number of Accidents']
        accident_range = []
        accident_range = [accident_range.append(x)
                          for x in accident_entires if x not in accident_range]  # number of unique accident values
        # number of unique accident number entries
        color_steps = len(accident_range)
        step = 256//color_steps
        if step == 0:
            step = 1
        r = 255  # since we sorted above, the largest volume will be red, green lightest volume
        g = 0
        b = 0
        last_accident_count = -1
        for index, items in incident_frame.iterrows():
            info = items['INCIDENT INFO']
            desc = items['DESCRIPTION']
            date = items['START_DT']
            lat = items['Latitude']
            lon = items['Longitude']
            acc = items['Number of Accidents']
            if last_accident_count == -1:
                last_accident_count = acc
            if acc != last_accident_count:  # Check if we need to change color
                r -= step  # change red to green from max to min by step value
                g += step
                last_accident_count = acc
            color = self.rgb_to_hex((r, g, b))
            folium.map.Marker(location=[lat, lon],
                              popup=f'{desc}\n {info}\n {date}\n {acc} Total accidents in this zone', icon=folium.Icon(icon='car', prefix='fa', icon_color=color)).add_to(calgary_map)
        print(f"Saving total incident {year} map")
        calgary_map.save('./assets/map.html', zoom_start=5)
        return calgary_map

    def get_vol_map_df(self, switch='total', year='2016', n=10):
        '''get max vol map
        @args: year: str, switch:str, n:int
        @return pd.dataframe object of table to be mapped
        '''
        volume_frame = self.get_volume(year=year, sort=True)
        if switch == 'total':
            return volume_frame
        else:  # switch = max
            volume_frame = volume_frame.iloc[0:n]  # return top n rows
            return volume_frame

    def draw_vol_map(self, volume_frame):
        '''get volume map
        @args: volume_frame :pd.DataFrame to map
        @return folium map NOTE: front end will simply render map.html from assets
        '''
        calgary_map = folium.Map(location=CALGARY)
        color_increments = 256  # 0-255
        color_steps = len(volume_frame)  # number of data entries
        n_color = color_steps // color_increments  # change color every n_color steps
        step_counter = 0
        step = 256//color_steps
        if step == 0:
            step = 1
        r = 255  # since we sorted above, the largest volume will be red, green lightest volume
        g = 0
        b = 0

        for index, items in volume_frame.iterrows():
            secname = items['secname']
            volume = items['volume']
            the_geom = items['the_geom']
            year = items['year_vol']
            if step_counter > n_color:  # Check if we need to change color
                r -= step
                g += step
                step_counter = 0
            point_cloud = []
            color = self.rgb_to_hex((r, g, b))
            # strip everything outside of (( ))
            location = re.search(r'\(\((.*?)\)\)', the_geom)
            for loc in location.groups(1):
                loc = loc.split(',')  # split coordinate pairs
                for point in loc:
                    point = point.strip().split(' ')
                    lon = point[0].strip(')').strip(
                        '(')  # remove any remaining parenthesis
                    lon = float(lon)  # convert from string
                    lat = point[1].strip('(').strip(')')
                    lat = float(lat)
                    point_cloud.append([lat, lon])
            polyline = folium.PolyLine(
                locations=point_cloud, tooltip=f'{secname}\n {volume} number of cars in {year}', color=color).add_to(calgary_map)
            step_counter += 1
        print(f"Saving total volume {year} map")
        calgary_map.save('./assets/map.html', zoom_start=5)
        return calgary_map


def main():
    print("Running controller.main()...\n")


if __name__ == "__main__":
    main()
