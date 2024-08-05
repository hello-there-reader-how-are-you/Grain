import vlc
import time
import os
import threading


file_name = "output.wav"
Full_Name = f"./bark_cpp/bark.cpp/{file_name}"


def clv_play(file_path):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(file_path)
    player.set_media(media)
    player.play()
    time.sleep(0.2)
    duration = player.get_length()/1000
    time.sleep(duration)
    #os.remove(file_path)

def speak(lines):
    os.system('cd ./bark_cpp/bark.cpp && ./build/examples/main/main -m ./models/bark-small/ggml_weights.bin -p "$(cat ../../voice_lines.txt)" -t 4 ; echo complete')
    disc = threading.Thread(target=clv_play, args=(Full_Name,), daemon=True)
    disc.start()



from llama_cpp import Llama
import time
from testing_prompt import *
#alt is best version with corrections

llm = Llama("./models/gemma-2-2b-it.q4_k_m.gguf", n_gpu_layers=-1)

print("\n\n\n")
def ask(question):
      x = llm(
            BROMPT_GRAIN.format(question),
            #temperature=0.3
            max_tokens=400,
            seed=420,
            stop=["<|end|>", "<|im_end|>"],
      )["choices"][0]["text"].replace('"', '').replace("'", "").replace("\n", "")
      print(x)
      with open('voice_lines.txt', 'w') as file:
          file.write(x)
      return x




speak(ask("can you write a paragraph summerizing the life of aberham lincon?"))

time.sleep(40)