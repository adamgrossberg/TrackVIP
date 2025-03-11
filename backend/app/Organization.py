from app.local_objects.Athlete import Athlete
from app.local_objects.Run import Run
from app.local_objects.User import User
from app.local_objects.Video import Video

from app.schemas import *
from app.database import *

import numpy as np
import json


class Organization:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.athletes = {} # {id: Athlete}
        self.runs = {} # {id: Run}
        self.users = {} # {id: User}

        self.session = start_database_session()
        self.load_from_db()
    
    def create_athlete(self, id: str, first_name: str, last_name: str):
        if id in self.athletes:
            return None

        athlete = Athlete(id, first_name, last_name)
        self.athletes[id] = athlete
        self.session.add(athlete.to_db())
        self.save_to_db()
        return AthleteResponse(id=id, first_name=first_name, last_name=last_name)
    
    def get_athlete(self, id: str):
        athlete = self.athletes.get(id)
        if athlete:
            return AthleteResponse(id=athlete.id, first_name=athlete.first_name, last_name=athlete.last_name)
        else:
            return None

    def edit_athlete(self, id: str, first_name: str, last_name: str) -> AthleteResponse:
        athlete = self.athletes[id]
        if athlete:
            athlete.first_name = first_name
            athlete.last_name = last_name
            db_athlete = self.session.query(AthleteDB).filter_by(id=id).first()
            db_athlete.first_name = athlete.first_name
            db_athlete.last_name = athlete.last_name
            self.save_to_db()
            return AthleteResponse(id=id, first_name=first_name, last_name=last_name)
        else:
            return None
    
    def delete_athlete(self, id: str) -> int:
        if id in self.athletes:
            self.athletes.pop(id)
            db_athlete = self.session.query(AthleteDB).filter_by(id=id).first()
            self.session.delete(db_athlete)
            self.save_to_db()
            return 0
        else:
            return -1
    
    def get_all_athletes(self) -> list[AthleteResponse]:
        return [AthleteResponse(id=a.id, first_name=a.first_name, last_name=a.last_name) for a in self.athletes.values()]

    def create_run(self, id: str, athlete_id: str, video_path: str,
                   start_10m_coords_x: int, start_10m_coords_y: int,
                   end_10m_coords_x: int, end_10m_coords_y: int) -> None:
        
        if id in self.runs:
            return None
        
        run = Run(id=id, athlete_id=athlete_id, video_path=video_path, 
                  start_10m_coords=(start_10m_coords_x, start_10m_coords_y),
                  end_10m_coords=(end_10m_coords_x, end_10m_coords_y))
        self.runs[id] = run
        self.session.add(run.to_db())
        self.session.add(run.video.to_db())
        self.save_to_db()
        return RunResponse(id=run.id, athlete_id=run.athlete_id, video_path=run.video.path,
                           pose_data=json.dumps(run.pose_data), velocity_data=json.dumps(run.velocity_data))
    
    def get_run(self, id: str):
        run = self.runs.get(id)
        if run:
            return RunResponse(id=run.id, athlete_id=run.athlete_id, video_path=run.video.path,
                               pose_data=json.dumps(run.pose_data.tolist()), velocity_data=json.dumps(run.velocity_data.tolist()))
        else:
            return None

    def edit_run(self, id: str, athlete_id: str) -> None:
        if id in self.runs:
            self.runs[id].athlete_id = athlete_id
            db_run = self.session.query(RunDB).filter_by(id=id).first()
            db_run.athlete_id = athlete_id
            self.save_to_db()
            return RunResponse(id=id, athlete_id=athlete_id, video_path=self.runs[id].video.path)
        else:
            return None
    
    def delete_run(self, id: str) -> int:
        if id in self.runs:
            db_run = self.session.query(RunDB).filter_by(id=id).first()
            self.session.delete(db_run)
            self.runs.pop(id)
            self.save_to_db()
            return 0
        else:
            return -1
    
    def get_all_runs(self) -> list[RunResponse]:
        return [RunResponse(id=r.id, athlete_id=r.athlete_id, video_path=r.video.path) for r in self.runs.values()]

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