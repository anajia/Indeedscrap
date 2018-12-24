from flask import Flask
from flask import render_template
from flask import request, redirect, url_for       
from flask import jsonify
import json
from bson import BSON
from bson import json_util

import pymongo
from pymongo import MongoClient
import graphs

client = MongoClient('localhost', 27017)
db = client.georgian
collection = db.data_final

top_five = graphs.mongo_query(collection)
skills_by_job = graphs.skills_query(collection)
total_skills = graphs.total_skills(collection)
avg_salary = graphs.average_salary(collection)
total_records = graphs.get_total(collection)
	
for skill in total_skills:
		
	sql =   int((skill["sql"]*100)/total_records)
	python =   int((skill["python"]*100)/total_records)
	java =   int((skill["java"]*100)/total_records)
	sas =   int((skill["sas"]*100)/total_records)
	javascript =   int((skill["javascript"]*100)/total_records)
	hadoop =   int((skill["hadoop"]*100)/total_records)
	other = 100 -(sql+python+java+sas+javascript+hadoop)

all_data = graphs.get_all_data(collection)


app = Flask(__name__)

@app.route('/')
def index_page():
        return render_template('index.html')

@app.route('/map')
def map_view():
	return render_template('map_view.html')

@app.route('/graph')
def graph():
	

		#pie_chart_per.update({"python": int((skill.python*100)/total_records)})
		#pie_chart_per.update({"java": int((skill.java*100)/total_records)})
		#pie_chart_per.update({ int((skill.hadoop*100)/total_records)
		#pie_chart_per["sas"] = int((skill.sas*100)/total_records)
		#pie_chart_per["javascript"] = int((skill.javascript*100)/total_records)



	return render_template('graphs.html',top_five = top_five, skills_by_job =skills_by_job, sql = sql
	,python = python, java= java, sas=sas, javascript= javascript, hadoop=hadoop,other=other,
	 avg_salary =avg_salary, total_records = total_records )


@app.route('/tables')
def view_tables():
	return render_template('tables.html', city_table = top_five, average = avg_salary, job_title_skill = skills_by_job,
	sql2 = sql, python2 = python, java2= java, sas2 = sas, javascript2= javascript, hadoop2= hadoop, other2 = other)


@app.route('/excel')
def offline_graph():
        return render_template('excel.html')


@app.route('/api')
def simple_api():
	
	
	
	json_data=  [json.dumps(doc, default=json_util.default)for doc in all_data  ]
	return  jsonify(json_data)

@app.route('/docs')
def documentation():
        return render_template('docs.html')

@app.route('/api2')
def api2():
	    city = request.args.get('city')
	    print(city)
	    cities =   collection.find({ "Search_city": city })
	    city_list = list(cities)
	    return render_template('api2.html', city_list= city_list)



if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)

