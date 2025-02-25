class Athlete:
    def __init__(self, id: str, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
    
    def __str__(self):
        return f'{self.id + ':':<20}{self.first_name} {self.last_name}'