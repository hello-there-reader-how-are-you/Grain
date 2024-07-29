from llama_cpp import Llama
import time
from testing_prompt import *



llm = Llama(model_path="./models/dolphin-2.9.3-mistral-nemo-Q5_K_M.gguf", n_gpu_layers=-1)

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
