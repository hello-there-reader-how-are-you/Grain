from llama_cpp import Llama
from clock import *
from youtube import *
from Prompt import PROMPT
import re
import time

jukebox = yt()

#speech = "Hey Grain, set a time for 5 seconds"
speech = "Hey Grain, play still alive from portal"
llm = Llama(model_path="./models/Phi-3-mini-4k-instruct-q4.gguf")
print("\n\n\n\n\n\n")

def ask(question):
      x = llm(
            PROMPT.format(question),
            max_tokens=200,
            seed=420,
            stop= ["<|end|>"],
      )["choices"][0]["text"]

      try: x = f"{re.search(r'\[\[.*?\[(.*?)\].*?\]\]', x).group(1)}".split(",")
      except: pass
      x = [item for item in output if item != " None"]
      return x

def action(act):
    if type(act) != list: return
    if act[0] == "Music":
      print("Music!")
      if act[1] == " Play":
            print("Play!")
            jukebox.set_search_term(''.join(act[2:]))
      if act[1] == " Pause" or " Stop":
            print("Pause!")
            jukebox.pause()



action(ask(question="Hey Grain, play still alive from portal"))
time.sleep(14)
output = ask(question="hey grain. Please pause my music")
print(output)
action(output)
time.sleep(10)
output = ask(question="hey grain. Please play my music")
print(output)
action(output)


time.sleep(10000000)