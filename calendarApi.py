import os
import datetime
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build


class CalendarApi():
    def __init__(self):
        self.__calendarId = os.getenv("CALENDAR_ID")

        SCOPES = [os.getenv("CALENDAR_SCOPES")]
        gapi_creds = load_credentials_from_file('google_calendar_key.json', SCOPES)[0]
        self.__service = build('calendar', 'v3', credentials=gapi_creds)

    @property
    def calendarUrl(self):
        return self.__calendarUrl

    @property
    def calendarId(self):
        return self.__calendarId

    @property
    def service(self):
        return self.__service

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, val):
        self.__body = val

    @property
    def eventId(self):
        return self.__eventId

    @eventId.setter
    def eventId(self, val):
        self.__eventId = val

    def get(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        nextWeek = now + datetime.timedelta(days=30)
        timeMax = datetime.datetime(nextWeek.year, nextWeek.month, nextWeek.day, 23, 59, tzinfo=datetime.timezone.utc)

        events_result = self.service.events().list(
            calendarId=self.calendarId,
            timeMin=now.isoformat(),
            timeMax=timeMax.isoformat(),
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return events

    def check_calendar(self, start_time):
        checkDay = start_time
        timeMin = datetime.datetime(checkDay.year, checkDay.month, checkDay.day, 0, 0, tzinfo=datetime.timezone.utc)
        timeMax = datetime.datetime(checkDay.year, checkDay.month, checkDay.day, 23, 59, tzinfo=datetime.timezone.utc)

        events_result = self.service.events().list(
            calendarId=self.calendarId,
            timeMin=timeMin.isoformat(),
            timeMax=timeMax.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return events

    def search_from_name(self, name):
        now = datetime.datetime.now(datetime.timezone.utc)

        events_result = self.service.events().list(
            calendarId=self.calendarId,
            timeMin=now.isoformat(),
            q=name,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return events

    def insert(self, body):
        result = self.service.events().insert(calendarId=self.calendarId, body=body).execute()
        return result

    def delete(self, eventId):
        result = self.service.events().delete(calendarId=self.calendarId, eventId=eventId).execute()
        return result
