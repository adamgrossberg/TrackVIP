from app.database import UserDB

class User:
    def __init__(self, id: str, name:str):
        self.id = id
        self.name = name

    def to_db(self):
        return UserDB(id=self.id, name=self.name)
    
    @staticmethod
    def from_db(db_user: UserDB):
        return User(id=db_user.id, name=db_user.name)
    
    def __str__(self):
        return f'{self.id + ":":<20}{self.name:<20}'