class User:
    def __init__(self, id: str, name:str):
        self.id = id
        self.name = name
    
    def __str__(self):
        return f'{self.id + ':':<20}{self.name:<20}'