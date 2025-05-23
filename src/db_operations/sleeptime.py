import os
import json
import requests
from datetime import date, timedelta
import requests

def insertSleepTimeRoutes(cursor, conn):
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