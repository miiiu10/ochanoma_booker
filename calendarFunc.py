import datetime
from calendarApi import CalendarApi
from calendarData import CalendarBody, CalendarData

def insert(calData):
    try:
        calendar = CalendarApi()
        calContent = CalendarBody()

        body = calContent.createInsertData(calData)
        result = calendar.insert(body)
        calData.eventId = result["id"]
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

def delete(eventId):
    try:
        calendar = CalendarApi()
        calendar.delete(eventId)
    except Exception as e:
        print(e)

