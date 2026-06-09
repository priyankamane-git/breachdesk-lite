'''Unit tests for BreachDesk Lite.'''

import unittest

from models import Choice, Scenario
from input_utils import get_choice_by_number, parse_choice_number
from scoring import apply_choice, check_choice, clamp_score, get_final_grade
from scenarios import load_scenarios, validate_scenario, validate_choice


class TestScoring(unittest.TestCase):
    '''Tests for scoring and outcome helpers'''

    # check_choice() should return feedback based on the choice's correctness flag
    def test_choice_for_correct_choice(self):
        '''Test choice feedback based on correctness'''
        choice = Choice(
            choice_id="test_choice",
            label="Test choice",
            is_correct=True,
            trust_delta=0,
            health_delta=0,
            threat_delta=0
        )
        result = check_choice(choice)

        self.assertEqual(result, "Good Choice")
    
    def test_choice_for_wrong_choice(self):
        choice = Choice(
            choice_id="test_choice",
            label="Test choice",
            is_correct=False,
            trust_delta=0,
            health_delta=0,
            threat_delta=0
        )
        result = check_choice(choice)

        self.assertEqual(result, "Risky Choice")


    # clamp_score() should keep scores inside the 0 to 100 range
    def test_clamp_score_keeps_score_in_range(self):
        '''Test score boundaries'''
        
        self.assertEqual(clamp_score(-10), 0)
        self.assertEqual(clamp_score(0), 0)
        self.assertEqual(clamp_score(50), 50)
        self.assertEqual(clamp_score(100), 100)
        self.assertEqual(clamp_score(200), 100)


    # apply_choice() should apply score deltas and clamp scores when needed
    def test_apply_choice_updates_scores(self):
        '''Test score updates after applying a player's choice'''
        choice = Choice(
                choice_id="test_choice",
                label="Test choice",
                is_correct=True,
                trust_delta=8,
                health_delta=-2,
                threat_delta=-16,
            )

        result = apply_choice(choice, 82, 91, 38)

        self.assertEqual(result, (90, 89, 22))

    def test_apply_choice_with_clamped_scores(self):
        choice = Choice(
                choice_id="test_choice",
                label="Test choice",
                is_correct=True,
                trust_delta=8,
                health_delta=-2,
                threat_delta=-16,
            )
        result = apply_choice(choice, 98, 91, 38)
        
        self.assertEqual(result, (100, 89, 22))
    

    #Test final grade outcomes
    def test_get_final_grade_returns_strong_response(self):
        result = get_final_grade(90, 80, 20)

        self.assertEqual(result, "Strong Incident Response")

    def test_get_final_grade_returns_needs_more_triage(self):
        result = get_final_grade(65, 55, 50)

        self.assertEqual(result, "Needs More Triage")

    def test_get_final_grade_returns_high_risk(self):
        result = get_final_grade(40, 45, 80)

        self.assertEqual(result, "High Risk Outcome")
        

class TestInputUtils(unittest.TestCase):
    '''Test for input parsing and choice lookup helpers'''
    
    # parse_choice_number() should convert numeric text and reject non-numeric text
    def test_parse_choice_number_input_integer(self):
        result = parse_choice_number("2")

        self.assertEqual(result, 2)
        
    def test_parse_choice_number_input_integer_with_spaces(self):
        result = parse_choice_number("  2  ")

        self.assertEqual(result, 2)

    def test_parse_choice_number_input_alphabets(self):
        result = parse_choice_number("hello")

        self.assertIsNone(result)

    def test_parse_choice_number_input_empty_string(self):
        result = parse_choice_number("")

        self.assertIsNone(result)


    def test_get_choice_by_number_for_matching_choice(self):
        '''Test the mapping of numeric selections to scenario choices'''
        # get_choice_by_number() should map display numbers to list items
        choices = [
            Choice("first", "First", True, 0, 0, 0),
            Choice("second", "Second", False, 0, 0, 0),
        ]
        result = get_choice_by_number(choices, 2)

        self.assertEqual(result.id, "second")

    def test_get_choice_by_number_for_choice_zero(self):
        choices = [
        Choice("first", "First", True, 0, 0, 0),
        Choice("second", "Second", False, 0, 0, 0),
        ]
        result = get_choice_by_number(choices, 0)

        self.assertIsNone(result)

    def test_get_choice_by_number_for_choice_out_of_range(self):
        choices = [
            Choice("first", "First", True, 0, 0, 0),
            Choice("second", "Second", False, 0, 0, 0),
        ]
        result = get_choice_by_number(choices, 99)

        self.assertIsNone(result)

    def test_get_choice_by_number_for_choice_negative_number(self):
        choices = [
            Choice("first", "First", True, 0, 0, 0),
            Choice("second", "Second", False, 0, 0, 0),
        ]
        result = get_choice_by_number(choices, -1)

        self.assertIsNone(result)


class TestChoiceModel(unittest.TestCase):
    '''Tests for the Choice domain model'''

    def test_choice_stores_attributes(self):
        choice = Choice(
            choice_id="test_choice",
            label="Test Choice",
            is_correct=True,
            trust_delta=1,
            health_delta=0,
            threat_delta=-1
        )

        self.assertEqual(choice.id, "test_choice")
        self.assertEqual(choice.label, "Test Choice")
        self.assertTrue(choice.is_correct)
        self.assertEqual(choice.trust_delta, 1)
        self.assertEqual(choice.health_delta, 0)
        self.assertEqual(choice.threat_delta, -1)

    def test_choice_from_dict_creates_choice(self):
        data = {
            "id": "test_choice",
            "label": "Test choice",
            "is_correct": True,
            "trust_delta": 1,
            "health_delta": 0,
            "threat_delta": -1
        }

        choice = Choice.from_dict(data)

        self.assertIsInstance(choice, Choice)
        self.assertEqual(choice.id, "test_choice")
        self.assertEqual(choice.trust_delta, 1)


class TestScenarioModel(unittest.TestCase):
    '''Tests for the Scenario domain model'''

    def test_scenario_stores_attributes(self):
        choices = [
            Choice(
                choice_id="test_choice",
                label="Test choice",
                is_correct=True,
                trust_delta=1,
                health_delta=0,
                threat_delta=-1,
            )
        ]

        scenario = Scenario(
            title="Test Title",
            severity="Low",
            summary="Test Summary",
            choices=choices
        )
        
        self.assertEqual(scenario.title, "Test Title")
        self.assertEqual(scenario.severity, "Low")
        self.assertEqual(scenario.summary, "Test Summary")
        self.assertEqual(scenario.choices, choices)

    def test_scenario_from_dict_creates_scenario(self):
        data = {
            "title": "Test Title",
            "severity": "Low",
            "summary": "Test Summary",
            "choices": [
                {
                    "id": "test_choice",
                    "label": "Test choice",
                    "is_correct": True,
                    "trust_delta": 1,
                    "health_delta": 0,
                    "threat_delta": -1
                }
            ]
        }

        scenario = Scenario.from_dict(data)

        self.assertEqual(scenario.title, "Test Title")
        self.assertEqual(scenario.severity, "Low")
        self.assertEqual(scenario.summary, "Test Summary")
        self.assertIsInstance(scenario.choices[0], Choice)
        self.assertEqual(scenario.choices[0].id, "test_choice")


class TestScenariosLoading(unittest.TestCase):
    '''Tests for loading scenarios JSON data'''
    def test_load_scenarios_returns_list(self):
        scenarios = load_scenarios()

        self.assertIsInstance(scenarios, list)

    def test_load_scenarios_includes_choices(self):
        scenarios = load_scenarios()

        self.assertIsInstance(scenarios[0].choices[0], Choice)
        self.assertIsInstance(scenarios[0], Scenario)


class TestScenarioValidation(unittest.TestCase):
    '''Tests for scenario data validation'''

    def test_validate_scenario_accepts_valid_data(self):
        scenario = {
            "title": "Test Scenario",
            "severity": "Low",
            "summary": "Test Summary",
            "choices": [
                {
                    "id": "test_choice",
                    "label": "Test Choice",
                    "is_correct": True,
                    "trust_delta": 1,
                    "health_delta": 0,
                    "threat_delta": -1
                }
            ]
        }
        validate_scenario(scenario)

    def test_validate_scenario_rejects_missing_title(self):
        scenario = {
            "severity": "Low",
            "summary": "Test Summary",
            "choices": []
        }

        with self.assertRaises(ValueError):
            validate_scenario(scenario)

    def test_validate_choice_rejects_missing_id(self):
        choice = {
            "label": "Test Choice",
            "is_correct": True,
            "trust_delta": 1,
            "health_delta": 0,
            "threat_delta": -1
        }

        with self.assertRaises(ValueError):
            validate_choice(choice)


if __name__ == "__main__":
    unittest.main()