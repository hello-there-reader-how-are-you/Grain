from youtube_search import YoutubeSearch
import vlc
import time
import os
import yt_dlp
import threading



NAME = "yt_vid"
FORMAT = "m4a"
SAVE_PATH = "./"
FULL_NAME = f"{SAVE_PATH}{NAME}.{FORMAT}"
ydl_opts = {
    'outtmpl': NAME,
    'format': f'{FORMAT}/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': f'{FORMAT}',
    }]
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

def yt_dl_url(url):
    ydl.download(url)

def yt_dl(search_term):
    try: os.remove(FULL_NAME)
    except: pass
    ydl.download(f"https://youtube.com{YoutubeSearch(search_term, max_results=1).to_dict()[0]["url_suffix"]}")
    return f"{SAVE_PATH}{NAME}.{FORMAT}"



def yt_play(search_term):
    source = yt_dl(search_term)
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(source)
    player.set_media(media)
    player.play()
    time.sleep(0.2)
    duration = player.get_length()/1000
    time.sleep(duration)
    os.remove(source)

yt_dl_url("https://www.youtube.com/watch?v=-kwVE0DFmSM")