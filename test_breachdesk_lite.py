'''Unit tests for BreachDesk Lite.'''

import unittest

from models import Choice, Scenario, GameSession
from input_utils import get_choice_by_number, parse_choice_number
from scoring import check_choice, clamp_score
from scenarios import load_scenarios, validate_scenario, validate_choice
from exceptions import ScenarioDataError


class TestScoring(unittest.TestCase):
    '''Tests for scoring and outcome helpers'''

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

    def test_clamp_score_keeps_score_in_range(self):
        '''Test score boundaries'''
        
        self.assertEqual(clamp_score(-10), 0)
        self.assertEqual(clamp_score(0), 0)
        self.assertEqual(clamp_score(50), 50)
        self.assertEqual(clamp_score(100), 100)
        self.assertEqual(clamp_score(200), 100)


class TestInputUtils(unittest.TestCase):
    '''Test for input parsing and choice lookup helpers'''
    
    def test_parse_choice_number_input_integer(self):
        # parse_choice_number() should convert numeric text and reject non-numeric text
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

        with self.assertRaises(ScenarioDataError):
            validate_scenario(scenario)

    def test_validate_choice_rejects_missing_id(self):
        choice = {
            "label": "Test Choice",
            "is_correct": True,
            "trust_delta": 1,
            "health_delta": 0,
            "threat_delta": -1
        }

        with self.assertRaises(ScenarioDataError):
            validate_choice(choice)


class TestGameSessionModel(unittest.TestCase):
    '''Tests for the GameSession domain model'''

    def test_game_session_stores_starting_scores(self):
        session = GameSession(trust=82, health=91, threat=38)

        self.assertEqual(session.trust, 82)
        self.assertEqual(session.health, 91)
        self.assertEqual(session.threat, 38)

    def test_game_session_applies_choice_to_scores(self):
        session = GameSession(trust=82, health=91, threat=38)
        choice = Choice(
                choice_id="test_choice",
                label="Test choice",
                is_correct=True,
                trust_delta=8,
                health_delta=-2,
                threat_delta=-16,
            )
        session.apply_choice(choice)

        self.assertEqual(session.trust, 90)
        self.assertEqual(session.health, 89)
        self.assertEqual(session.threat, 22)

    def test_game_session_clamps_scores(self):
        session = GameSession(trust=98, health=91, threat=8)
        choice = Choice(
                choice_id="test_choice",
                label="Test choice",
                is_correct=True,
                trust_delta=8,
                health_delta=-2,
                threat_delta=-16,
            )
        session.apply_choice(choice)

        self.assertEqual(session.trust, 100)
        self.assertEqual(session.health, 89)
        self.assertEqual(session.threat, 0)
    

    #Test final grade outcomes
    def test_game_session_returns_strong_final_grade(self):
        session = GameSession(trust=90, health=80, threat=20)
        
        result = session.get_final_grade()

        self.assertEqual(result, "Strong Incident Response")

    def test_game_session_returns_returns_needs_more_triage_grade(self):
        session = GameSession(trust=65, health=55, threat=50)
        
        result = session.get_final_grade()

        self.assertEqual(result, "Needs More Triage")

    def test_game_session_returns_returns_high_risk_grade(self):
        session = GameSession(trust=40, health=45, threat=80)
        
        result = session.get_final_grade()

        self.assertEqual(result, "High Risk Outcome")
        


if __name__ == "__main__":
    unittest.main()