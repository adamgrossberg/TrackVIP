from Athlete import Athlete
from Run import Run
from User import User

class Organization:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.athletes = {} # {id: Athlete}
        self.runs = {} # {id: Run}
        self.users = {} # {id: User}
    
    def add_athlete(self, id: str, first_name: str, last_name: str):
        self.athletes[id] = Athlete(id, first_name, last_name)

    def add_run(self, id: str, video_path: str, athlete_id: str):
        self.runs[id] = Run(id, video_path, athlete_id)
    
    def add_user(self, id: str, name: str, can_view: bool, can_add: bool):
        self.users[id] = User(id, name, can_view, can_add)
    
    def __str__(self):
        result = f'Organization: {self.name} ({self.id}) \n'
        result += f'Users: \n'
        for user in self.users.items():
            result += f'{str(user)}\n'
        result += f'Runs: \n'
        for run in self.runs.items():
            result += f'{str(run)}\n'
        result += 'Athletes: \n'
        for athlete in self.athletes.items():
            result += f'{str(athlete)}'
        return result