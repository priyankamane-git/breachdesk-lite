'''Assertion tests for Breachdesk Lite'''

import logging as LOG

from input_utils import get_choice_by_number, parse_choice_number
from scoring import apply_choice, check_choice, clamp_score, get_final_grade

LOG.basicConfig(level=LOG.INFO)

# These checks run before gameplay starts, so obvious logic bugs fail early
def run_assertion_tests():
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
    test_choices = [
        {"id": "first"},
        {"id": "second"}
    ]

    assert get_choice_by_number(test_choices, 1)["id"] == "first"
    assert get_choice_by_number(test_choices, 2)["id"] == "second"
    assert get_choice_by_number(test_choices, 0) is None
    assert get_choice_by_number(test_choices, 99) is None
    assert get_choice_by_number(test_choices, -1) is None


def test_get_final_grade():
    '''Test final grade outcomes'''
    assert get_final_grade(90, 80, 20) == "Strong Incident Response"
    assert get_final_grade(65, 55, 50) == "Needs More Triage"
    assert get_final_grade(40, 45, 80) == "High Risk Outcome"
