import homeassistant_api
from homeassistant_api import Client
import json


with open('./ignore_me/HA.json', 'r') as file:
    data = json.load(file)
URL = data.get("API_Server_URL")
TOKEN = data.get("Long_Lived_Access_Token")
client = Client(URL, TOKEN)

#from hassapi import Hass
#HASS = Hass(hassurl=URL, token=TOKEN)
#HASS.turn_on("switch.bedroom_lamp")

accessible = ["Bedroom Overhead Lights", "Bedroom Lamp", "2nd Floor Bedrooms"]
Entities = [*client.get_states()]

i = 0
while i in range(len(Entities)):
    if Entities[i].attributes["friendly_name"] not in accessible:
        Entities.pop(i)
    else:
        i += 1

def trigger(name, action):
    name = str(name)
    action = str(action)
    #name example == "bedroom_lamp"
    for item in Entities:
        if item.entity_id.split('.')[1] == name:
            service = client.get_domain(item.entity_id.split('.')[0])
            actions = list(service.services.keys())
            if action in actions:
                getattr(service, action)(entity_id=item.entity_id)
                return client.get_state(entity_id=item.entity_id)
    else: return None

#print(Entities[2])

(trigger("bedroom_lamp", "toggle"))


"""
def lights():
    lights = []
    for item in Entities:
        if (item.entity_id.split('.')[0] == "light") or any(keyword in item.attributes["friendly_name"].lower() for keyword in ["light", "lamp"]):
            lights.append(item)
    return lights


            if (item.entity_id.split('.')[0] == "light"):
                client.trigger_service("light", item.entity_id)
                print("light")
            if (item.entity_id.split('.')[0] == "switch"):
                client.trigger_service("switch", item.entity_id)
                print("switch")



def toggle(ent):
    if ent.state == "on":
        return "off"
    if ent.state == "off":
        return "on"

service = client.get_domain(Entities[2].entity_id.split('.')[0])
print(service)
actions = list(service.services.keys())
print(actions)
service.toggle(entity_id=Entities[2].entity_id)



"""