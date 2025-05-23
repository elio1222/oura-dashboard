import os
import json
import requests
from datetime import date, timedelta
import requests

# SAMPLE
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

def insertDailySleep(cursor, conn):
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
        conn.commit() # <= saves into database

# '%s' acts as placeholders since a QUERY line of code cannot read python code,
# that is why the python code is outside the query line of code
# In order to rerun the program without getting a psycopg2.errors.UniqueViolatoin error, 
# we must add the line 'ON CONFLICT (sleep_date) DO NOTHING' which enables us to rerun the
# program without any errors. Since the sleep_date is the PRIMARY KEY, each key must be unqiue
# If a duplicate sleep_date occurs (when rerunning the program), PostgreSQL will see the dupliacte
# and DO NOTHING, will skip insert query