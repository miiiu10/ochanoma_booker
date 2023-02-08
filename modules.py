import sys
import datetime
import urllib.parse
import pandas as pd
import os.path as osp
from messages import gen_text, message_random

sys.path.append(osp.join(osp.dirname(osp.abspath(__file__)), 'json'))
from views import view_schedule, view_duplicate, view_delete_fail

from calendarApi import CalendarApi
from calendarData import CalendarBody, CalendarData
from calendarFunc import insert, get, delete, search_from_name, cheack_calendar

def manage_info(user, add, date='2022-08-15', start_time='00:00', end_time='00:01', description='', event_id=''):
    df = pd.read_csv('iiclab_member.csv')
    _df = df[df['id']==user]
    name = _df['name'].unique()[0]

    year, month, day = map(int, date.split('-'))
    s_hour, s_minute = map(int, start_time.split(':'))
    if end_time==None:
        e_hour = s_hour + 1
        e_minute = s_minute + 1
    else:
        e_hour, e_minute = map(int, end_time.split(':'))

    check_frag = True
    if add:
        s_calData = CalendarData()
        s_calData.year = year
        s_calData.month = month
        s_calData.day = day
        s_calData.hour = s_hour
        s_calData.minute = s_minute
        s_calData.summary = '{}'.format(name)
        s_calData.description = description

        e_calData = CalendarData()
        e_calData.year = year
        e_calData.month = month
        e_calData.day = day
        e_calData.hour = e_hour
        e_calData.minute = e_minute
        e_calData.summary = '{}'.format(name)
        e_calData.description = description

        schedules = cheack_calendar()
        s_dt_add = datetime.datetime(year, month, day, s_hour, s_minute)
        e_dt_add = datetime.datetime(year, month, day, e_hour, e_minute)
        if schedules:
            for s in schedules:
                start_dt = str2datetime(s['StartTime'])
                end_dt = str2datetime(s['EndTime'])
                if (start_dt < e_dt_add) and (s_dt_add < end_dt):
                    check_frag = False

        if check_frag:
            insert(s_calData, e_calData)
        else:
            print('予定が被っています。')

        return check_frag

    else:
        schedules = get()
        if schedules:
            for s in schedules:
                if s['ID']==event_id:
                    delete(s['ID'])
                    return check_frag

        check_frag=False
        return check_frag

def delete_from_chat(user, date, time):
    df = pd.read_csv('iiclab_member.csv')
    _df = df[df['id']==user]
    name = _df['name'].unique()[0]

    year, month, day = map(int, date.split('-'))
    s_time, e_time = time.split('~')
    s_hour, s_minute = map(int, s_time.split(':'))
    e_hour, e_minute = map(int, e_time.split(':'))
    s_dt_delete = datetime.datetime(year, month, day, s_hour, s_minute)
    e_dt_delete = datetime.datetime(year, month, day, e_hour, e_minute)

    check_frag = True
    schedules = search_from_name(name)

    if schedules:
        for s in schedules:
            start_dt = str2datetime(s['StartTime'])
            end_dt = str2datetime(s['EndTime'])
            if start_dt==s_dt_delete and end_dt==e_dt_delete:
                delete(s['ID'])
                return check_frag

    check_frag=False
    return check_frag


def schedule2txt(schedules):
    txt=''
    if schedules:
        for s in schedules:
            start_dt = str2datetime(s['StartTime'])
            end_dt = str2datetime(s['EndTime'])
            txt += 'ID: {}\nTime: {}:{} ~ {}:{}\nUser: {}\n------------------------------------------------------\n'.format(s['ID'], start_dt.hour, start_dt.minute, end_dt.hour, end_dt.minute, s['Summary'])
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

def is_overlap_time(starttime1, endtime1, starttime2, endtime2):
    return starttime1 <= endtime2 and endtime1 >= starttime2