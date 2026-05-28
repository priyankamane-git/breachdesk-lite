'''Scenarios data for BreachDesk Lite.'''

#Choices Tradeoffs examples:
#1. Ignore: trust drops, threat rises
#2. Rotate key: trust rises, health slightly drops, threat drops
#3. Delete account: threat drops somewhat, but trust and health drop badly

# Scenario data is stored as a list so the game can run multiple rounds.
# Each scenario owns its own choices, which keeps the prompt and responses together.
SCENARIOS = [
    {
        "title": "A customer key might be stolen",
        "severity": "High",
        "summary": "A customer API key is being used from two countries",
        "choices": [
            {
                "id": "ignore",
                "label": "Do nothing for now",
                "is_correct": False,
                "trust_delta": -12,
                "health_delta": 0,
                "threat_delta": 18   
            },
            {
                "id": "rotate_key",
                "label": "Replace the key and alert the customer",
                "is_correct": True,
                "trust_delta": 8,
                "health_delta": -2,
                "threat_delta": -16
            },
            {
                "id": "delete_account",
                "label": "Delete the customer account",
                "is_correct": False,
                "trust_delta": -18,
                "health_delta": -8,
                "threat_delta": -6
            }
        ]
    },
    {
        "title": "Webhook retries are flooding the system",
        "severity": "Medium",
        "summary": "A partner webhook is sending the same failed payment event repeatedly",
        "choices": [
            {
                "id": "ignore",
                "label": "Ignore it because retries are normal",
                "is_correct": False,
                "trust_delta": -6,
                "health_delta": -10,
                "threat_delta": 8
            },
            {
                "id": "deduplicate",
                "label": "Deduplicate events and investigate the retry source",
                "is_correct": True,
                "trust_delta": 7,
                "health_delta": 8,
                "threat_delta": -10
            },
            {
                "id": "block_partner",
                "label": "Block the partner integration immediately",
                "is_correct": False,
                "trust_delta": -10,
                "health_delta": 4,
                "threat_delta": -4
            }
        ]
    }
]