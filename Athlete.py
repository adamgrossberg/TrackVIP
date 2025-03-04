from database import AthleteDB

class Athlete:
    def __init__(self, id: str, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def to_db(self) -> AthleteDB:
        return AthleteDB(id=self.id, first_name=self.first_name, last_name=self.last_name)

    @staticmethod
    def from_db(db_athlete: AthleteDB):
        return Athlete(id=db_athlete.id, first_name=db_athlete.first_name, last_name=db_athlete.last_name)
    
    def __str__(self):
        return f'{self.id + ':':<20}{self.first_name} {self.last_name}'