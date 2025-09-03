from flask import Flask, render_template, request, url_for, redirect, jsonify
from dotenv import load_dotenv
import os
import json
import requests
import psycopg2
import requests
import datetime
#loading environment variables
load_dotenv()

#connecting to database
conn = psycopg2.connect(host = os.getenv("hostname"), dbname = "oura", user = "postgres", password = os.getenv("password"), port = 5432)
cursor = conn.cursor()


app = Flask(__name__)



@app.route("/", methods = ['POST', 'GET'])
def index():
  return render_template('index.html')

@app.route("/database", methods = ['POST', 'GET'])
# this piece of code is connecting to our postgresql databse.
# reminder: the data in the database is from the 2025 spring semester only, in order to extract data outside that scope, we must fetch data from the OURA API. 
def connectingToDatabase():
  cursor.execute("""SELECT score, sleep_date FROM dailysleep;""")
  data = cursor.fetchall()
  return jsonify(data)

@app.route("/oura/api/daily_sleep", methods = ['POST', 'GET'])
def connectingToOura():
  url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
  headers = {
    "Authorization": f"Bearer {os.getenv("API_KEY")}"
  }

  #getting last 7 days
  today = datetime.date.today()
  sevenDaysAgo = today - datetime.timedelta(days=7)

  params = {
    "start_date": f"{sevenDaysAgo}",
    "end_date": f"{today}"
  }
  response = requests.get(url, headers=headers, params=params)

  data = json.loads(response.text)
  return jsonify(data)

@app.route("/oura/api/sleeptimes")
def getSleepTimes():
  url = "https://api.ouraring.com/v2/usercollection/sleep"
  headers = {
    "Authorization": f"Bearer {os.getenv("API_KEY")}"
  }

  today = datetime.date.today()
  sevenDaysAgo = today - datetime.timedelta(days=7)
  params = {
    "start_date": f"{sevenDaysAgo}",
    "end_date": f"{today}"
  }
  response = requests.get(url, headers=headers, params=params)

  data = json.loads(response.text)
  return jsonify(data)

if __name__== "__main__":
  app.run(debug=True, port=8080)



