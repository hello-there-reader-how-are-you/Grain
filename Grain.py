#Welcome

from modules.clock import *
from modules.youtube import *
from modules.calender import *
from modules.mail import *
from Prompt import *

import sys
import re
import time
import datetime
import threading
import numpy as np
import random
import json

from llama_cpp import Llama
from styletts2 import tts

import speech_recognition as sr
from openwakeword.model import Model
import noisereduce as nr

import pyaudio
import pyvolume

# Fix voice threshold

PATH_TO_NLP_MODEL = "./models/gemma-2-2b-it-abliterated-Q2_K_L.gguf"
#PATH_TO_NLP_MODEL = "./models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
#PATH_TO_NLP_MODEL = "./models/dolphin-2.9.3-mistral-nemo-12b.Q5_K_M.gguf"
PATH_TO_PERSONALITY_MODEL = PATH_TO_NLP_MODEL

SANDBOXING = True # Sandboxing creates a new thread for each action (I have not fixed the fact that some actions spawn threads. This means nested threading may be present [This is Bad])
GPU = True
NOISE_SUPP = True

MIN_CONFIDENCE = 700

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

if GPU:
      llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_gpu_layers=-1, n_ctx=2048)
else: 
      llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_ctx=2048)

print("\n\n\n")
llm_Grain = llm_nlp

#print("\n\n\n\n\n\n")

def nlp(question):
      x = llm_nlp(
            PROMPT_INSTRUCTION.replace(REPLACE_ME_WITH_USER_INPUT, question),
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
            PROMPT_INSTRUCTION.replace(REPLACE_ME_WITH_USER_INPUT, question),
            #temperature=0.3
            max_tokens=400,
            stop= ["<|im_end|>", "|</assistant|>", "<|end_of_text|>"],
      )["choices"][0]["text"]
      print(x)
      return x


def listen():
      p = pyaudio.PyAudio()
      mic_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
      wake_up = Model(wakeword_models=["./sounds/grain.onnx", "./sounds/Hey_Grain.onnx"], inference_framework="onnx")

      def transcribe():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                  print("Say something!")
                  audio = r.listen(source)
                  text = r.recognize_whisper(audio, language="english")
                  print(text)
                  return text

      while True:
            if NOISE_SUPP:
                  prediction = wake_up.predict(np.frombuffer(mic_stream.read(1, exception_on_overflow= False), dtype=np.uint16))
            else:
                  prediction = wake_up.predict(np.frombuffer(mic_stream.read(1, exception_on_overflow= False), dtype=np.uint16))
            confedence = (prediction["grain"]*100000) + (prediction["Hey_Grain"]*100000)
            confedence = round(confedence, 3)
            sys.stdout.write(f"\r{str(confedence)}")
            sys.stdout.flush()
            #TO BE FIXED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if confedence >= MIN_CONFIDENCE:
                  pyvolume.custom(percent=0)
                  print()
                  request = transcribe()
                  pyvolume.custom(percent=HOLDOVER["volume"])
                  hold()
                  response = nlp(question=request)
                  if SANDBOXING == True:
                        threading.Thread(target=action, args=(response,), daemon=True).start()
                  else:
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
