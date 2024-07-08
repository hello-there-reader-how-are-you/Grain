from youtube_search import YoutubeSearch
from pytube import YouTube 
import vlc
import time
import os

SAVE_PATH = "./"

def yt_dl(search_term):
    downloaded_file = YouTube(f"https://youtube.com{YoutubeSearch(search_term, max_results=1).to_dict()[0]["url_suffix"]}").streams.filter(file_extension='mp4').all()[-1].download(output_path=SAVE_PATH)
    return downloaded_file[downloaded_file.find('./') + 2:]



def yt_play(search_term):
    downloaded_file = YouTube(f"https://youtube.com{YoutubeSearch(search_term, max_results=1).to_dict()[0]["url_suffix"]}").streams.filter(file_extension='mp4').all()[-1].download(output_path=SAVE_PATH)
    source = downloaded_file[downloaded_file.find('./') + 2:]
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(source)
    player.set_media(media)
    player.play()
    time.sleep(0.2)
    duration = player.get_length()/1000
    time.sleep(duration)
    os.remove(source)

    
yt_play("video killed the radio star")
print("done")