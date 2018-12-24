import pymongo
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)

db = client.georgian
collection = db.data_final

#print(collection.find_one({"_id" : ObjectId("5bfdf4275a37e507cff0ff4a")}))

print(collection.find_one({"Search_word" : "Data Scientist" , "max_salary" : { "$gt": 70000 }}))

