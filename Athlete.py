class Athlete:
    def __init__(self, id: str, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.runs = []
    
    def add_run(self, run_id: str):
        self.runs.append(run_id)
        pass