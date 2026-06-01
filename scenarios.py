'''Helper that loads scenarios data for BreachDesk Lite.'''

import json

#Choices Tradeoffs examples:
#1. Ignore: trust drops, threat rises
#2. Rotate key: trust rises, health slightly drops, threat drops
#3. Delete account: threat drops somewhat, but trust and health drop badly

# Scenario data is stored as a list so the game can run multiple rounds.
# Each scenario owns its own choices, which keeps the prompt and responses together.

def load_scenarios(file_path="scenarios_data.json"):
    '''Load scenarios data from a JSON file'''
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)