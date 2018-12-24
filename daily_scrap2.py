## lacks experience
## checking dates
import googlemaps
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import string
from datetime import datetime, timedelta
import re
import os
import json
import pymongo
from pymongo import MongoClient

# change number to get more results
max_results_per_city = 2

#cities Ottawa, Toronto, Waterloo, Barrie
#city array if we want to we can use to search in different areas
# Québec+Province Ontario
city_set = ['Québec+Province','Ontario']

#gather data on these jobs
jobs = ['Data+Analyst','Data+Scientist', 'Data+Architect', 'Data+Engineer', 'Database+Administrator', 
        'Database+Developer', 'Business+Analyst' ]

current_job_query = ['Data+Analyst']

# search words
words = [ 'hive', 'pig', 'sql', 'sas', 'powerbi', 'hadoop', 'scala', 'python', 'java', 'javascript', 'mongodb']

# dataframe header columns
columns = ['job_id','Search_word','job_title', 'company_name', 'Search_city', 'Salary',"summary", "date", 'url',
           'hive', 'pig', 'sql', 'sas', 'powerbi', 'hadoop', 'scala', 'python', 'java', 'javascript', 'mongodb',
           'min_salary', 'max_salary', 'lat', 'lng']

#defining a data frame and adding the columns
jobs_df = pd.DataFrame(columns = columns)

# get current date, we need this for 2 reasons
# data in indeed are stored relative to today such as 2 days ago etc..
# we need date in order to run script properly every 2 days
today_date = datetime.now()

# this is the date to check, if ad date newer than 2 days ago then we get it
# else we don't take the data
check_date = today_date - timedelta(days = 2)

# variables for date 
day_array = ['day', 'days']
hour_array = ['hour', 'hours']

#function to check the ad date and decide
def check_job_date(thediv):
    div = thediv
    date_posted = div.find_all(name='span', attrs={'class':'date'})
    if len(date_posted) > 0:
        for dp in date_posted:
            if dp.text == 'Just posted' or dp.text == 'Today':
                return 1
            else:
                #remove plus from number
                clean_number = dp.text.strip()
                for char in string.punctuation:
                    clean_number = clean_number.replace(char, ' ')
                    date_split = clean_number.split()
                    if(date_split[1] in day_array): 

                        #checking date
                        delta = today_date - check_date
                        if(delta.days >= 2):
                            #print("old data")
                            return 0
                        else:
                            return 1
                            #print("new data")

                    elif(date_split[1] in hour_array):
                        return 1
    else: 
        return 0
            

# make 2 columns from salary into min and max
def seperate_salary(string_salary):
    
    salary = str(string_salary)
    
    salary = salary.replace('$', '')
    salary = salary.replace(',', '')
    
    if string_salary == "Salary undefined":
        min_sal = "Salary undefined"
        max_sal = "Salary undefined"
        salaries = [min_sal, max_sal, salary]
        return salaries
    else: 
        payment_types = ['hour', 'day', 'year']

        for payment in payment_types:
            if payment in string_salary:
                payment_type = payment
                break
                
        if(salary.find('-') > -1):
            two_salaries= salary.split('-')

            if(payment_type == "hour"):
                min_sal = float(two_salaries[0])* 1920
                max_sal = float(two_salaries[1][1:3]) * 1920
            elif(payment_type == "day"):
                min_sal = float(two_salaries[0])* 240
                max_sal = float(two_salaries[1][1:4]) * 240
            elif(payment_type == "year"):
                min_sal = two_salaries[0]
                max_sal = two_salaries[1][1:7]

            #salaries.append(min_sal)
            #salaries.append(max_sal)
            salaries = [min_sal, max_sal, salary]
            return salaries

        else:
            # for cases with just one salary
            one_salary = [float(s) for s in re.findall(r'-?\d+\.?\d*', salary)]
            if(payment_type == "hour"):
                min_sal = one_salary[0]* 1560
                max_sal = one_salary[0]* 1560
            elif(payment_type == "day"):
                min_sal = one_salary[0]* 240
                max_sal = one_salary[0]* 240               
            elif(payment_type == "year"):
                min_sal = one_salary[0]
                max_sal = one_salary[0]

            #salaries.append(min_sal)
            #salaries.append(max_sal)
            salaries = [min_sal, max_sal, salary]
            return salaries
            
            
# get job count from page to set max_results_per_city for only new jobs
#1
def get_num_jobs():
    pass


            
#get experience experimental
#2
def add_experience(job_description):
    pass



def get_location(town_region):
    location_row = []
    fname = "google_api.txt"
    ## use my google api key to get lang and lat
    with open('google_api.txt') as f:
        APIKEY = f.readline()
        f.close()

    google_map = googlemaps.Client(key=APIKEY)

    geo_location = google_map.geocode(town_region)[0]
    location_row.append(geo_location['geometry']['location']['lat'])
    location_row.append(geo_location['geometry']['location']['lng'])
    
    return location_row


def connect_mongo():
    #insert dataframe when done         
    client = MongoClient('localhost', 27017)
    db = client.georgian
    collection = db.data_final
    return collection

collection = connect_mongo()

def  get_latest_id(col):
    collection = col
    current_id=collection.find_one(sort=[("job_id", -1)])["job_id"]
    return current_id
  
num = int(get_latest_id(collection))

for current_job in jobs:
    #loop on cities
    for city in city_set:
        #how many pages
        # get num jobs function here #1
        for start in range(0, max_results_per_city, 10):
            #%2C+ON old
            #page = requests.get('https://ca.indeed.com/jobs?q=Data+scientist&l=' + str(city) + 
                                #'&fromage=last&start=' + str(start))
            #page = requests.get('https://ca.indeed.com/jobs?q='+ str(current_job_query) +'&l=' + str(city) + 
                                #'&start=' + str(start))
            page = requests.get('https://ca.indeed.com/jobs?q=' +str(current_job) +'&l='+ str(city) +
                                '&fromage=last&sort=date')
            #ensuring at least 1 second between page grabs
            #might need to increase this
            time.sleep(2)  

            soup = BeautifulSoup(page.text, "lxml")

            #loop on the row divs on page
            for div in soup.find_all(name='div', attrs={'class':'row'}):
                new_data = check_job_date(div)
                if(new_data == 0):
                    print("old data")
                else:                
                    num += 1
                    print(num)

                    job_post = []
                    job_post.append(num)
                    job_post.append(current_job.replace("+", " "))

                    # find all jobtitles in div
                    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
                        if len(a) > 0:
                            job_post.append(a['title'])
                            break
                        else:
                            job_post.append("couldnt get title")

                        #find company name
                    company = div.find_all(name='span', attrs={'class':'company'}) 
                    # company name more than one word
                    if len(company) > 0: 
                        for b in company:
                            company_name = b.text.strip()
                            job_post.append(b.text.strip())
                            break
                    else: 
                        sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
                        if len(sec_try) >0:
                            for span in sec_try:
                                job_post.append(span.text)
                                break
                        else:
                            job_post.append("could not find company")


                    #city in search div added recently for better results                        
                    city2 = div.find_all(name='span', attrs={'class':'location'})

                    if len(city2) > 0: 
                        for cc in city2:
                            job_post.append(cc.text.strip())
                            town_region = cc.text.strip()
                            break
                    else:
                        city2 = div.find_all(name='div', attrs={'class':'location'})

                        if len(city2) > 0: 
                            for cc in city2:
                                job_post.append(cc.text.strip())
                                town_region = cc.text.strip()
                                break
                        else:
                            job_post.append(city)
                            town_region = city
                    # get long and lat for the region
                    coordinates = get_location(town_region)



                    # salary if posted
                    function_salary = ""
                    salary2 = div.find_all(name='span', attrs={'class':'no-wrap'})
                    if len(salary2) > 0: 
                        for ss in salary2:
                            function_salary = ss.text.strip()
                            job_post.append(ss.text.strip())
                            break
                    else:
                        function_salary = "Salary undefined"
                        job_post.append("Salary undefined") 

                    # find job summary        
                    d = div.findAll('span', attrs={'class': 'summary'}) 
                    if len(d) >0:
                        for span in d:
                            job_post.append(span.text.strip())
                            break
                    else:
                        job_post.append("could not fetch summary")


                    #find the date posted
                    # subtract from today date and then append


                    date_posted = div.find_all(name='span', attrs={'class':'date'})


                    if len(date_posted) > 0:
                            for dp in date_posted:
                                if dp.text == 'Just posted' or dp.text == 'Today':
                                    job_post.append(today_date.strftime('%m/%d/%Y'))
                                else:
                                    #remove plus from number
                                    clean_number = dp.text.strip()

                                    for char in string.punctuation:
                                        clean_number = clean_number.replace(char, ' ')
                                        # split the date to get the number and its type (hours, days)
                                        # subtract from today date to get the date the ad was posted
                                    date_split = clean_number.split()    

                                    # check if number is days or hours to insert proper date into dataframe
                                    if(date_split[1] in day_array): 
                                        the_date = today_date - timedelta(days = int(date_split[0]))
                                        the_date_string = the_date.strftime('%m/%d/%Y')
                                        job_post.append(the_date_string)
                                        break
                                    elif(date_split[1] in hour_array):
                                        job_post.append(today_date.strftime('%m/%d/%Y'))

                    else: 
                        job_post.append("Date undefined")

                    #add url for the page
                    job_link = div.find_all(name='a', attrs={'data-tn-element':'jobTitle'})

                    if len(job_link) > 0:

                        for job_link in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):

                            job_post.append("https://ca.indeed.com"+job_link['href'])

                            info_page_url = "https://ca.indeed.com"+job_link['href']

                            if(company_name == "Indeed Prime"):
                                for counter in range(0,11):
                                    job_post.append(0)
                            elif(company_name == "Indeed"):
                                for counter in range(0,11):
                                    job_post.append(0)

                            else:
                                #access the url of the job description page to get full summary

                                #sleep some time first since im having connection refused errors after some tim
                                time.sleep(3)
                                try:
                                    info_page = requests.get(info_page_url)
                                except:
                                    print("Connection refused ! sleep 5 seconds and try again")
                                    time.sleep(5)
                                    info_page = requests.get(info_page_url)


                                soup2 = BeautifulSoup(info_page.text, "lxml")


                                for job_desc in soup2.findAll(name='div', attrs={'class':'jobsearch-JobComponent-description'}):


                                    job_desc_text = job_desc.text.strip()

                                    #convert the text to lower case for more accurate results
                                    #user this variable in get experience function
                                    words_find = job_desc_text.casefold()

                                    #remove punctuations from the paragraph to prevent bugs
                                    for char in string.punctuation:
                                        words_find = words_find.replace(char, ' ')

                                    #here add exp function #2

                                    # loop on the paragrap and look for the keywords in words array
                                    # then append data into dataframe
                                    for word in words:
                                        exists = 0
                                        for word2 in words_find.split():
                                            if(word2 == word):
                                                exists +=1
                                        if exists > 0:
                                            job_post.append(1)
                                        else:
                                            job_post.append(0)

                    else:
                        job_post.append("URL not found")




                    print(start)
                    # insert the row job_post into the dataframe  

                    two_sals = seperate_salary(function_salary)
                    job_post.append(two_sals[0])
                    job_post.append(two_sals[1])
                    job_post.append(coordinates[0])
                    job_post.append(coordinates[1])
                    print(two_sals[2])
                    print(job_post)
                    print(coordinates)

                    jobs_df.loc[num] = job_post
                    #or insert every row
                    collection.insert(jobs_df.to_dict('records'))

            
#or insert all
#collection.insert_many(jobs_df.to_dict('records'))

