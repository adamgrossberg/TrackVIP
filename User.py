class User:
    def __init__(self, id: str, can_view: bool, can_add: bool):
        self.id = id
        self.can_view = can_view
        self.can_add = can_add