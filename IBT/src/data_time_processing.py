# -*- coding: utf-8 -*-
"""
 Project: Bachelor thesis
 Theme: Physiological Data to Analyze and Improve the User Experience
 Author: Daniel Stepanek
 License: GPL 3.0

 VUT FIT Brno 2021

"""

import datetime
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
    Get daytime from timestamps. Make statistic of data by daytime when they have been received.

"""

path = os.path.dirname(os.getcwd())
path = '{}/data'.format(path)


timestamp_dict = {}

emotions = []
day_time = {'morning' : 0, 'noon' : 0, 'afternoon' : 0, 'evening' : 0, 'night' : 0}
for folder in os.listdir(path):
    if not os.path.isdir('{}/{}'.format(path, folder)):
        continue
    ts = folder.split('_')

    day = ts[1][:3]
    month = ts[1][3:6]
    if len(ts[1]) % 2 == 0:
        date = ts[1][6:8]
        hour = ts[1][8:10]
    else:
        date = ts[1][6:7]
        hour = ts[1][7:9]

    minutes = ts[2]
    seconds = ts[3][:2]
    year = ts[3][2:]

    time = '{} {}\t{} {}:{}:{} {}'.format(day, month, date, hour, minutes, seconds, year)
    time = datetime.datetime.strptime(time, "%a %b %d %H:%M:%S %Y")
    time_ts = time.timestamp()

    timestamp_dict[time_ts] = folder
    if not ts[0] in emotions:
        emotions += [ts[0]]

    hour = int(hour)

    if hour >= 4 and hour < 11:
        day_time['morning'] += 1
    elif hour >= 11 and hour < 13:
        day_time['noon'] += 1
    elif hour >= 13 and hour < 18:
        day_time['afternoon'] += 1
    elif hour >= 18 and hour < 22:
        day_time['evening'] += 1
    elif (hour >= 22 and hour < 24) or (hour >= 0 and hour < 4):
        day_time['night'] += 1


print('-----------------------')
for k, v in day_time.items():
    print(/{k} : {v}')
print('-----------------------')
