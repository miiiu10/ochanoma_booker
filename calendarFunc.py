import datetime
from calendarApi import CalendarApi


def insert(calData1, calData2):
    try:
        calendar = CalendarApi()

        body = create_insert_data(calData1, calData2)
        result = calendar.insert(body)
        calData1.eventId = result["id"]
        calData2.eventId = result["id"]
    except Exception as e:
        print(e)


def create_insert_data(data1, data2):
    body = {
        'summary':data1.summary,
        'description': data1.description,
        'start':{
            'dateTime': datetime.datetime(data1.year, data1.month, data1.day, data1.hour, data1.minute).isoformat(),
            'timeZone': 'Japan'
        },
        'end': {
            'dateTime': datetime.datetime(data2.year, data2.month, data2.day, data2.hour, data2.minute).isoformat(),
            'timeZone': 'Japan'
        },
    }
    return body


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

