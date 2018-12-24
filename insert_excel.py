
import json
import pandas as pd
import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.georgian

collection = db.data_final

df = pd.read_excel("indeed_2_loc_new.xlsx")

collection.insert_many(df.to_dict('records'))
