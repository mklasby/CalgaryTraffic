# app.py - view

from mainframe import Mainframe
from controller import Controller


class App():
    def __init__(self):
        pass


def main():
    mainframe = Mainframe("calgaryTraffic")
    mainframe.drop_db()
    mainframe.load_data("Traffic_Incidents.csv")
    mainframe.load_data("TrafficFlow2016_OpenData.csv")
    mainframe.load_data("2017_Traffic_Volume_Flow.csv")
    mainframe.load_data("Traffic_Volumes_for_2018.csv")
    mainframe.push_data()
    ctrl = Controller(mainframe)
    vol16 = ctrl.get_volume("2016")
    print(vol16)
    vol17 = ctrl.get_volume("2017")
    print(vol17)
    vol18 = ctrl.get_volume("2018")
    print(vol18)
    inc16 = ctrl.get_incident("incidents", "2016")
    print(inc16)
    inc17 = ctrl.get_incident("incidents", "2017")
    print(inc17)


if __name__ == "__main__":
    print("Running app.main()...\n")
    main()
