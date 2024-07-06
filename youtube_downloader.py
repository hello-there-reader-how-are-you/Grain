from youtube_search import YoutubeSearch
from pytube import YouTube 

SAVE_PATH = "./"

def yt_dl(search_term):
    YouTube(f"https://youtube.com{YoutubeSearch(search_term, max_results=1).to_dict()[0]["url_suffix"]}").streams.filter(file_extension='mp4').all()[-1].download(output_path=SAVE_PATH)


