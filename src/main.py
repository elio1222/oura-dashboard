from dotenv import load_dotenv
import os
import json
import requests
import psycopg2
from datetime import date, timedelta
from oura import OuraClient
import requests

#loading environment variables
load_dotenv()
# Connecting to the database
conn = psycopg2.connect(host = os.getenv("hostname"), dbname = os.getenv("dbname"), user = os.getenv("user"),
                         password = os.getenv("password"), port = os.getenv("port"))
cursor = conn.cursor()

url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
headers = {
    "Authorization": f"Bearer {os.getenv("API_KEY")}"
}
# Actual parameters going to be used in the future...
'''
params = {
    "start_date": "2025-01-13",
    "end_date": "2025-05-10"
}
'''
# Testing parameter
params = {
    "start_date": "2025-01-13",
    "end_date": "2025-01-13"
}


#response = requests.request('GET', url, headers=headers, params=params)
#print(response.text)

# sleep_data = requests.get(url, headers=headers, params=params)
# print(json.dumps(sleep_data.json(), indent=2))

#request.get() returns the raw body of the HTTP Response into a Response object
response = requests.get(url, headers=headers, params=params)
# response.text turns this object into pure text, aka a string
# json.load() converts a JSOn string into a Python object, parses into a python dict/list.
jsondata = json.loads(response.text)
# print(jsondata)

# .json() returns the python dict at once, a shortcut instead of using .text and json.loads()
# print(jsondata['data'][0]['contributors']['deep_sleep'])
# the json data is a list full of dictionaries, hence the ['data'][0] <= first index of data
# the simple examples prints the value of the keys: ['contributors']['deep_sleep']
print(jsondata['data'][0]['contributors']['deep_sleep'])

# inserting this data into the database
cursor.execute("""
               INSERT INTO dailysleep (
               sleep_date, deep_sleep, efficiency,
               latency, rem_sleep, restfulness,
               timing, total_sleep, score
               )
               VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )
               ON CONFLICT (sleep_date) DO NOTHING;
               """, (
               jsondata['data'][0]['day'],
               int(jsondata['data'][0]['contributors']['deep_sleep']),
               int(jsondata['data'][0]['contributors']['efficiency']),
               int(jsondata['data'][0]['contributors']['latency']),
               int(jsondata['data'][0]['contributors']['rem_sleep']),
               int(jsondata['data'][0]['contributors']['restfulness']),
               int(jsondata['data'][0]['contributors']['timing']),
               int(jsondata['data'][0]['contributors']['total_sleep']),
               int(jsondata['data'][0]['score'])
)); 

# '%s' acts as placeholders since a QUERY line of code cannot read python code,
# that is why the python code is outside the query line of code
# In order to rerun the program without getting a psycopg2.errors.UniqueViolatoin error, 
# we must add the line 'ON CONFLICT (sleep_date) DO NOTHING' which enables us to rerun the
# program without any errors. Since the sleep_date is the PRIMARY KEY, each key must be unqiue
# If a duplicate sleep_date occurs (when rerunning the program), PostgreSQL will see the dupliacte
# and DO NOTHING, will skip insert query

# Fetches all columns from table
cursor.execute("""SELECT * FROM dailysleep;""")
print(cursor.fetchall())

# close
cursor.close()
conn.close()

