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
    if choice["is_correct"]:
        return "Good Choice"
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

def get_final_grade(trust, health, threat):
    '''Return a final grade based on ending scores'''
    if trust>=80 and health>=70 and threat<=30:
        return "Strong Incident Response"
    if trust>=60 and health>=50 and threat<=60:
        return "Needs More Triage"
    return "High Risk Outcome"

# Assertion tests
# These checks run before gameplay starts, so obvious logic bugs fail early
def run_asseertion_tests():
    '''Run basic assertion tests before gameplay starts'''
    test_check_choice()
    test_clamp_score()
    test_parse_choice_number()
    test_apply_choice()
    test_get_choice_by_number()
    test_get_final_grade()
    LOG.info("All assertion tests passed")

def test_check_choice():
    '''Test choice feedback based on correctness'''
    # check_choice() should return feedback based on the choice's correctness flag
    assert check_choice({"is_correct": True}) == "Good Choice"
    assert check_choice({"is_correct": False}) == "Risky Choice"

def test_clamp_score():
    '''Test score boundaries'''
    # clamp_score() should keep scores inside the 0 to 100 range
    assert clamp_score(-10) == 0
    assert clamp_score(0) == 0
    assert clamp_score(50) == 50
    assert clamp_score(100) == 100
    assert clamp_score(120) == 100

def test_parse_choice_number():
    '''Test parsing of player's input'''
    # parse_choice_number() should convert numeric text and reject non-numeric text
    assert parse_choice_number("2") == 2
    assert parse_choice_number("  2  ") == 2
    assert parse_choice_number("hello") is None
    assert parse_choice_number("") is None

def test_apply_choice():
    '''Test score updates after applying a player's choice'''
    # apply_choice() should apply score deltas and clamp scores when needed
    test_choice = {
        "trust_delta": 8,
        "health_delta": -2,
        "threat_delta": -16,
    }

    assert apply_choice(test_choice, 82, 91, 38) == (90, 89, 22)
    assert apply_choice(test_choice, 98, 91, 38) == (100, 89, 22)

def test_get_choice_by_number():
    '''Test the mapping of numeric selections to scenario choices'''
    # get_choice_by_number() should map display numbers to list items
    test_choices = scenarios[0]["choices"]

    assert get_choice_by_number(test_choices, 1)["id"] == "ignore"
    assert get_choice_by_number(test_choices, 2)["id"] == "rotate_key"
    assert get_choice_by_number(test_choices, 0) is None
    assert get_choice_by_number(test_choices, 99) is None
    assert get_choice_by_number(test_choices, -1) is None

def test_get_final_grade():
    '''Test final grade outcomes'''
    assert get_final_grade(90, 80, 20) == "Strong Incident Response"
    assert get_final_grade(65, 55, 50) == "Needs More Triage"
    assert get_final_grade(40, 45, 80) == "High Risk Outcome"
    

print()

#Choices Tradeoffs examples:
#1. Ignore: trust drops, threat rises
#2. Rotate key: trust rises, health slightly drops, threat drops
#3. Delete account: threat drops somewhat, but trust and health drop badly

# Scenario data is stored as a list so the game can run multiple rounds.
# Each scenario owns its own choices, which keeps the prompt and responses together.
scenarios = [
    {
        "title": "A customer key might be stolen",
        "severity": "High",
        "summary": "A customer API key is being used from two countries",
        "choices": [
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
    },
    {
        "title": "Webhook retries are flooding the system",
        "severity": "Medium",
        "summary": "A partner webhook is sending the same failed payment event repeatedly",
        "choices": [
            {
                "id": "ignore",
                "label": "Ignore it because retries are normal",
                "is_correct": False,
                "trust_delta": -6,
                "health_delta": -10,
                "threat_delta": 8
            },
            {
                "id": "deduplicate",
                "label": "Deduplicate events and investigate the retry source",
                "is_correct": True,
                "trust_delta": 7,
                "health_delta": 8,
                "threat_delta": -10
            },
            {
                "id": "block_partner",
                "label": "Block the partner integration immediately",
                "is_correct": False,
                "trust_delta": -10,
                "health_delta": 4,
                "threat_delta": -4
            }
        ]
    }
]

# Starting scores
trust = 82
health = 91
threat = 38

run_asseertion_tests()

# Gameplay flow starts here
for scenario in scenarios:
    show_scenario(scenario)

    print()
    print("Choices:")
    choices = scenario["choices"]
    show_choices(choices)

    selected_choice = None

    while selected_choice is None:
        #If the failure path is small and the success path is large,
        #try to handle failure first, then let success path continue normally.
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
    result = check_choice(selected_choice)
    print(result)

    print()
    print("-"*40)

print()
print("Final Summary")
print(f"Trust: {trust}")
print(f"Health: {health}")
print(f"Threat: {threat}")

final_grade = get_final_grade(trust, health, threat)
print(f"Grade: {final_grade}")

LOG.info("Final grade: %s", final_grade)


