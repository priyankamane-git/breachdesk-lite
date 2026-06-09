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
            choices=data["choices"]
        )