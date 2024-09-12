from pymongo import MongoClient

host = 'localhost'
port = 27017

mongo = MongoClient(host, port)
print("Mongo Client: {0}".format(mongo))

server_info = mongo.server_info()
print('SErver Info: {0}'.format(server_info))