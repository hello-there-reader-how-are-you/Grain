from llama_cpp import Llama
from styletts2 import tts

import speech_recognition as sr
from openwakeword.model import Model

import sys
import re
import time
import datetime
import threading
import numpy as np
import random
import json

import pyaudio
import pyvolume

from modules.clock import *
from modules.youtube import *
from modules.calender import *
from modules.mail import *
from Prompt import *

PATH_TO_NLP_MODEL = "./models/Meta-Llama-3.1-8B-Instruct-Q4_K_L.gguf"
PATH_TO_PERSONALITY_MODEL = PATH_TO_NLP_MODEL

mouth = tts.StyleTTS2()
jukebox = yt()
watch = clock()
cal = calender()
postman = mailbox()

with open("holdover.json", "r") as file:
    HOLDOVER = json.load(file)

def hold():
      with open("holdover.json", "w") as json_file:
            json.dump(HOLDOVER, json_file)

Person = "Off"                         # Full, Limited, Off,

llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_gpu_layers=-1)

print("\n\n\n")
llm_Grain = llm_nlp

#print("\n\n\n\n\n\n")

def nlp(question):
      x = llm_nlp(
            PROMPT_INSTRUCTION.format(Day_Of_Week= datetime.datetime.now().strftime("%A"), Date= datetime.datetime.now().strftime("%m/%d/%Y"), Time =datetime.datetime.now().strftime("%H:%M:%S"), Tomorrow= datetime.datetime.now().strftime("%Y-%m-%d"), User_Input= question),
            max_tokens=400,
            seed=420,
            echo=False,
            stop= ["<|end|>", "|</assistant|>", "<|end_of_text|>"],
      )["choices"][0]["text"]
      print(x)
      try: x = str(re.search(r'\[\[.*?\[(.*?)\].*?\]\]', x).group(1)).split(", ")
      except: 
            #print("faild to find [[[command]]], lowering confedence")
            try: x = str(re.findall(r'\[(?![^\[\]]*\[)([^\[\]]+)\]', x)[-1]).split(", ")
            except: pass #print("faild to find [command], AT LOW CONDFEDENCE")

      if type(x) == list: x = [item for item in x if item != "None"]
      print(x)
      if type(x) == list: return x
      else: return "No command found"

def personality(question):
      x = llm_Grain(
            PROMPT_GRAIN.format(Day_Of_Week= datetime.datetime.now().strftime("%A"), Date= datetime.datetime.now().strftime("%m/%d/%Y"), Time= datetime.datetime.now().strftime("%H:%M:%S"), User_Input= question),
            #temperature=0.3
            max_tokens=400,
            stop= ["<|im_end|>", "|</assistant|>", "<|end_of_text|>"],
      )["choices"][0]["text"]
      print(x)
      return x


def listen():
      p = pyaudio.PyAudio()
      mic_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
      wake_up = Model(wakeword_models=["./sounds/grain.onnx"])

      def transcribe():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                  print("Say something!")
                  audio = r.listen(source)
                  text = r.recognize_whisper(audio, language="english")
                  print(text)
                  return text

      while True:
            prediction = wake_up.predict(np.frombuffer(mic_stream.read(1, exception_on_overflow= False), dtype=np.uint16))
            confedence = prediction["grain"]*100000
            confedence = round(confedence, 3)
            sys.stdout.write(f"\r{str(confedence)}")
            sys.stdout.flush()
            #Threshold
            if confedence >= 1000:
                  pyvolume.custom(percent=0)
                  print()
                  request = transcribe()
                  pyvolume.custom(percent=HOLDOVER["volume"])
                  hold()
                  response = nlp(question=request)
                  action(response)
                  wake_up.reset()


def action(command):
      if type(command) != list: 
            print("Not a list")
            return "Not a list"

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
                  print(booking(command[2], datetime.datetime.strptime(f"{command[3]} {command[4]}", "%Y-%m-%d %H:%M"), datetime.datetime.strptime(f"{command[3]} {command[5]}", "%Y-%m-%d %H:%M")))
                  event = booking(command[2], datetime.datetime.strptime(f"{command[3]} {command[4]}", "%Y-%m-%d %H:%M"), datetime.datetime.strptime(f"{command[3]} {command[5]}", "%Y-%m-%d %H:%M"))
                  print(event)
                  cal.schedule(event)
      
      if command[0] == "Email":
            if command[1] == "Today":
                  print(postman.emails_today())
            if command[1] == "Unread":
                  print(postman.unread())
      print("")
         
def speak(lines):
      if lines != "":
            mouth.inference(lines, output_wav_file="voice_lines.wav")
            def clv_play(file_path):
                  vlc_instance = vlc.Instance()
                  player = vlc_instance.media_player_new()
                  media = vlc_instance.media_new(file_path)
                  player.set_media(media)
                  player.play()
                  time.sleep(0.2)
                  duration = player.get_length()/1000
                  time.sleep(duration)
            threading.Thread(target=clv_play, args=("./voice_lines.wav",), daemon=True).start()

core = threading.Thread(target=listen, daemon=True)
core.start()


while True:
      time.sleep(1)


#CMAKE_ARGS="-DGGML_METAL=on" pip install --force-reinstall --upgrade --no-cache-dir  -v "llama_cpp_python==0.2.83"    
