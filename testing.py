from youtube_search import YoutubeSearch
from pytube import YouTube 
import vlc
import time
import io

flo = io.BinaryIO

def yt_dl(search_term):
    downloaded_file = YouTube(f"https://youtube.com{YoutubeSearch(search_term, max_results=1).to_dict()[0]["url_suffix"]}").streams.filter(file_extension='mp4').all()[-1].stream_to_buffer(flo)



def yt_play(source):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(source)
    player.set_media(media)
    player.play()
    time.sleep(0.2)
    duration = player.get_length()/1000
    print(duration)
    time.sleep(duration)
    
yt_dl("1min timer")
print("done")