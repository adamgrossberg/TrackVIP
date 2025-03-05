from Athlete import Athlete
from Run import Run
from User import User
from Video import Video
import numpy as np
from database import *
import json

class Organization:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.athletes = {} # {id: Athlete}
        self.runs = {} # {id: Run}
        self.users = {} # {id: User}

        self.session = start_database_session()
    
    def add_athlete(self, id: str, first_name: str, last_name: str) -> None:
        athlete = Athlete(id, first_name, last_name)
        self.athletes[id] = athlete
        self.session.add(athlete.to_db())

    def add_run(self, id: str, athlete_id: str, video_path: str) -> None:
        run = Run(id, athlete_id, video_path)
        self.runs[id] = run
        self.session.add(run.to_db())
        self.session.add(run.video.to_db())
    
    def add_user(self, id: str, name: str) -> None:
        self.users[id] = User(id, name)

    def edit_athlete(self, id: str, first_name: str, last_name: str) -> None:
        self.athletes[id].first_name = first_name
        self.athletes[id].last_name = last_name
        db_athlete = self.session.query(AthleteDB).filter_by(id=id).first()
        db_athlete.first_name = first_name
        db_athlete.last_name = last_name

    def edit_run(self, id: str, athlete_id: str) -> None:
        self.runs[id].athlete_id = athlete_id
        db_run = self.session.query(RunDB).filter_by(id=id).first()
        db_run.athlete_id = athlete_id
    
    def edit_user(self, id: str, name: str) -> None:
        self.users[id].name = name

    def delete_athlete(self, id: str) -> None:
        db_athlete = self.session.query(AthleteDB).filter_by(id=id).first()
        self.session.delete(db_athlete)
        self.athletes.pop(id)
    
    def delete_run(self, id: str) -> None:
        db_run = self.session.query(RunDB).filter_by(id=id).first()
        self.session.delete(db_run)
        self.runs.pop(id)
    
    def delete_user(self, id: str) -> None:
        self.users.pop(id)

    def load_from_db(self) -> None:
        self.athletes = {} # {id: Athlete}
        self.runs = {} # {id: Run}
        self.users = {} # {id: User}
        
        try:
            #Load Users
            db_users = self.session.query(UserDB).all()
            self.users = {u.id: User.from_db(u) for u in db_users}
            # Load athletes
            db_athletes = self.session.query(AthleteDB).all()
            self.athletes = {a.id: Athlete.from_db(a) for a in db_athletes}

            # Load videos into a dictionary for quick lookup
            db_videos = self.session.query(VideoDB).all()
            video_dict = {v.id: Video.from_db(v) for v in db_videos}  # {video_id: Video object}

            # Load runs
            db_runs = self.session.query(RunDB).all()
            for db_run in db_runs:
                # Retrieve the corresponding Video object
                video_obj = video_dict[db_run.video_id]

                # Construct Run object using preloaded Video object
                run = Run(
                    id=db_run.id,
                    athlete_id=db_run.athlete_id,
                    video_path=video_obj.path,  # video_id is the path
                    video=video_obj,  # Pass the preloaded Video object
                    pose_data=np.array(json.loads(db_run.pose_data)) if db_run.pose_data else None,
                    start_10m_coords=(db_run.start_10m_x, db_run.start_10m_y),
                    end_10m_coords=(db_run.end_10m_x, db_run.end_10m_y)
                )

                # Store in dictionary
                self.runs[run.id] = run

            print("All data successfully loaded from the database.")

        except Exception as e:
            print(f"Error loading data from database: {e}")

    def save_to_db(self) -> None:
        self.session.commit()
        self.load_from_db()

    def __str__(self):
        result = f'Organization: {self.name} ({self.id}) \n'
        result += f'Users: \n'
        for user in self.users.values():
            result += f'\t{str(user)}\n'
        result += f'Runs: \n'
        for run in self.runs.values():
            result += f'\t{str(run)}\n'
        result += 'Athletes: \n'
        for athlete in self.athletes.values():
            result += f'\t{str(athlete)}\n'
        return result