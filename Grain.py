from llama_cpp import Llama
import re
import time
import datetime
from styletts2 import tts

from modules.clock import *
from modules.youtube import *
from Prompt import *
from modules.calender import *
from modules.mail import *

PATH_TO_NLP_MODEL = "models\Meta-Llama-3.1-8B-Instruct-Q4_K_L.gguf"
PATH_TO_PERSONALITY_MODEL = "models\Meta-Llama-3.1-8B-Instruct-Q4_K_L.gguf"

mouth = tts.StyleTTS2()
jukebox = yt()
watch = clock()
cal = calender()
postman = mailbox()

#speech = "Hey Grain, set a time for 5 seconds"
#speech = "Play radio gaga by queen"
llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_gpu_layers=-1)
#llm_Grain = llm_nlp
print("\n\n\n")
llm_Grain = Llama(model_path=PATH_TO_PERSONALITY_MODEL, n_gpu_layers=-1)

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

def personality(question):
      x = llm_Grain(
            PROMPT_GRAIN.format(question),
            #temperature=0.3
            max_tokens=400,
            stop= ["<|im_end|>"],
      )["choices"][0]["text"]
      print(x)
      return x

def speak(lines):
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

def ask(question):
      command = nlp(question)
      funny = personality(question)
      return [command, funny]



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
         

#text = input("Input: ")
text = "whats on my calender for later today?"
pln = ask(question=text)
action(pln[0])
speak(pln[1])



print
time.sleep(60)


#CMAKE_ARGS="-DGGML_METAL=on" pip install --force-reinstall --upgrade --no-cache-dir  -v "llama_cpp_python==0.2.83"    