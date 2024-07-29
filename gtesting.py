from llama_cpp import Llama
from clock import *
from youtube import *
from Prompt import *
import re
import time
import datetime
from calender import *
from mail import *

jukebox = yt()
watch = clock()
cal = calender()
postman = mailbox()

#speech = "Hey Grain, set a time for 5 seconds"
#speech = "Play radio gaga by queen"
llm_nlp = Llama(model_path="./models/Phi-3-mini-4k-instruct-q4.gguf", n_gpu_layers=-1)
print("\n\n\n")
#llm_Grain = Llama(model_path="./models/dolphin-2.9.3-mistral-nemo-Q5_K_M.gguf")
#print("\n\n\n\n\n\n")

def nlp(question):
      x = llm_nlp(
            PROMPT_INSTRUCTION.format( datetime.datetime.now().strftime("%A"), datetime.datetime.now().strftime("%m/%d/%Y"), datetime.datetime.now().strftime("%H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d"), question),
            max_tokens=400,
            seed=420,
            echo=False,
            stop= ["<|end|>"],
      )["choices"][0]["text"]
      print(x)
      try: x = f"{re.search(r'\[\[.*?\[(.*?)\].*?\]\]', x).group(1)}".split(", ")
      except: 
            #print("faild to find [[[command]]], lowering confedence")
            try: x = f"{re.findall(r'\[(?![^\[\]]*\[)([^\[\]]+)\]', x)[-1]}".split(", ")
            except: pass #print("faild to find [command], AT LOW CONDFEDENCE")

      if type(x) == list: x = [item for item in x if item != "None"]
      print(x)
      if type(x) == list: return x
      else: return "No command found"
"""
def personality(question):
      x = llm_Grain(
            PROMPT_GRAIN.format(question),
            #temperature=0.3
            max_tokens=400,
            seed=420,
            stop= ["<|im_end|>"],
      )["choices"][0]["text"]
      return x
"""

def action(command):
      if type(command) != list: return

      if command[0] == "Music" or command[0] == "Video":
            print("Music!")
            if command[1] == "Play":
                  print("Play!")
                  jukebox.set_search_term(''.join(command[2:]))
            if command[1] == "Pause" or command[0] ==  "Stop":
                  print("Pause!")
                  jukebox.pause()

      if command[0] == "Clock":
            print("Clock!")
            if command[1] == "Time":
                  print("Time!")
                  print(watch.time_pretty())
            if command[1] == "Date":
                  print("Date!")
                  print(watch.date_words())
            if command[1] == "Timer":
                  print("Timer!")
                  try: watch.timer(int(command[2]))
                  except: pass
            if command[1] == "Alarm":
                  print("Alarm!")
                  try: watch.alarm(command[2])
                  except: pass  

      if command[0] == "Calender":
            print("Calender!")
            if command[1] == "Today":
                  print("Today!")
                  print(cal.events_today_pretty())
            if command[1] == "Schedule":
                  print("Schedule!")
                  event = booking(command[2], datetime.datetime.strptime(f"{command[3]} {command[4]}", "%Y-%m-%d %H:%M"), datetime.datetime.strptime(f"{command[3]} {command[5]}", "%Y-%m-%d %H:%M"))
                  print(event)
                  cal.schedule(event)
      
      if command[0] == "Email":
            if command[1] == "Today":
                  print(postman.emails_today())
            if command[1] == "Unread":
                  print(postman.unread())
      print("")
         

text = "Hey grain, what unread emails do I have?"

action(nlp(question=text))

time.sleep(500)


#CMAKE_ARGS="-DGGML_METAL=on" pip install --force-reinstall --upgrade --no-cache-dir  -v "llama_cpp_python==0.2.83"    