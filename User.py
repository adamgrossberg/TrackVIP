class User:
    def __init__(self, id: str, name:str, can_view: bool, can_add: bool):
        self.id = id
        self.name = name
        self.can_view = can_view
        self.can_add = can_add
    
    def __str__(self):
        return f'{self.name} ({self.id})'