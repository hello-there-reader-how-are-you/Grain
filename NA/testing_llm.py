from llama_cpp import Llama
import time
from testing_prompt import *
#alt is best version with corrections

#--override-kv tokenizer.ggml.pre=str:tekken
llm = Llama("./models/dolphin-2.9.3-mistral-nemo-12b.Q2_K.gguf", n_gpu_layers=-1)

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
