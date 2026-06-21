'''FastAPI application for BreachDesk Lite'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

from config import APP_NAME, STARTING_HEALTH, STARTING_THREAT, STARTING_TRUST
from models import GameSession
from input_utils import get_choice_by_number, get_choice_by_id
from scenarios import load_scenarios
from scoring import check_choice


app = FastAPI(title=f"{APP_NAME} API")


SESSIONS = {}


class SubmitChoiceRequest(BaseModel):
    '''Request body for submitting a selected choice'''

    session_id: str
    scenario_index: int
    choice_id: str


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

    session = SESSIONS.get(request.session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session.apply_choice(selected_choice)

    result = check_choice(selected_choice)

    result_response = {
        "result": result,
        "trust": session.trust,
        "health": session.health,
        "threat": session.threat,
        "selected_choice": selected_choice.label
    }

    return result_response

@app.post("/sessions")
def create_session():
    '''Create a new game session'''
    session_id = str(uuid4())

    session = GameSession(
        trust=STARTING_TRUST,
        health=STARTING_HEALTH,
        threat=STARTING_THREAT
    )

    SESSIONS[session_id] = session

    session_response = {
        "session_id": session_id,
        "trust": session.trust,
        "health": session.health,
        "threat": session.threat,
    }

    return session_response