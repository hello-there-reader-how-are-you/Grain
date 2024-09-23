import datetime
from num2words import num2words
import time
import vlc
import threading
ALARM_SOUND = "alarm_bells.mp3"

class clock:
    def __init__(self, volume=200):
        self.volume = volume

    #clock
    def now(self):
        return datetime.datetime.now()
    def time(self):
        return datetime.datetime.now().strftime('%I:%M:%S %p')
    def time_pretty(self):
        return f"{num2words(datetime.datetime.now().strftime('%I'))} {num2words(datetime.datetime.now().strftime('%M'))} {datetime.datetime.now().strftime('%p')}"
    def time_military(self):
        return datetime.datetime.now().strftime('%H:%M%S')
    def day(self):
        return datetime.datetime.now().today()
    def date(self):
        return datetime.datetime.now().strftime('%m/%d/%Y')
    def date_words(self):
        day = datetime.datetime.now().strftime('%d')
        if datetime.datetime.now().strftime('%d'[0]) == "0":
            day = datetime.datetime.now().strftime('%d'[1])
        return f"{datetime.datetime.now().strftime('%A')} the {num2words(day, 'ordinal_num')} of {datetime.datetime.now().strftime('%B')} the year of our lord {num2words(datetime.datetime.now().strftime('%C'))} {num2words(datetime.datetime.now().strftime('%y'))}"
    
    def play_alarm_sound(self):
        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(ALARM_SOUND)
        player.set_media(media)
        player.audio_set_volume(self.volume)
        player.play()
        time.sleep(0.2)
        duration = player.get_length()/1000
        time.sleep(duration)


    #timer
    def timer(self, wait, label="timer"):
        #accepts seconds (int)
        #datetime.datetime.now() + datetime.timedelta(seconds=wait)
        def funk_timer(wait):
            time.sleep(wait)
            self.play_alarm_sound()
        threading.Thread(target=funk_timer, args=(wait,), daemon=True).start()

    def alarm(self, trigger_time, label="alarm"):
        update_rate = 1
        #label does not work
        #expects format(millatry):   hour:minute        
        def funk_alarm(trigger_time):
            while True:
                if trigger_time.split(":")[0] == datetime.datetime.now().strftime("%H"):
                    if trigger_time.split(":")[1] == datetime.datetime.now().strftime("%M"):
                        self.play_alarm_sound()
                        return
                time.sleep(update_rate)
        threading.Thread(target=funk_alarm, args=(trigger_time,), daemon=True).start()




"""
x = clock
print(x.timer(5))

x=clock().alarm(datetime.datetime.now().strftime("%H:%M"))

clock().alarm("18:20")
clock().timer(5)
print("MEEE")
time.sleep(4000000)
"""

