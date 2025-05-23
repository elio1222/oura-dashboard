from dotenv import load_dotenv
import os
import json
import requests
import psycopg2
import requests
from db_operations.dailysleep import insertDailySleep
from db_operations.sleeproutes import insertSleepRoutes
from db_operations.sleeptime import insertSleepTimeRoutes

#loading environment variables
load_dotenv()
# Connecting to the database
conn = psycopg2.connect(host = os.getenv("hostname"), dbname = "oura", user = "postgres",
                         password = os.getenv("password"), port = 5432)
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
    "end_date": "2025-01-14"
}


#response = requests.request('GET', url, headers=headers, params=params)
#print(response.text)

# sleep_data = requests.get(url, headers=headers, params=params)
# print(json.dumps(sleep_data.json(), indent=2))
# json dumps turns a python object into a json string

#request.get() returns the raw body of the HTTP Response into a Response object
response = requests.get(url, headers=headers, params=params)
# response.text turns this object into pure text, aka a string
# json.loads() converts a JSOn string into a Python object, parses into a python dict/list.
jsondata = json.loads(response.text)
# print(jsondata)

# .json() returns the python dict at once, a shortcut instead of using .text and json.loads()
# print(jsondata['data'][0]['contributors']['deep_sleep'])
# the json data is a list full of dictionaries, hence the ['data'][0] <= first index of data
# the simple examples prints the value of the keys: ['contributors']['deep_sleep']
# print(jsondata['data'][0]['contributors']['deep_sleep'])

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
)); # EXAMPLE OF INSERTION <=

# This function will allow us to enter multiple days of sleep data into the PostgreSQL=        
insertDailySleep(cursor, conn)
# Fetches all columns from table
cursor.execute("""SELECT sleep_date FROM dailysleep WHERE score > 90 LIMIT 3;""")
print(cursor.fetchall())

# inserts sleep routes into database
insertSleepRoutes(cursor, conn)
# Fetches one column from table
cursor.execute("""SELECT COUNT(*) FROM sleeproutes WHERE 
               awake_time < 60000""")
print(cursor.fetchone())

# inserts sleep time routes into database
insertSleepTimeRoutes(cursor, conn)
# Fetches COUNT from table
cursor.execute("""SELECT COUNT(*) FROM sleeptimeroutes""")
print(cursor.fetchone())

# close
cursor.close()
conn.close()

