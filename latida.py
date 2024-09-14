from llama_cpp import Llama
import re
import datetime
from Prompt import *
PATH_TO_NLP_MODEL = "./models/Meta-Llama-3.1-8B-Instruct-Q4_K_L.gguf"
llm_nlp = Llama(model_path=PATH_TO_NLP_MODEL, n_gpu_layers=-1)

print(PROMPT_INSTRUCTION)

exit()
def nlp(question):
      x = llm_nlp(
            PROMPT_INSTRUCTION.format(Day_Of_Week= datetime.datetime.now().strftime("%A"), Date= datetime.datetime.now().strftime("%m/%d/%Y"), Time =datetime.datetime.now().strftime("%H:%M:%S"), Tomorrow= datetime.datetime.now().strftime("%Y-%m-%d"), User_Input= question),
            max_tokens=400,
            seed=420,
            echo=False,
            stop= ["<|end|>", "|</assistant|>", "<|end_of_text|>"],
      )#["choices"][0]["text"]
      print(x)

nlp("what time is it?")