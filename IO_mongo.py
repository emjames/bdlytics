# takes care of connecting to mongodb
# from pymongo import MongoClient
import pymongo


class IO_mongo(object):
    def __init__(self, db, coll):
        try:
            # use MongoClient to create a connection
            # set the max server time out (default is 30)
            self.client = pymongo.MongoClient(serverSelectionTimeoutMS=2)
            # self.client = MongoClient("mongodb://mongodb0.example.net:27019")
            # force connection request
            self.client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            # if connection failed print the error message
            print(err)
        else:
            # else the connection was successful, can proceed
            # access a database to db, create one if it doesn't exist
            self.db = self.client[db]
            # access collections objects
            self.coll = self.db[coll]

    def save(self, data):
        # print "Saving to mongodb"
        # try to get a connection on the database server
        try:
            # request server info
            self.client.server_info()
        # catch the error
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
        # if there is no error, add the incoming data to the database
        else:
            # insert incoming data in the collection
            # returns inserted_id, which contains the _id of the inserted document
            return self.coll.insert_one(data)
