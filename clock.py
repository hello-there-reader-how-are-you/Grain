import datetime
from num2words import num2words
import time
import vlc
import threading
ALARM_SOUND = "alarm_bells.mp3"

class clock:
    #clock
    def now():
        return datetime.datetime.now()
    def time():
        return datetime.datetime.now().strftime("%I:%M:%S %p")
    def time_pretty():
        return f"{num2words(datetime.datetime.now().strftime("%I"))} {num2words(datetime.datetime.now().strftime("%M"))} {datetime.datetime.now().strftime("%p")} "
    def time_military():
        return datetime.datetime.now().strftime("%H:%M%S")
    def day():
        return datetime.datetime.now().today()
    def date():
        return datetime.datetime.now().strftime("%m/%d/%Y")
    def date_words():
        day = datetime.datetime.now().strftime("%d")
        if datetime.datetime.now().strftime("%d"[0]) == "0":
            day = datetime.datetime.now().strftime("%d"[1])
        return f"{datetime.datetime.now().strftime("%A")} the {num2words(day, "ordinal_num")} of {datetime.datetime.now().strftime("%B")} the year of our lord {num2words(datetime.datetime.now().strftime("%C"))} {num2words(datetime.datetime.now().strftime("%y"))}"

    #timer
    def timer(wait):
        #accepts seconds
        #datetime.datetime.now() + datetime.timedelta(seconds=wait)
        def play_alarm_sound(wait):
            time.sleep(wait)
            vlc_instance = vlc.Instance()
            player = vlc_instance.media_player_new()
            media = vlc_instance.media_new(ALARM_SOUND)
            player.set_media(media)
            player.audio_set_volume(500)
            player.play()
            time.sleep(0.2)
            duration = player.get_length()/1000
            time.sleep(duration)
        threading.Thread(target=play_alarm_sound(wait), daemon=True).start()





x = clock


print(x.timer(5))


