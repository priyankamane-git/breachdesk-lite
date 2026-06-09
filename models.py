'''Domain models for BreachDesk Lite'''


class Scenario:
    '''Represents one security scenario in the game'''

    def __init__(self, title, severity, summary, choices):
        self.title = title
        self.severity = severity
        self.summary = summary
        self.choices = choices

    @classmethod
    def from_dict(cls, data):
        '''Create a Scenario object from dictionary data''' 
        return cls(
            title=data["title"],
            severity=data["severity"],
            summary=data["summary"],
            choices=[Choice.from_dict(choice) for choice in data["choices"]]
        )


class Choice:
    '''Represents one response choice in a scenario'''
    
    def __init__(self, choice_id, label, is_correct, trust_delta, health_delta, threat_delta):

        self.id = choice_id
        self.label = label
        self.is_correct = is_correct
        self.trust_delta = trust_delta
        self.health_delta = health_delta
        self.threat_delta = threat_delta

    @classmethod
    def from_dict(cls, data):
        '''Create a Choice object from dictionary data'''
        return cls(
            choice_id=data["id"],
            label=data["label"],
            is_correct=data["is_correct"],
            trust_delta=data["trust_delta"],
            health_delta=data["health_delta"],
            threat_delta=data["threat_delta"]
        )