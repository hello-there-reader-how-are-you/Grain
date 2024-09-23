#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#https://calendar.google.com/calendar/u/0/r

import pytz
import datetime
import os.path
import num2words

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


cred_file = "./ignore_me/credentials.json"
token_file = "./ignore_me/token.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class calender():
    def __init__(self):
        self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        self.service = build("calendar", "v3", credentials=self.creds)

    
    def events_today(self):
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        end = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        events = self.service.events().list(calendarId = "primary", timeMin=start, timeMax=end, singleEvents=True, orderBy="startTime").execute().get("items", [])
        for i in range(len(events)):
            events[i] = booking(name=events[i]["summary"], start_time=datetime.datetime.fromisoformat(events[i]["start"]["dateTime"]), end_time=datetime.datetime.fromisoformat(events[i]["end"]["dateTime"]))
            #events[i] = [events[i]["summary"], datetime.datetime.fromisoformat(events[i]["start"]["dateTime"]), datetime.datetime.fromisoformat(events[i]["end"]["dateTime"])]
        return events
    
    def events_today_pretty(self):
            start = datetime.datetime.now(datetime.timezone.utc).isoformat()
            end = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
            events = self.service.events().list(calendarId="primary", timeMin=start, timeMax=end, singleEvents=True, orderBy="startTime").execute().get("items", [])
            
            # Convert event times and names to a list
            formatted_events = []
            for event in events:
                name = event["summary"]
                start_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
                end_time = datetime.datetime.fromisoformat(event["end"]["dateTime"])
                formatted_events.append([name, start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p")])
            
            # Function to convert time to words
            def time_to_words(time_str):
                time_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
                hours = time_obj.strftime("%I").lstrip('0')
                minutes = time_obj.strftime("%M")
                period = time_obj.strftime("%p").lower()
                
                if hours == "12" and minutes == "00" and period == "am":
                    return "midnight"
                elif hours == "12" and minutes == "00" and period == "pm":
                    return "noon"
                else:
                    hour_word = num2words.num2words(int(hours))
                    minute_word = num2words.num2words(int(minutes)) if int(minutes) != 0 else "o'clock"
                    return f"{hour_word} {minute_word} {period}"
                
            # Creating the formatted string
            pretty_events = "Here are your events for today: " + ", ".join([f"You have {event[0]} from {time_to_words(event[1])} to {time_to_words(event[2])}" for event in formatted_events]) + "."
            return pretty_events


    def schedule(self, book):
        #tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        tz = list(filter(lambda x: datetime.datetime.now(pytz.timezone(x)).strftime("%Z") == str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo), pytz.common_timezones))[0]
        event = {
        'summary': book.name,
        'location': 'location',
        'description': 'description',
        'start': {
            'dateTime': book.start.isoformat(),
            'timeZone': tz,
        },
        'end': {
            'dateTime': book.start.isoformat(),
            'timeZone': tz,
        }
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()

        check = self.service.events().list(calendarId = "primary", singleEvents=True, orderBy="startTime").execute().get("items", [])
        print(check)
        book.name


class booking():
    def __init__(self, name, start_time, end_time) -> None:
        self.name = name
        if end_time == start_time:
            end_time = start_time + datetime.timedelta(minutes=30)
        self.start = start_time
        self.end = end_time
    def __repr__(self) -> str:
        return f"{self.name}, {self.start}, {self.end}"
    def to_list(self):
        return [self.name, self.start, self.end]



