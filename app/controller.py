# controller.py - controller
'''This module provides app.py with a controller interface to interact with
data model. 
'''


class Controller():
    '''class to act as middle man b/w app and mainframe. Need to be passes these
    as references'''

    def __init__(self, mainframe):
        self.mainframe = mainframe  # mainframe class

    def find_table(self, name):
        '''returns text string of collection name in db
        Could be in db class too'''
        if name == "2016":
            return "TrafficFlow2016_OpenData"
        elif name == "2017":
            return "2017_Traffic_Volume_Flow"
        elif name == "2018":
            return "Traffic_Volumes_for_2018"
        elif name == "incidents" or "Traffic_Incidents":
            return "Traffic_Incidents"
        else:
            # TODO: Raise excpetion on bad input / not found
            print("NO YEAR FOUND")
            return -1

    def get_volume(self, year):
        '''returns pd.DataFrame object of volume for requested year'''
        name = self.find_table(year)
        vol = self.mainframe.get_collection(name)
        #vol = vol.sort_values(by='volume', ascending=False)
        return vol

    def get_incident(self, name, year):
        name = self.find_table(name)
        incidents = self.mainframe.get_collection(
            name, {"START_DT": {'$regex': year}})
        return incidents
        # TODO:HOW TO SORT?
        # incidents = incidents.sort_values(by="")

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


def main():
    print("Running controller.main()...\n")


if __name__ == "__main__":
    main()
