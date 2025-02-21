class Athlete:
    def __init__(self, id: str):
        self.id = id
        self.runs = []
    
    def add_run(self, run_id: str):
        self.runs.append(run_id)
        pass