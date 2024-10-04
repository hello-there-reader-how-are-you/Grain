import homeassistant_api
from homeassistant_api import Client

import sys
sys.path.append('../ignore_me/')
from Home_Assistant import *

URL = API_Server_URL
TOKEN = Long_Lived_Access_Token


client = Client(URL, TOKEN)


def toggle_lights():
    #example function. Doesn't work
    light = client.get_domain("light")
    light.turn_on(entity_id="light.living_room_lamp")

