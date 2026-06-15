'''Input parsing helpers for BreachDesk Lite'''


import logging as LOG


def parse_choice_number(player_input):
    '''Convert player input into a choice number, or return None'''
    try:
        return int(player_input)
    except ValueError:
        LOG.warning("Invalid non-numeric choice entered: %s", player_input)
        return None


def get_choice_by_number(choices, choice_number):
    '''Return the choice that matches a player's numeric selection'''
    index = choice_number - 1
    if index < 0 or index >= len(choices):
        return None

    return choices[index]


def get_choice_by_id(choices, choice_id):
    '''Return the choice that matches a choice ID'''
    for choice in choices:
        if choice.id == choice_id:
            return choice
    
    return None