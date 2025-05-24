import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

def generatePlot(cursor, conn):
    cursor.execute("""SELECT sleep_date FROM dailysleep;""")
    result = cursor.fetchall()
    # datelist = list(result)
    datelist = [date[0] for date in result]
    newdates = []
    whatisit = type(datelist[0]) # <= debugging to see what type it is <datatime.data>
    for dates in datelist:
        stringdates = str(dates) # <= turns datatime.data into a string
        newdates.append(stringdates)
    # print(newdates)

    cursor.execute("""SELECT deep_sleep FROM dailysleep;""")
    result = cursor.fetchall()
    deep_sleep = [dsleep[0] for dsleep in result]
    # print(deep_sleep)

    cursor.execute("""SELECT rem_sleep FROM dailysleep;""")
    result = cursor.fetchall()
    rem_sleep = [rsleep[0] for rsleep in result]

    #  = np.vstack([deep_sleep, rem_sleep)

    fig, ax = plt.subplots(figsize=(45, 7))
    # ax.stackplot(newdates, y, labels=labels)
    ax.plot(newdates, deep_sleep, label="Deep Sleep")
    ax.plot(newdates, rem_sleep, label="Rem Sleep")

    plt.xticks(rotation = 90)
    plt.xlabel("Day")
    plt.ylabel("Score")
    plt.title("Deep & REM Sleep Over Spring 2025 Semester")
    plt.tight_layout(pad=1.5)
    plt.legend(loc=(0.8, 0.1))

    plt.show()


