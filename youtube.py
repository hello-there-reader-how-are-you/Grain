from youtube_search import YoutubeSearch
import vlc
import time
import os
import yt_dlp
import threading
import sys

#Where does the video file go? It dissapears...

# Python program raising
# exceptions in a python
# thread

import ctypes



class yt:
    def __init__(self, search_term=None, is_paused=False):
        self.file_title = "yt_vid"
        self.format = "m4a"
        self.savepath = "./"
        self.Full_Name = f"{self.savepath}{self.file_title}.{self.format}"

        self.is_paused = is_paused
        self.kill_flag = False
        self.search_term = search_term

        ydl_opts = {
            'outtmpl': self.file_title,
            'format': f'{self.format}/bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': f'{self.format}',
            }]
        }
        self.ydl = yt_dlp.YoutubeDL(ydl_opts)

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.disc = threading.Thread(target=self.core, daemon=True)
        self.disc.start()

    
    def clear(self):
        self.kill_flag = True
        self.disc.join()
        print("clear????")

    def change_song(self, search_term=None):
        self.search_term = search_term
        self.clear()
    
    def set_search_term(self, search_term):
        self.search_term = search_term
    def wait_for_search_term(self):
        while self.search_term == None:
            time.sleep(0.1)
    
    def play(self):
        if self.search_term == None: return
        self.is_paused = False
        self.player.play()
    def pause(self):
        if self.search_term == None: return
        self.is_paused = True
        self.player.pause()


    def core(self):
        self.wait_for_search_term()

        try: os.remove(self.Full_Name)
        except: pass
        print(self.search_term)
        self.ydl.download(f"https://youtube.com{YoutubeSearch(self.search_term, max_results=1).to_dict()[0]["url_suffix"]}")


        self.media = self.vlc_instance.media_new(self.Full_Name)
        self.player.set_media(self.media)

        self.player.play()
        length = self.player.get_length()/1000

        time.sleep(0.2)

        tick = 0

        while tick <= length:
            if self.kill_flag == True:
                self.kill_flag = False
                sys.exit(1)
            if self.is_paused == True:
                time.sleep(0.1)
            else:
                time.sleep(0.1)
                tick +=1
        os.remove(self.Full_Name)


jukebox = yt("radio gaga")
time.sleep(15)
jukebox.clear()
jukebox.play()
time.sleep(100)


"""
jukebox = yt("radio gaga")
time.sleep(15)
jukebox.pause()
input("continue?:")
jukebox.play()

time.sleep(100)
print("done")
"""




