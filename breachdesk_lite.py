import logging as LOG

LOG.basicConfig(level=LOG.INFO)

APP_NAME = "BreachDesk Lite"

LOG.info("%s started", APP_NAME)
print(f"{APP_NAME} is starting ...")


def show_scenario(scenario):
    '''Display a security scenario in a readable format'''
    print(f"Scenario: {scenario['title']}")
    print(f"Severity: {scenario['severity']}")
    print(f"Summary: {scenario['summary']}")
    LOG.info("Scenario displayed: %s", scenario["title"])

def show_choices(choices):
    '''Display response choices in a numbered list'''
    for number, choice in enumerate(choices, start=1):
        print(f"{number}. {choice['label']}")

def parse_choice_number(player_input):
    '''Convert player input into a choice number, or return None'''
    try:
        return int(player_input)
    except ValueError as e:
        #LOG.error("ValueError: %s", e)
        LOG.warning("Invalid non-numeric choice entered: %s", player_input)
        return None

def get_choice_by_number(choices, choice_number):
    '''Return the choice that matches a player's numeric selection.
    Given a valid number, returns the choice that number points to.'''
    index = choice_number - 1
    if index < 0 or index >= len(choices):
        return None
    return choices[index]

def check_choice(choice):
    '''Return a decision result for the selected choice'''
    if choice == "rotate_key":
        return "Good Choice"
    else:
        return "Risky Choice"

def clamp_score(score):
    '''Helper function to keep a score between 0 and 100'''
    return max(0, min(100, score))

def apply_choice(choice, trust, health, threat):
    '''Apply a choice's score changes and returns updated scores'''
    new_trust = clamp_score(trust + choice["trust_delta"])
    new_health = clamp_score(health + choice["health_delta"])
    new_threat = clamp_score(threat + choice["threat_delta"])

    return new_trust, new_health, new_threat




print()

#Scenario data used for the first app exercise
scenario = {
    "title": "A customer key might be stolen",
    "severity": "High",
    "summary": "A customer API key is being used from two countries"
}

choices = [
    {
        "id": "ignore",
        "label": "Do nothing for now",
        "is_correct": False,
        "trust_delta": -12,
        "health_delta": 0,
        "threat_delta": 18   
    },
    {
        "id": "rotate_key",
        "label": "Replace the key and alert the customer",
        "is_correct": True,
        "trust_delta": 8,
        "health_delta": -2,
        "threat_delta": -16
    },
    {
        "id": "delete_account",
        "label": "Delete the customer account",
        "is_correct": False,
        "trust_delta": -18,
        "health_delta": -8,
        "threat_delta": -6   
    }
]
#Tradeoffs:
#Ignore: trust drops, threat rises
#Rotate key: trust rises, health slightly drops, threat drops
#Delete account: threat drops somewhat, but trust and health drop badly

# Starting scores
trust = 82
health = 91
threat = 38

# Assertion tests
assert check_choice("rotate_key") == "Good Choice"
assert check_choice("ignore") == "Risky Choice"

assert clamp_score(-10) == 0
assert clamp_score(0) == 0
assert clamp_score(50) == 50
assert clamp_score(100) == 100
assert clamp_score(120) == 100

assert parse_choice_number("2") == 2
assert parse_choice_number("  2  ") == 2
assert parse_choice_number("hello") is None
assert parse_choice_number("") is None

test_choice = {
    "trust_delta": 8,
    "health_delta": -2,
    "threat_delta": -16,
}

assert apply_choice(test_choice, 82, 91, 38) == (90, 89, 22)
assert apply_choice(test_choice, 98, 91, 38) == (100, 89, 22)

assert get_choice_by_number(choices, 1)["id"] == "ignore"
assert get_choice_by_number(choices, 2)["id"] == "rotate_key"
assert get_choice_by_number(choices, 0) is None
assert get_choice_by_number(choices, 99) is None
assert get_choice_by_number(choices, -1) is None

# Gameplay flow starts here
show_scenario(scenario)

print()
print("Choices:")
show_choices(choices)

selected_choice = None

while selected_choice is None:
    player_input = input("Choose an option number: ").strip()
    choice_number = parse_choice_number(player_input)

    if choice_number is not None:
        selected_choice = get_choice_by_number(choices, choice_number)
  
    if selected_choice is None:
        LOG.warning("Invalid choice entered: %s", player_input)
        print("Invalid choice. Please run the program again and enter one of the listed choice numbers.")

print()
print("Starting scores:")
print(f"Trust: {trust}")
print(f"Health: {health}")
print(f"Threat: {threat}")

print()
print(f"Selected choice: {selected_choice['label']}")
LOG.info("Selected choice: %s", selected_choice["id"])

trust, health, threat = apply_choice(selected_choice, trust, health, threat)

print()
print("Updated scores:")
print(f"Trust: {trust}")
print(f"Health: {health}")
print(f"Threat: {threat}")

LOG.info(
    "Scores updated: Trust = %s, Health = %s, Threat = %s",
    trust,
    health,
    threat
)

print()
result = check_choice(selected_choice["id"])
print(result)






