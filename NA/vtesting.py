import pyttsx3

engine = pyttsx3.init("espeak")
engine.say("I will speak this text")
engine.runAndWait()