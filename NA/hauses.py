import homeassistant_api
from homeassistant_api import Client
import json
import datetime

class Context:
    def __init__(self, id):
        self.id = id
    def __repr__(self):
        return f"Context(id={self.id!r})"
    
class UTC:
    def __init__(self):
        pass
    def __repr__(self):
        return "UTC()"

def TzInfo(UTC):
    return datetime.tzinfo('UTC')

class State:
    def __init__(self, entity_id, state, attributes, last_changed, last_updated, context):
        self.entity_id=entity_id
        self.state=state,
        self.attributes = attributes
        self.last_changed=last_changed
        self.last_updated=last_updated
        self.context=context

    def __repr__(self):
        return (f"State(entity_id={self.entity_id!r}, state={self.state!r}, "
                f"attributes={self.attributes!r}, last_changed={self.last_changed!r}, "
                f"last_updated={self.last_updated!r}, context={self.context!r})")

class Entity:
    def __init__(self, slug, state):
        self.slug=slug
        self.state=state

    def __repr__(self):
        return f"Entity(slug={self.slug!r}, state={self.state!r})"

with open('./ignore_me/HA.json', 'r') as file:
    data = json.load(file)

URL = data.get("API_Server_URL")
TOKEN = data.get("Long_Lived_Access_Token")

client = Client(URL, TOKEN)

accessible = ["Bedroom Overhead Lights", "Bedroom Lamp", "2nd Floor Bedrooms"]


Entities = list(client.get_entities().values())
for i in range(len(Entities)):
    Entities[i] = list(Entities[i].entities.values())

for i in range(len(Entities)):
    for j in range(len(Entities[i])):
        #print(repr(entity))
        Entities[i][j] = eval(repr(Entities[i][j]))

def flatten(xss):
    return [x for xs in xss for x in xs]

Entities = flatten(Entities)

for entity in Entities:
    if entity.state.attributes["friendly_name"] in accessible:
        print(entity.state.attributes["friendly_name"])
        pass #Entities.remove(entity)

#print(Entities)
