from Athlete import Athlete
from Run import Run
from User import User
from Video import Video
import pandas as pd
import numpy as np
import os
from database_utils import *
from orm_classes import UserDB, AthleteDB, RunDB, VideoDB
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

    def save_to_csv(self) -> None:
        export_path = f'./save_data/'
        os.makedirs(export_path + 'pose_data', exist_ok=True)

        #Athletes CSV
        athlete_data = []
        for athlete in self.athletes.values():
            id = athlete.id
            first_name = athlete.first_name
            last_name = athlete.last_name

            athlete_data.append([id, first_name, last_name])

        df = pd.DataFrame(athlete_data, columns=['id', 'first_name', 'last_name'])
        df.to_csv(export_path + 'athletes.csv', index=False)

        #Runs and pose data CSVs
        run_data = []
        for run in self.runs.values():
            id = run.id
            athlete_id = run.athlete_id
            video_path = run.video.path
            video_fps = run.video.fps
            video_resolution_x = run.video.resolution[0]
            video_resolution_y = run.video.resolution[1]
            start_10m_coords_x = run.start_10m_coords[0]
            start_10m_coords_y = run.start_10m_coords[1]
            end_10m_coords_x = run.end_10m_coords[0]
            end_10m_coords_y = run.end_10m_coords[1]
            run_data.append([id, athlete_id, video_path, video_fps, video_resolution_x, video_resolution_y,
                             start_10m_coords_x, start_10m_coords_y, end_10m_coords_x, end_10m_coords_y])
            
            #Export pose data from run into separate csv
            pose_data = run.pose_data
            num_frames, num_points, _ = pose_data.shape

            reshaped_positions = pose_data.reshape(num_frames, num_points * 2)

            column_names = []
            for i in range(num_points):
                column_names.append(f"Point {i+1} X")
                column_names.append(f"Point {i+1} Y")

            df = pd.DataFrame(reshaped_positions, columns=column_names)
            df.insert(0, "Frame #", np.arange(num_frames))  # Insert time column at the beginning

            df.to_csv(export_path + f'pose_data/{id}.csv', index=False)

        df = pd.DataFrame(run_data, columns=['id', 'athlete_id', 'video_path', 'video_fps', 'video_resolution_x', 'video_resolution_y', 
                                             'start_10m_coords_x', 'start_10m_coords_y', 'end_10m_coords_x', 'end_10m_coords_y'])
        df.to_csv(export_path + 'runs.csv', index=False)

    def load_from_csv(self) -> None:
        self.athletes = {}
        self.runs = {}
        self.users = {}

        input_path = f'./save_data/'
        org_info = np.loadtxt('./init_data/organization_info.csv', dtype=str, delimiter=',', skiprows=1)
        self.id = org_info[0]
        self.name = org_info[1]
        #Load Users from csv
        user_data = np.loadtxt('./init_data/users.csv', dtype=str, delimiter=',', skiprows=1)
        if isinstance(user_data[0], str):
            user_data = [user_data]
        for user in user_data:
            user_id = user[0]
            user_name = user[1]
            self.users[user_id] = User(user_id, user_name)
        #Load Athletes from csv
        if os.path.exists(input_path + 'athletes.csv'):
            athlete_data = np.loadtxt(input_path + 'athletes.csv', dtype=str, delimiter=',', skiprows=1)
            if isinstance(athlete_data[0], str):
                athlete_data = [athlete_data]
            for athlete in athlete_data:
                athlete_id = athlete[0]
                first_name = athlete[1]
                last_name = athlete[2]
                self.athletes[athlete_id] = Athlete(athlete_id, first_name, last_name)
        #Load Runs and pose data from csv
        if os.path.exists(input_path + 'runs.csv'):
            run_data = np.loadtxt(input_path + 'runs.csv', dtype=str, delimiter=',', skiprows=1)
            if len(run_data) > 0 and isinstance(run_data[0], str):
                run_data = [run_data]
            for run in run_data:
                run_id = run[0]
                athlete_id = run[1]
                video_path = run[2]
                video_fps = float(run[3])
                video_resolution_x = int(run[4])
                video_resolution_y = int(run[5])
                start_10m_coords_x = int(run[6])
                start_10m_coords_y = int(run[7])
                end_10m_coords_x = int(run[8])
                end_10m_coords_y = int(run[9])

                pose_data = np.loadtxt(input_path + f'pose_data/{run_id}.csv', delimiter=',', skiprows=1)[:, 1:]
                pose_data = pose_data.reshape(pose_data.shape[0], pose_data.shape[1] // 2, 2)

                self.runs[run_id] = Run(run_id, athlete_id, video_path, Video(video_path, video_fps, (video_resolution_x, video_resolution_y)), pose_data, 
                                        (start_10m_coords_x, start_10m_coords_y), (end_10m_coords_x, end_10m_coords_y))

    def load_from_db(self) -> None:
        
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