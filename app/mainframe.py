# data.py - model

from pymongo import MongoClient
import pandas as pd
from getpass import getpass
from os import path


class Mainframe():
    '''
    A collection of pd.Dataframe objects used for interacting with a single database in a single cluster
    '''

    def __init__(self, db_name="default", local=True):
        self.data_frames = []
        self.db_name = db_name
        self.cluster = False
        self.local = local

    def load_data(self, name):
        data_frame = pd.read_csv(name)
        head, tail = path.split(name)
        data_frame.name = tail.split('.')[0]
        print("Loading: "+data_frame.name)
        self.data_frames.append(data_frame)

    def display_CLI(self):
        '''Prints relevent information about all loaded dataframes'''
        for data in self.data_frames:
            print(type(data))
            print(len(data))
            print(data.shape)
            print(data.head())

    def init_db(self):
        if self.local:
            # local cluster
            print("Connecting to local cluster")
            self.cluster = MongoClient(
                'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        else:
            # cloud cluster
            print("Connecting to Mongo Atlas cluster")
            pw = getpass("Enter DB Password >>> ")
            self.cluster = MongoClient('mongodb+srv://mklasby:' + pw
                                       + '@cluster0.hkive.mongodb.net/<dbname>?retryWrites=true&w=majority')
        # creates db named db_name within cluster
        self.db = self.cluster[self.db_name]

    def push_data(self):
        if not self.cluster:  # if cluster has not be started
            self.init_db()
        for data_frame in self.data_frames:
            collection = self.db[data_frame.name]
            data_frame.reset_index(inplace=True)
            data_dict = data_frame.to_dict("records")
            collection.insert_many(data_dict)

    def drop_db(self, db_name="default"):
        if not self.cluster:
            self.init_db()
        print("Dropping DB named: " + self.db_name)
        self.cluster.drop_database(self.db_name)

    # TODO: move follow to a pandas type class?

    def get_collection(self, name, query={}, no_id=True, no_index=True):
        print(
            f"Getting collection {name} from {self.db_name} using query {query}")
        cursor = self.db[name].find(query)
        collection = pd.DataFrame(list(cursor))

        if no_id:
            del collection['_id']

        if no_index:
            del collection['index']
        return collection


def main():
    '''will load data if called as main'''
    # TODO: Add input requests db name and file names so this can be reused in future
    response = input("Save to local?[y/n]: ")
    if response == ("y" or "Y"):
        mainframe = Mainframe("calgaryTraffic")
    else:
        mainframe = Mainframe("calgaryTraffic", local=False)
    mainframe.drop_db()
    mainframe.load_data("Traffic_Incidents.csv")
    mainframe.load_data("TrafficFlow2016_OpenData.csv")
    mainframe.load_data("2017_Traffic_Volume_Flow.csv")
    mainframe.load_data("Traffic_Volumes_for_2018.csv")
    mainframe.push_data()
    print("Data successfully loaded")


if __name__ == "__main__":
    print("Running data.main()...\n")
    main()
