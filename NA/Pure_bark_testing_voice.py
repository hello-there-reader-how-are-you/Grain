from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

import vlc
import time
import os
import threading

#https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c&p=298639784299443090b6870cbcafde69&pm=s

#on macos must run: export SUNO_ENABLE_MPS=True
#check with echo $SUNO_ENABLE_MPS
#or:
#os.environ["SUNO_ENABLE_MPS"] = "True"
os.environ["SUNO_ENABLE_MPS"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"


file_name = "voice_lines.wav"
Full_Name = f"./{file_name}"

voice = "v2/en_speaker_6"



#preload_models()


def speak(lines):
     audio_array = generate_audio(lines, history_prompt=voice)
     write_wav(file_name, SAMPLE_RATE, audio_array)
     disc = threading.Thread(target=clv_play, args=(Full_Name,), daemon=True)
     disc.start()

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


from llama_cpp import Llama
import time
from NA.testing_prompt import *
#alt is best version with corrections

#--override-kv tokenizer.ggml.pre=str:tekken
llm = Llama("./models/dolphin-2.9.3-mistral-nemo-12b.Q5_K_M.gguf", n_gpu_layers=-1)

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

speak(ask("Please turn my AC on"))

time.sleep(1000)