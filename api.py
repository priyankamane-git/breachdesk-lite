'''FastAPI application for BreachDesk Lite'''

from fastapi import FastAPI
from scenarios import load_scenarios

app = FastAPI(title="BreachDesk Lite API")


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