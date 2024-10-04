from llama_cpp import Llama
import time
from NA.testing_prompt import *
#alt is best version with corrections

#--override-kv tokenizer.ggml.pre=str:tekken
llm = Llama("./models/Meta-Llama-3.1-8B-Instruct-Q4_K_L.gguf", n_gpu_layers=-1)

print("\n\n\n")
def ask(question):
      x = llm(
            BROMPT_GRAIN.format(question),
            #temperature=0.3
            max_tokens=400,
            seed=420,
            stop=["<|end|>", "<|im_end|>"],
      )["choices"][0]["text"]
      return x

print(ask("Please turn my AC on"))
