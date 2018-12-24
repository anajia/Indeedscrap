# Indeedscrap

Project to scrap data from job Postings from indeed, including scrapping keywords from description. Initally data was saved in excel but
code was changed to store data in Mongodb. sample of row data scrapped. you can see sql, python etc.. with 0 and 1. For the project,
Programming languages and some Database technologies were check for inside the job postings and if they existed then 1 else 0. 
Just a simple way to check what the job is asking for.


Scarpping code was modified to only look for jobs posted On current day and day before. Function check_date() can be removed to fetch 
data endlessly or modify for a specific date range.

Salaries also had to be modified since they were given as hourly, daily, monthly or yearly. Two new columns Min_salary and Max salary
were created to get numerical yearly salary data from orginal. 

Finally, google api was used to get lat and lng for jobs.

sample row of data (a single job posting)
![alt text](https://github.com/anajia/Indeedscrap/blob/master/imgs/sample.jpg)

A couple of web pages on Amazon EC2 instance were created using python Flask.The data was then used to graph charts using Google Charts.

This was based on an article from medium: https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b


**daily_scrap2.py** : web scarpping code

**graphs.py, app.py** : Flask code

**mongo_test.py, insert_excel.py** : just sample code to export to excel or mongo

Jobs scrapped were only jobs related to data analysis, but job array can be modified to look for any job position.

This is actually my first python project. Scrapping code could be improved significantly, but the project is done for me ^^;
