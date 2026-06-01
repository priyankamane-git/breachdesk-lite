# BreachDesk Lite

BreachDesk Lite is a Python command-line cybersecurity decision game.

The player reviews a security scenario, chooses a response, and sees how the decision affects customer trust, system health, and threat level.

## Current Status

BreachDesk Lite is currently a modular Python command-line game with unit tests and JSON-backed scenario data.


## Project Structure

- `breachdesk_lite.py` - main CLI game flow
- `scenarios.py` - loads scenario data
- `scenarios.json` - scenario and choice data
- `scoring.py` - scoring and grade helpers
- `input_utils.py` - input parsing and choice lookup helpers
- `test_breachdesk_lite.py` - unit tests

## Skills Practiced So Far

- Modular Python design with separated scoring, input, scenario, and test layers
- JSON-based data loading for scenario-driven gameplay
- Input validation and retry-safe CLI control flow
- Stateful business logic for trust, health, and threat scoring
- Outcome classification using explicit business rules
- Unit test coverage with Python `unittest`
- Runtime logging for user actions, validation failures, and final outcomes
- Git/GitHub workflow with feature branches and commit history

## How To Run Tests

Open `test_breachdesk_lite.py` in VS Code and run the file.

## Roadmap

- Improve input validation
- Add multiple scenarios
- Add tests
- Refactor into modules
- Build a FastAPI backend
- Add a simple frontend
