import os
import json
import requests
from datetime import date, timedelta
import requests

def insertSleepRoutes(cursor, conn):
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
