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
'''
{
  "data": [
    {
      "id": "388b3215-9203-421d-a61e-08c2b5e1f08d",
      "contributors": {
        "deep_sleep": 99,
        "efficiency": 99,
        "latency": 86,
        "rem_sleep": 86,
        "restfulness": 98,
        "timing": 100,
        "total_sleep": 79
      },
      "day": "2025-01-13",
      "score": 89,
      "timestamp": "2025-01-13T00:00:00+00:00"
    },
    {
      "id": "57e66043-b16b-43b0-9864-7e248e2e6f05",
      "contributors": {
        "deep_sleep": 97,
        "efficiency": 93,
        "latency": 83,
        "rem_sleep": 90,
        "restfulness": 90,
        "timing": 100,
        "total_sleep": 73
      },
      "day": "2025-01-14",
      "score": 85,
      "timestamp": "2025-01-14T00:00:00+00:00"
    }
  ],
  "next_token": null
}
'''
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
)); 
# This function will allow us to enter multiple days of sleep data into the PostgreSQL

def insertDailySleep():
    insertQuery = """INSERT INTO dailysleep (
    sleep_date, deep_sleep, efficiency, latency, rem_sleep, restfulness, 
    timing, total_sleep, score
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (sleep_date) DO NOTHING;"""

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
        "end_date": "2025-05-10"
    }
    response = requests.get(url, headers=headers, params=params)
    # json dumps to convert from python object to json string
    # json loads converts json string to python list / dict.
    # in order to use a for loop to place each row of data into the database
    data = json.loads(response.text)

    for i, rows in enumerate(data['data']): # <= ????? no idea but works for sleepday
        if i == 0:
            continue # skips first iteration
        sleepday = rows['day'] # <= I HAVE NO IDEA HOW THIS WORKS
        cursor.execute(insertQuery, (
            sleepday,
            int(rows['contributors']['deep_sleep']),
            int(rows['contributors']['efficiency']),
            int(rows['contributors']['latency']),
            int(rows['contributors']['rem_sleep']),
            int(rows['contributors']['restfulness']),
            int(rows['contributors']['timing']),
            int(rows['contributors']['total_sleep']),
            int(rows['score'])
            )) # executes the rest of the iterations of data from 1.13-5.10
        
insertDailySleep()
conn.commit() # <= saves into database
# '%s' acts as placeholders since a QUERY line of code cannot read python code,
# that is why the python code is outside the query line of code
# In order to rerun the program without getting a psycopg2.errors.UniqueViolatoin error, 
# we must add the line 'ON CONFLICT (sleep_date) DO NOTHING' which enables us to rerun the
# program without any errors. Since the sleep_date is the PRIMARY KEY, each key must be unqiue
# If a duplicate sleep_date occurs (when rerunning the program), PostgreSQL will see the dupliacte
# and DO NOTHING, will skip insert query

# Fetches all columns from table
cursor.execute("""SELECT sleep_date FROM dailysleep WHERE score > 90 LIMIT 3;""")
print(cursor.fetchall())

# inserts sleep routes into database
def insertSleepRoutes():
    url = 'https://api.ouraring.com/v2/usercollection/sleep'
    params = {
        'start_date': '2025-01-13',
        'end_date': '2025-05-10'
    }
    headers = {
        'Authorization': f'Bearer {os.getenv("API_KEY")}'
    }
    response = requests.get(url, headers=headers, params=params)
    sleeproutes = response.json()

    insertQuery = """INSERT INTO sleeproutes (
    sleep_date, avg_breath, avg_heartrate, avg_hrv,
    deepsleep_effic, bedtime_start, bedtime_end,
    time_in_bed, awake_time, totalsleep_dur)
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
    ON CONFLICT (sleep_date) DO NOTHING"""
    # JSON STRING FROM OURA API SAMPLE
    '''
    {
  "data": [
    {
      "id": "string",
      "average_breath": 0,
      "average_heart_rate": 0,
      "average_hrv": 0,
      "awake_time": 0,
      "bedtime_end": "string",
      "bedtime_start": "string",
      "day": "2019-08-24",
      "deep_sleep_duration": 0,
      "efficiency": 0,
      "heart_rate": {
        "interval": 0,
        "items": [
          0
        ],
        "timestamp": "string"
      },
      "hrv": {
        "interval": 0,
        "items": [
          0
        ],
        "timestamp": "string"
      },
      "latency": 0,
      "light_sleep_duration": 0,
      "low_battery_alert": true,
      "lowest_heart_rate": 0,
      "movement_30_sec": "string",
      "period": 0,
      "readiness": {
        "contributors": {
          "activity_balance": 0,
          "body_temperature": 0,
          "hrv_balance": 0,
          "previous_day_activity": 0,
          "previous_night": 0,
          "recovery_index": 0,
          "resting_heart_rate": 0,
          "sleep_balance": 0
        },
        "score": 0,
        "temperature_deviation": 0,
        "temperature_trend_deviation": 0
      },
      "readiness_score_delta": 0,
      "rem_sleep_duration": 0,
      "restless_periods": 0,
      "sleep_phase_5_min": "string",
      "sleep_score_delta": 0,
      "sleep_algorithm_version": "v1",
      "time_in_bed": 0,
      "total_sleep_duration": 0,
      "type": "deleted"
    }
  ],
  "next_token": "string"
}
    '''
    for data in sleeproutes['data']:
        cursor.execute(insertQuery,
                (
                data['day'],
                int(data['average_breath']),
                int(data['average_heart_rate']),
                int(data['average_hrv'] or 0),
                int(data['deep_sleep_duration']),
                data['bedtime_start'],
                data['bedtime_end'],
                int(data['time_in_bed']),
                int(data['awake_time']),
                int(data['total_sleep_duration'])
                ))
        
    conn.commit()

insertSleepRoutes()
cursor.execute("""SELECT COUNT(*) FROM sleeproutes WHERE 
               awake_time < 60000""")
print(cursor.fetchone())
# inserts sleep time routes into database
def insertSleepTimeRoutes():
    url = "https://api.ouraring.com/v2/usercollection/sleep_time"
    headers = {
        "Authorization": f"Bearer {os.getenv("API_KEY")}"
    }
    params = {
        "start_date": "2025-01-13",
        "end_date": "2025-05-10"
    }

    response = requests.get(url, headers=headers, params=params)
    timeroutes = response.json()

    insertQuery = """INSERT INTO sleeptimeroutes (
    day, day_tz, start_offset, end_offset, recommendation, daystatus)
    VALUES ( %s, %s, %s, %s, %s, %s)
    ON CONFLICT (day) DO NOTHING"""
    # JSON STRING FROM OURA API SAMPLE
    '''
    {
  "data": [
    {
      "id": "string",
      "day": "2019-08-24",
      "optimal_bedtime": {
        "day_tz": 0,
        "end_offset": 0,
        "start_offset": 0
      },
      "recommendation": "improve_efficiency",
      "status": "not_enough_nights"
    }
  ],
  "next_token": "string"
}
    '''
    #print(timeroutes) <= for debugging purposes
    '''
    for times in timeroutes['data']:
      print(times)  # See the full dictionary
      print(times['day'])  # Does this key exist?
      print(times['optimal_bedtime'])  # Is it a dict?
      print(times['optimal_bedtime']['day_tz'])  # Does this key exist?
      print(times['recommendation'])  # Exists?
    '''

    for times in timeroutes['data']:
        cursor.execute(insertQuery, (
            times['day'],
            int(times['optimal_bedtime']['day_tz']),
            int(times['optimal_bedtime']['start_offset']),
            int(times['optimal_bedtime']['end_offset']),
            times['recommendation'],
            times['status']
        ))
    conn.commit()
insertSleepTimeRoutes()
cursor.execute("""SELECT COUNT(*) FROM sleeptimeroutes""")
print(cursor.fetchone())
# close
cursor.close()
conn.close()

