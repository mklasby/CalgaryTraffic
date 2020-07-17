# data.py - model

from pymongo import MongoClient
import pandas as pd
from getpass import getpass

# Following is for connecting to my cloud cluster
# TODO: Hide PW
# pw = "Hikehigh00!mongodb"  # getpass("Enter DB Password")
# cluster = MongoClient('mongodb+srv://mklasby:' + pw
#                       + '@cluster0.hkive.mongodb.net/<dbname>?retryWrites=true&w=majority')

# local cluster


def mongo_test():
    cluster = MongoClient(
        'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
    db = cluster["calgaryTraffic"]
    collection = db["test"]

    post1 = {"_id": 0, "name": "rachel", "score": 5}
    post2 = {"_id": 1, "name": "mike", "score": 5}

    collection.insert_many([post1, post2])

    results = collection.find({"name": "mike"})

    for items in results:
        print(items)
        print(items["_id"])

    results = collection.update_one({"_id": 0, }, {"$set": {"name": "josh"}})


class Mainframe():
    '''
    A collection of pd.Dataframe objects
    '''

    def __init__(self):
        self.data_frames = []

    def load_data(self, name):
        data_frame = pd.read_csv(name)
        data_frame.name = name.split('.')[0]
        print(data_frame.name)
        self.data_frames.append(data_frame)

    def display_CLI(self):
        for data in self.data_frames:
            print(type(data))
            print(len(data))
            print(data.shape)
            print(data.head())

    def init_db(self, local=True):
        if local:
            # local cluster
            cluster = MongoClient(
                'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        else:
            # cloud cluster
            pw = getpass("Enter DB Password >>> ")
            cluster = MongoClient('mongodb+srv://mklasby:' + pw
                                  + '@cluster0.hkive.mongodb.net/<dbname>?retryWrites=true&w=majority')

        db = cluster["calgaryTraffic"]
        for data_frame in self.data_frames:
            collection = db[data_frame.name]
            data_frame.reset_index(inplace=True)
            data_dict = data_frame.to_dict("records")
            collection.insert_many(data_dict)


def main():
    mainframe = Mainframe()
    mainframe.load_data("Traffic_Incidents.csv")
    mainframe.load_data("")
    mainframe.display_CLI()

    # TrafficFlow2016_OpenData.csv
    # 2017_Traffic_Volume_Flow.csv
    # Traffic_Incidents_Archive_2016.csv
    # Traffic_Incidents_Archive_2017.csv
    # Traffic_Volumes_for_2018.csv


if __name__ == "__main__":
    print("Running data.main()...\n")
    main()
