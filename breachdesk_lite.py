import logging as LOG

from input_utils import get_choice_by_number, parse_choice_number
from scenarios import load_scenarios
from scoring import apply_choice, check_choice, clamp_score, get_final_grade

LOG.basicConfig(level=LOG.INFO)

APP_NAME = "BreachDesk Lite"
STARTING_TRUST = 82
STARTING_HEALTH = 91
STARTING_THREAT = 38


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


def main():
    '''Run the BreachDesk Lite command-line game.'''
    LOG.info("%s started", APP_NAME)
    print(f"{APP_NAME} is starting ...")

    # Starting scores
    trust = STARTING_TRUST
    health = STARTING_HEALTH
    threat = STARTING_THREAT

    scenarios = load_scenarios()

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


if __name__ == "__main__":
    main()

