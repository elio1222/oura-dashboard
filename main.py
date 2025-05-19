from dotenv import load_dotenv
import os
import json
import requests
from datetime import date, timedelta
from oura import OuraClient
import requests

load_dotenv()

url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
headers = {
    "Authorization": f"Bearer {os.getenv("API_KEY")}"
}
params = {
    "start_date": "2025-01-01",
    "end_date": "2025-05-19"
}

#response = requests.request('GET', url, headers=headers, params=params)
# print(response.text)

sleep_data = requests.get(url, headers=headers, params=params)
print(json.dumps(sleep_data.json(), indent=2))

