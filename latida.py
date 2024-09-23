from llama_cpp import Llama
import re
import datetime
from Prompt import *

PATH_TO_NLP_MODEL = "./models/dolphin-2_6-phi-2.Q2_K.gguf"
llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL)



def nlp(question):
      x = llm_nlp(
            PROMPT_INSTRUCTION.replace("REPLACE_ME_WITH_USER_INPUT", question),
            max_tokens=400,
            seed=420,
            echo=False,
            stop= ["<|end|>", "|</assistant|>", "<|end_of_text|>"],
      )["choices"][0]["text"]
      print(x)

nlp("what time is it?")