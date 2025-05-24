import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

def generateScorePlot(cursor, conn):
    cursor.execute("""SELECT score, sleep_date FROM dailysleep;""")
    data = cursor.fetchall()
    scores = [sc[0] for sc in data] # <= turns tuple into list
    dates = [dts[1] for dts in data] 

    fig, ax = plt.subplots(figsize=(40, 7))

    ax.stem(dates, scores)
    plt.xticks(rotation = 90)
    plt.xlabel("Day")
    plt.ylabel("Score")
    plt.title("Sleep Scores Over Spring 2025 Semester")


    plt.show()


    