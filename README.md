# BreachDesk Lite

BreachDesk Lite is a Python command-line cybersecurity decision game.

The player reviews a security scenario, chooses a response, and sees how the decision affects customer trust, system health, and threat level.

## Current Status

BreachDesk Lite is currently a modular Python command-line game with JSON-backed scenario data, validation, a `Scenario` domain model, and unit tests.

## Project Structure

- `breachdesk_lite.py` - main CLI game flow
- `models.py` - domain models such as `Scenario`
- `scenarios.py` - loads and validates scenario data
- `scenarios_data.json` - scenario and choice data
- `scoring.py` - scoring and grade helpers
- `input_utils.py` - input parsing and choice lookup helpers
- `test_breachdesk_lite.py` - unit tests

## Skills Practiced So Far

- Modular Python design with separated scoring, input, scenario, model, and test layers
- JSON-based data loading for scenario-driven gameplay
- Scenario data validation with explicit failure cases
- Domain modeling with a `Scenario` class
- Input validation and retry-safe CLI control flow
- Stateful business logic for trust, health, and threat scoring
- Outcome classification using explicit business rules
- Unit test coverage with Python `unittest`
- Runtime logging for user actions, validation failures, and final outcomes
- Git/GitHub workflow with feature branches and commit history

## How To Run

Open `breachdesk_lite.py` in VS Code and run the file.

## How To Run Tests

Open `test_breachdesk_lite.py` in VS Code and run the file.

## Roadmap

- Add a `Choice` domain model
- Add a `GameSession` domain model
- Refine object-oriented design
- Add custom exceptions for validation failures
- Build a FastAPI backend
- Add a simple frontend
