#https://huggingface.co/IlyaGusev/gemma-2-2b-it-abliterated

from llama_cpp import Llama
import re
import datetime
import sys
sys.path.append('.')
from Prompt import *

#PATH_TO_NLP_MODEL = "./models/gemma-2-2b-it-abliterated-Q2_K_L.gguf" the good one for raspi
PATH_TO_NLP_MODEL = "./models/dolphin-2.9.3-mistral-nemo-12b.Q5_K_M.gguf"
llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_gpu_layers=-1, n_ctx=2048)

training_prompt= f"""
Write 10 examlple echanges between a user and an ai assistant. Do not number the prompts. Use as much variety as you can, the goal is a diverse dataset.
Use this template:
User: USER_PROMPT
AI: AI_RESPONSE

Here is an example exchange:

User: play yellow submarine by the beatles
AI: [[[Music, Play, Yellow Submarine by the beatles]]]

User: Set an alarm for 5 58 p m.
AI: [[[Clock, Alarm, 17:58]]]

User: Do I have mail?
AI: [[[Email, Today]]]

The AI's system prompt is written below: 

Your name is Grain.
Grain is an AI smart assistant.
Grain's job is to format spoken commands into a computer readable format,
Today is Day_Of_Week, Date and the time is Time

Here is the mandatory format for all responses:
"[[[category, command, mandatory_fields, optional_fields]]]"

A list of all valid catagories and their commands are listed below.

{IS}

Be extremely careful! If a User's speech does not match any commands, respond: [[[[Not A Command]]].
"""


def ex():
      x = llm_nlp(
            training_prompt,
            
            max_tokens=1800,
            seed=420,
            temperature= 0.8,
            echo=False,
            stop= ["<|end|>", "|</assistant|>", "<|end_of_text|>"],
      )["choices"][0]["text"]
      print(x)
      return x



print("\n\n\n\n")

ex()