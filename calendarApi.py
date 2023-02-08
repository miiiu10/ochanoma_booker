from configparser import ConfigParser
import errno
import os
import re
import json
import datetime
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build
from calendarData import CalendarData

class CalendarApi():
    def __init__(self):
        config = ConfigParser()
        config_path = './bolt_config.ini'
        if not os.path.exists(config_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
        config.read(config_path)
        self.__calendarId = config["CALENDAR"]["id"]

        SCOPES = [config["CALENDAR"]["scopes"]]
        gapi_creds = load_credentials_from_file('json/google_calendar_key.json', SCOPES)[0]
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
        results = []
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

    def check_calendar(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        nextDay = now + datetime.timedelta(days=1)
        timeMax = datetime.datetime(nextDay.year, nextDay.month, nextDay.day, 23, 59, tzinfo=datetime.timezone.utc)

        events_result = self.service.events().list(
            calendarId=self.calendarId,
            timeMin=now.isoformat(),
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