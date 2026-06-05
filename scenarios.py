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
        scenarios = json.load(file)

    for scenario in scenarios:
        validate_scenario(scenario)
    
    return scenarios

def validate_scenario(scenario):
    '''Validate that the scenario has the required structure'''
    required_fields = ["title", "severity", "summary", "choices"]

    for field in required_fields:
        if field not in scenario:
            raise ValueError(f"Scenario is missing required field: {field}")

    if not isinstance(scenario["choices"], list):
        raise ValueError("Scenario choices must be a list")

    if len(scenario["choices"]) == 0:
        raise ValueError("Scenario must include at least one choice")

    for choice in scenario["choices"]:
        validate_choice(choice)

def validate_choice(choice):
    '''Validate that the choice has the required structure'''
    required_fields = [
        "id",
        "label",
        "is_correct",
        "trust_delta",
        "health_delta",
        "threat_delta"
    ]

    for field in required_fields:
        if field not in choice:
            raise ValueError(f"Choice is missing required field: {field}")

    