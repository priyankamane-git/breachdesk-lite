'''FastAPI application for BreachDesk Lite'''

from fastapi import FastAPI

app = FastAPI(title="BreachDesk Lite API")


@app.get("/health")
def get_health():
    '''Return API health status'''
    return {
        "status": "ok",
        "service": "BreachDesk Lite API"
    }