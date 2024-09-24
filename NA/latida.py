from llama_cpp import Llama
import re
import datetime
from Prompt import *

PATH_TO_NLP_MODEL = "./models/gemma-2-2b-it-abliterated-Q2_K_L.gguf"
llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_gpu_layers=-1, n_ctx=2048)



def nlp(question):
      x = llm_nlp(
            PROMPT_INSTRUCTION.replace("REPLACE_ME_WITH_USER_INPUT", question),
            max_tokens=400,
            seed=420,
            echo=False,
            stop= ["<|end|>", "|</assistant|>", "<|end_of_text|>"],
      )["choices"][0]["text"]
      print(x)

print("\n\n\n")
nlp("play radio gaga by queen")
nlp("what time is it?")
nlp("what in my email")
nlp("Grain, who are you?")