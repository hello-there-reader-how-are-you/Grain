from styletts2 import tts

my_tts = tts.StyleTTS2()

out = my_tts.inference("This is a test, I am testing. Look at me go! Wheatly", output_wav_file="test.wav",  target_voice_path= "yt_vid.m4a")
