import speech_recognition as sr
import openwakeword
from openwakeword.model import Model
import pyaudio
import numpy as np
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

model = Model(wakeword_models=["./sounds/grain.onnx"])


while True:
    prediction = model.predict(np.frombuffer(stream.read(1, exception_on_overflow= False), dtype=np.uint16))
    confedence = prediction["grain"]*100000
    print(confedence)
    if confedence >= 500:
        break

print("Awoke")


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)



try:
    print("Whisper thinks you said " + r.recognize_whisper(audio, language="english"))
except sr.UnknownValueError:
    print("Whisper could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Whisper; {e}")















"""

import openwakeword
from openwakeword.model import Model
import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=960)


# Instantiate the model(s)
model = Model(
    wakeword_models=["E:\Brian\Grain\sounds\grain.onnx"],  # can also leave this argument empty to load all of the included pre-trained models
)

# Get audio data containing 16-bit 16khz PCM audio data from a file, microphone, network stream, etc.
# For the best efficiency and latency, audio frames should be multiples of 80 ms, with longer frames
# increasing overall efficiency at the cost of detection latency
frame = stream.read(1)

prediction = model.predict(frame)
print(prediction)
"""
print("Finnished")
