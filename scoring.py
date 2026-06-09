'''Scoring and outcome helpers for BreachDesk Lite'''


def check_choice(choice):
    '''Return a decision result for the selected choice'''
    if choice.is_correct:
        return "Good Choice"
    return "Risky Choice"


def clamp_score(score):
    '''Helper function to keep a score between 0 and 100'''
    return max(0, min(100, score))


def apply_choice(choice, trust, health, threat):
    '''Apply a choice's score changes and return updated scores'''
    new_trust = clamp_score(trust + choice.trust_delta)
    new_health = clamp_score(health + choice.health_delta)
    new_threat = clamp_score(threat + choice.threat_delta)

    return new_trust, new_health, new_threat


def get_final_grade(trust, health, threat):
    '''Return a final grade based on ending scores'''
    if trust >= 80 and health >= 70 and threat <= 30:
        return "Strong Incident Response"
    if trust >= 60 and health >= 50 and threat <= 60:
        return "Needs More Triage"
    return "High Risk Outcome"