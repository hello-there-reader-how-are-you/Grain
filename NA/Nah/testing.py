from youtube_search import YoutubeSearch
from pytube import YouTube 
import vlc
import time
import os
#https://stackoverflow.com/questions/40713268/download-youtube-video-using-python-to-a-certain-directory
SAVE_PATH = "./"
#https://youtube.com/watch?v=W8r-tXRLazs&pp=ygUbdmlkZW8ga2lsbGVkIHRoZSByYWRpbyBzdGFy
print(YouTube(f"https://youtube.com{YoutubeSearch("video killed the radio star", max_results=1).to_dict()[0]["url_suffix"]}"))

print(YouTube("/watch?v=W8r-tXRLazs&pp=ygUbdmlkZW8ga2lsbGVkIHRoZSByYWRpbyBzdGFy"))


exit()
YouTube(f"https://youtube.com{YoutubeSearch("video killed the radio star", max_results=1).to_dict()[0]["url_suffix"]}").streams.filter(file_extension='mp4').all()[-1].download(output_path=SAVE_PATH)





