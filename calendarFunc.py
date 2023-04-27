import datetime
from calendarApi import CalendarApi
from calendarData import CalendarBody, CalendarData

def insert(calData1, calData2):
    try:
        calendar = CalendarApi()
        calContent = CalendarBody()

        body = calContent.createInsertData(calData1, calData2)
        result = calendar.insert(body)
        calData1.eventId = result["id"]
        calData2.eventId = result["id"]
    except Exception as e:
        print(e)

def check_calendar(start_time):
    calendar = CalendarApi()
    try:
        result = calendar.check_calendar(start_time)
        if result == []:
            print('No upcoming events found.')
        else:
            schedule_list = []
            for event in result:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                schedule = {'ID':event["id"], 'StartTime':start, 'EndTime':end, 'Summary':event['summary']}
                schedule_list.append(schedule)
            return schedule_list
    except Exception as e:
        print(e)

def get():
    calendar = CalendarApi()
    try:
        result = calendar.get()
        if result == []:
            print('No upcoming events found.')
        else:
            schedule_list = []
            for event in result:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                schedule = {'ID':event["id"], 'StartTime':start, 'EndTime':end, 'Summary':event['summary']}
                schedule_list.append(schedule)
            return schedule_list
    except Exception as e:
        print(e)

def search_from_name(name):
    calendar = CalendarApi()
    try:
        result = calendar.search_from_name(name)
        if result == []:
            print('No upcoming events found.')
        else:
            schedule_list = []
            for event in result:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                schedule = {'ID':event["id"], 'StartTime':start, 'EndTime':end, 'Summary':event['summary']}
                schedule_list.append(schedule)
            return schedule_list
    except Exception as e:
        print(e)

def delete(eventId):
    try:
        calendar = CalendarApi()
        calendar.delete(eventId)
        return True
    except Exception as e:
        print(e)
        return False

