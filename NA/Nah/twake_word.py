import openwakeword
from openwakeword.model import Model
import speech_recognition as sr

r = sr.Recognizer()



with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

