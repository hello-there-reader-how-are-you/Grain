
import datetime

import num2words


from datetime import datetime, timedelta, timezone
from num2words import num2words

class CalendarService:
    def __init__(self, service):
        self.service = service

    def events_today_pretty(self):
        start = datetime.now(timezone.utc).isoformat()
        end = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        events = self.service.events().list(calendarId="primary", timeMin=start, timeMax=end, singleEvents=True, orderBy="startTime").execute().get("items", [])
        
        # Convert event times and names to a list
        formatted_events = []
        for event in events:
            name = event["summary"]
            start_time = datetime.fromisoformat(event["start"]["dateTime"])
            end_time = datetime.fromisoformat(event["end"]["dateTime"])
            formatted_events.append([name, start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p")])

        # Creating the formatted string
            pretty_events = "Here are your events for today. " + " and ".join(
                [f"You have {event[0]} from {time_to_words(event[1])} to {time_to_words(event[2])}" for event in formatted_events]
            ) + "."

        return pretty_events
        
        # Function to convert time to words
        def time_to_words(time_str):
            time_obj = datetime.strptime(time_str, "%I:%M %p")
            hours = time_obj.strftime("%I").lstrip('0')
            minutes = time_obj.strftime("%M")
            period = time_obj.strftime("%p").lower()
            
            if hours == "12" and minutes == "00" and period == "am":
                return "midnight"
            elif hours == "12" and minutes == "00" and period == "pm":
                return "noon"
            else:
                hour_word = num2words(int(hours))
                minute_word = num2words(int(minutes)) if int(minutes) != 0 else "o'clock"
                return f"{hour_word} {minute_word} {period}"



# Example usage
# Assuming 'service' is a valid Google Calendar API service instance
calendar_service = CalendarService(service)
print(calendar_service.events_today_pretty())
