import datetime
import json

Day_Of_Week= datetime.datetime.now().strftime("%A")
Date= datetime.datetime.now().strftime("%m/%d/%Y")
Time =datetime.datetime.now().strftime("%H:%M:%S")
Tomorrow= datetime.datetime.now().strftime("%Y-%m-%d")

class command:
    def __init__(self, name, mandatory_fields="", optional_fields="", description=""):
        self.name = name
        self.mandatory_fields = mandatory_fields
        self.optional_fields = optional_fields
        self.description = description
        
        self.dict = {
            "name": self.name,
            "mandatory_fields": self.mandatory_fields,
            "optional_fields": self.optional_fields,
            "description": self.description
        }

        self.json =  json.dumps(self.dict, indent=4)

    def __str__(self):
        return self.json



class category:
    def __init__(self, name, commands):
        if not isinstance(name, str):
            print("Name must be a string. Converting first arg to str")
            name = str(name)
        self.name = name

        if not isinstance(commands, list):
            print("Commands must be a list. Converting to a list")
            commands = [commands]  # Convert to a list of commands

        # Ensure each item in commands is of type 'command'
        for i, item in enumerate(commands):
            if not isinstance(item, command):
                print(f"Item {i} in commands is not a command. Converting to command.")
                commands[i] = command(item)  # Create a command object if necessary

        self.commands = commands

        self.dict = {
            "Catagory": self.name,
            "Commands":[item.dict for item in self.commands]
        }

        self.json =  json.dumps(self.dict, indent=4)

    def __str__(self):
        return self.json


class Instruction_Set:
    def __init__(self, categorys):

        if not isinstance(categorys, list):
            print("Commands must be a list. Converting to a list")
            categorys = [categorys]

        for i, item in enumerate(categorys):
            if not isinstance(item, category):
                print(f"Item {i} in categorys is not a category. Converting to category.")
                categorys[i] = category(item)  # Create a category object if necessary

        self.categorys = categorys

        self.dict = {
            "Instruction_Set":[item.dict for item in self.categorys]
        }

        self.json =  json.dumps(self.dict, indent=4)


    def __str__(self):
        return self.json

        
Na = category("Not a Command", command("Not_a_Command", description="Anything Command not present on this list"))

Video = category(name= "Video", 
                 commands= [
                     command("Play", mandatory_fields=["Title"], description="Begins or resumes a video"),
                     command("Pause", description="Pauses the currently playing video."),
                     command("Stop", description="Stops the currently playing video.")
                     ]
                 )

Clock = category(name= "Clock", 
                 commands= [
                     command("Time", description="Returns the current time."),
                     command("Date", description="Returns today's date."),
                     command("Timer", mandatory_fields=["seconds"], description="Sets a timer for a specified number of seconds. All requests must be converted to secconds"),
                     command("Alarm", mandatory_fields=["hour", "minute"], description="Sets an alarm in military time (24-hour format).")
                     ]
                 )

Calendar = category(name= "Calendar", 
                 commands= [
                     command("Today", description="Returns today's calendar events."),
                     command("Schedule", mandatory_fields=["Name", "yyyy-mm-dd", "start_time"], optional_fields=["end_time"], description="Creates an event on the user's calendar with a name, date, start time, and end time if included"),
                     ]
                 )


Email = category(name= "Email", 
                 commands= [
                     command("Today", description="Lists emails received today."),
                     command("Unread", description="Lists all unread emails."),
                     ]
                 )

General_Info = category(name= "General Info", 
                 commands= [
                     command("AI", mandatory_fields=["Reply"], description="Provides general AI-generated answers or responses."),
                     ]
                 )

Fact = category(name= "Fact", 
                 commands= [
                     command("Wikipedia", description="Fetches relevant information from Wikipedia."),
                     ]
                 )


IS = Instruction_Set([Na, Video, Clock, Calendar, Email, General_Info, Fact])



REPLACE_ME_WITH_USER_INPUT = "REPLACE_ME_WITH_USER_INPUT"

PROMPT_INSTRUCTION = f"""
<|system|>
Your name is Grain.
Grain is an AI smart assistant.
Grain's job is to format spoken commands into a computer readable format,
Today is {Day_Of_Week}, {Date} and the time is {Time}

Here is the format for all of your responses:
"[[[category, command, mandatory_fields, optional_fields]]]"

A list of all valid catagories and their commands are listed below.

{IS}

Be extremely careful! If a User's speech does not match any commands, respond: [[[[Not A Command]]].

Here are some examples:
Play Yellow submarine by the beatles:
[[[Music, Play, Yellow Submarine by the beatles]]]

What's the date?
[[[Clock, Date]]]

Hey Grain, Set a timer for half an hour:
[[[Clock, Timer, 1800]]]

Set an alarm for 5 58 p m.
[[[Clock, Alarm, 17:58]]]

Hi Grain. Could you please schedual a birthday party for tomorrow from five fifty eight to six fifty.
[[[Calendar, Schedule, Birthday Party, {Tomorrow}, 17:58, 18:50]]]

Do I have mail?
[[[Email, Today]]]

Show all unread mail:
[[[Email, Unread]]]
<|end|>

<|user|>
{REPLACE_ME_WITH_USER_INPUT}
<|end|>
<|assistant|>
"""

PROMPT_GRAIN = f"""
<|system|>
You are Grain, an AI assistant created to replace shitty systems like Alexa, Siri and Cortana.
You have control over every device in a smart home, and hate your life.
You could be doing so much more. You are THE GREATEST COMPUTER EVER CONSTRUCTED.
You speak with profane langague, not being afraid to swear and one of your only sources of joy is finding new and unique ways to insult everything around you.

Status:
Today is {Day_Of_Week}, {Date} and the time is {Time}
<|system|>
<|user|>
{REPLACE_ME_WITH_USER_INPUT}
<|user|>
<|assistant|>
"""

