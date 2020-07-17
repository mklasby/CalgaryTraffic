# data.py - model

from pymongo import MongoClient
import pandas as pd
from getpass import getpass


class Mainframe():
    '''
    A collection of pd.Dataframe objects
    '''

    def __init__(self, db_name="default"):
        self.data_frames = []
        self.db_name = db_name
        self.cluster = False

    def load_data(self, name):
        data_frame = pd.read_csv(name)
        data_frame.name = name.split('.')[0]
        print("Loading: "+data_frame.name)
        self.data_frames.append(data_frame)

    def display_CLI(self):
        '''Prints relevent information about all loaded dataframes'''
        for data in self.data_frames:
            print(type(data))
            print(len(data))
            print(data.shape)
            print(data.head())

    def init_db(self, local=True):
        if local:
            # local cluster
            print("Connecting to local cluster")
            self.cluster = MongoClient(
                'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        else:
            # cloud cluster
            print("Conntect to Mongo Atlas cluster")
            pw = getpass("Enter DB Password >>> ")
            self.clustercluster = MongoClient('mongodb+srv://mklasby:' + pw
                                              + '@cluster0.hkive.mongodb.net/<dbname>?retryWrites=true&w=majority')
        # creates db named db_name within my cluster
        db = self.cluster[self.db_name]
        db_on = True

    def push_data(self):
        if not self.cluster:  # if cluster has not be started
            # defaults to looking at local cluster
            self.init_db()
        for data_frame in self.data_frames:
            db = self.cluster[self.db_name]
            collection = db[data_frame.name]
            data_frame.reset_index(inplace=True)
            data_dict = data_frame.to_dict("records")
            collection.insert_many(data_dict)

    def drop_db(self, db_name="default"):
        if not self.cluster:
            self.init_db()
        print("Dropping DB named: " + self.db_name)
        self.cluster.drop_database(self.db_name)


def main():
    mainframe = Mainframe("calgaryTraffic")
    mainframe.drop_db()
    mainframe.load_data("Traffic_Incidents.csv")
    mainframe.load_data("TrafficFlow2016_OpenData.csv")
    mainframe.load_data("2017_Traffic_Volume_Flow.csv")
    mainframe.load_data("Traffic_Volumes_for_2018.csv")

    mainframe.display_CLI()

    mainframe.init_db()
    mainframe.push_data()

    # TrafficFlow2016_OpenData.csv
    # 2017_Traffic_Volume_Flow.csv
    # Traffic_Volumes_for_2018.csv


if __name__ == "__main__":
    print("Running data.main()...\n")
    main()
