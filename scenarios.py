'''Scenario loading and validation helpers for BreachDesk Lite.'''

import json

from exceptions import ScenarioDataError
from models import Scenario


def load_scenarios(file_path="scenarios_data.json"):
    '''Load, validate, and convert scenario data from a JSON file'''
    with open(file_path, "r", encoding="utf-8") as file:
        scenario_data = json.load(file)

    if not isinstance(scenario_data, list):
        raise ScenarioDataError("Scenario data must be a list")
    
    scenarios = []

    for scenario in scenario_data:
        validate_scenario(scenario)
        scenarios.append(Scenario.from_dict(scenario))
    
    return scenarios


def validate_scenario(scenario):
    '''Validate that a scenario has the required structure'''
    required_fields = ["title", "severity", "summary", "choices"]

    for field in required_fields:
        if field not in scenario:
            raise ScenarioDataError(f"Scenario is missing required field: {field}")

    if not isinstance(scenario["choices"], list):
        raise ScenarioDataError("Scenario choices must be a list")

    if len(scenario["choices"]) == 0:
        raise ScenarioDataError("Scenario must include at least one choice")

    for choice in scenario["choices"]:
        validate_choice(choice)


def validate_choice(choice):
    '''Validate that a choice has the required structure'''
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
            raise ScenarioDataError(f"Choice is missing required field: {field}")
    