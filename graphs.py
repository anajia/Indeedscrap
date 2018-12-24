import pymongo
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId
from bson.son import SON
import pprint

def connect():

	client = MongoClient('localhost', 27017)
	db = client.georgian
	collection = db.data_final
	return collection

def get_all_data(table):
	collection= table
	all_data = collection.find({} ,{"_id": 0 })
	data_list = list(all_data)
	return data_list
	

#top five cities for jobs
def mongo_query(table):
	collection = table
	city_list = collection.aggregate([{ "$group" : { "_id" : "$Search_city", "count" : {"$sum" : 1} }}, 
				     {"$sort": SON([("count", -1)])}])
	cities = list(city_list)
	top_five = []

	for i in range(6):
		top_five.append(cities[i])
	return top_five

#query for skills by job title
def skills_query(table):
	collection = table
	skill_list  = collection.aggregate([{"$group" : {"_id": "$Search_word", "sql": {"$sum": "$sql"}, "hadoop": {"$sum" : "$hadoop" },
	"hive" : {"$sum": "$hive"}, "pig" :{"$sum" : "$pig"} ,  "sas" :{"$sum" : "$sas"},  "powerbi" :{"$sum" : "$powerbi"},
 	"mongodb" :{"$sum" : "$mongodb"}, "java" :{"$sum" : "$java"}, "python" :{"$sum" : "$python"},  
	 "javascript" :{"$sum" : "$javascript"}, "scala" :{"$sum" : "$scala"}
	}}]);

	skills = list(skill_list)
	return skills

#query for total skills distribution in job market
def total_skills(table):
	collection = table
	
	total_skills = collection.aggregate([{ "$group": { "_id": 1, "sql": { "$sum" : "$sql"}, "hadoop" : {"$sum" : "$hadoop" },
 	"hive" : { "$sum": "$hive"}, "pig" :{"$sum" : "$pig"} ,  "sas" :{ "$sum" : "$sas"},  "powerbi" :{ "$sum" : "$powerbi"},
 	"mongodb" :{ "$sum" : "$mongodb"}, "java" :{ "$sum" : "$java"}, "python" :{"$sum" : "$python"},
 	"javascript" :{ "$sum" : "$javascript"}, "scala" :{ "$sum" : "$scala"}}}])
	
	total_list = list(total_skills)
	return total_list

#average min and max salary
def average_salary(table):
	collection = table
	average_sal = collection.aggregate([
 	{"$group": { "_id" : "$Search_word", "min_salary":{ "$avg" : "$min_salary" }, "max_salary" :{ "$avg": "$max_salary" }}},
 	{"$sort" : {"min_salary": -1 }}])

	avg_list = list(average_sal)
	return avg_list

#current total records
def get_total(table):
	collection = table
	total_records = collection.count()
	return total_records



#test each function
#connection  = connect()

#skills  = get_all_data(connection)
#for skill in skills:

#	print(skill)






