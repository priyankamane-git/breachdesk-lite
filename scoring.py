'''Scoring and outcome helpers for BreachDesk Lite'''


def check_choice(choice):
    '''Return a decision result for the selected choice'''
    if choice.is_correct:
        return "Good Choice"
    return "Risky Choice"


def clamp_score(score):
    '''Helper function to keep a score between 0 and 100'''
    return max(0, min(100, score))