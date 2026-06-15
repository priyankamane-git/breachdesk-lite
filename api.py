'''FastAPI application for BreachDesk Lite'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from scenarios import load_scenarios
from input_utils import get_choice_by_number, get_choice_by_id
from models import GameSession
from scoring import check_choice


app = FastAPI(title="BreachDesk Lite API")


class SubmitChoiceRequest(BaseModel):
    '''Request body for submitting a selected choice'''

    scenario_index: int
    choice_id: str
    trust: int
    health: int
    threat: int


@app.get("/health")
def get_health():
    '''Return API health status'''
    return {
        "status": "ok",
        "service": "BreachDesk Lite API"
    }

@app.get("/scenarios")
def get_scenarios():
    '''Return all available scenarios'''
    scenarios = load_scenarios()

    return [scenario.to_dict() for scenario in scenarios]

@app.post("/submit-choice")
def submit_choice(request: SubmitChoiceRequest):
    '''Submit a choice and return updated scores'''

    scenarios = load_scenarios()

    if request.scenario_index < 0 or request.scenario_index >= len(scenarios):
        raise HTTPException(status_code=404, detail="Scenario not found")

    scenario = scenarios[request.scenario_index]
    selected_choice = get_choice_by_id(scenario.choices, request.choice_id)

    if selected_choice is None:
        raise HTTPException(status_code=404, detail="Choice not found")

    session = GameSession(
        trust=request.trust,
        health=request.health,
        threat=request.threat
    )

    session.apply_choice(selected_choice)

    result = check_choice(selected_choice)

    return {
        "result": result,
        "trust": session.trust,
        "health": session.health,
        "threat": session.threat,
        "selected_choice": selected_choice.label
    }

