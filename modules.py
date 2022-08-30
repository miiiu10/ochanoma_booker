import sys
import datetime
import urllib.parse
import pandas as pd
import os.path as osp
from messages import gen_text, message_random

sys.path.append(osp.join(osp.dirname(osp.abspath(__file__)), 'json'))
from views import view_schedule

from calendarApi import CalendarApi
from calendarData import CalendarBody, CalendarData
from calendarFunc import *

def manage_info(user, add, date='2022-08-15', time='00:00', description='', event_id=''):
    df = pd.read_csv('iiclab_member.csv')
    _df = df[df['id']==user]
    name = _df['name'].unique()[0]

    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))

    if add:
        calData = CalendarData()
        calData.year = year
        calData.month = month
        calData.day = day
        calData.hour = hour
        calData.minute = minute
        calData.summary = '{}'.format(name)
        calData.description = description

        insert(calData)

    else:
        schedules = get()
        if schedules:
            for s in schedules:
                if s['ID']==event_id:
                    delete(s['ID'])

    schedules = get()
    ui = view_schedule(schedule2txt(schedules))

    return ui

def schedule2txt(schedules):
    txt=''
    if schedules:
        for s in schedules:
            start_dt = str2datetime(s['StartTime'])
            end_dt = str2datetime(s['EndTime'])
            txt += 'ID: {}\nTime: {} ~ {}\nUser: {}\n------------------------------------------------------\n'.format(s['ID'], start_dt, end_dt, s['Summary'])
    else:
        txt = 'No upcoming events found.'
    return txt

def str2datetime(str):
    date, time = str.split('T')
    time = time.split('+')[0][:-3]
    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))
    dt = datetime.datetime(year, month, day, hour, minute)
    return dt