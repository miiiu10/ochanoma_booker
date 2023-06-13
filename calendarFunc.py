import logging
from typing import Optional, Tuple
from calendarApi import CalendarApi


def insert(start_dt, end_dt, name, description) -> Tuple[Optional[dict], Optional[str]]:
    "Add a reservation with Google Calendar API"
    try:
        calendar = CalendarApi()

        body = {
            "summary": name,
            "description": description,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "Japan",
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "Japan",
            },
        }
        result = calendar.insert(body)
        return (result, None)
    except Exception as e:
        return (None, e)


def check_calendar(start_time):
    calendar = CalendarApi()
    try:
        result = calendar.check_calendar(start_time)
        if result == []:
            print("No upcoming events found.")
        else:
            schedule_list = []
            for event in result:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                schedule = {
                    "ID": event["id"],
                    "StartTime": start,
                    "EndTime": end,
                    "Summary": event["summary"],
                }
                schedule_list.append(schedule)
            return schedule_list
    except Exception as e:
        print(e)


def get():
    calendar = CalendarApi()
    try:
        result = calendar.get()
        if result == []:
            print("No upcoming events found.")
        else:
            schedule_list = []
            for event in result:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                schedule = {
                    "ID": event["id"],
                    "StartTime": start,
                    "EndTime": end,
                    "Summary": event["summary"],
                }
                schedule_list.append(schedule)
            return schedule_list
    except Exception as e:
        print(e)


def search_from_name(name):
    calendar = CalendarApi()
    try:
        result = calendar.search_from_name(name)
        if result == []:
            print("No upcoming events found.")
        else:
            schedule_list = []
            for event in result:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                schedule = {
                    "ID": event["id"],
                    "StartTime": start,
                    "EndTime": end,
                    "Summary": event["summary"],
                }
                schedule_list.append(schedule)
            return schedule_list
    except Exception as e:
        print(e)


def delete(event_id: str) -> bool:
    try:
        calendar = CalendarApi()
        calendar.delete(event_id)
        return False
    except Exception as e:
        logging.error(e)
        return True
