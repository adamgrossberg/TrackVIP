from Athlete import Athlete
from Run import Run
from User import User
import pandas as pd
import numpy as np
import os

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

    def save_organization_to_csv(self):
        export_path = f'./save_data/{self.id}/'
        os.makedirs(export_path + 'pose_data', exist_ok=True)

        #Users CSV
        user_data = []
        for user in self.users.values():
            id = user.id
            name = user.name
            can_view = user.can_view
            can_add = user.can_add

            user_data.append([id, name, can_view, can_add])

        df = pd.DataFrame(user_data, columns=['id', 'name', 'can_view', 'can_add'])
        df.to_csv(export_path + 'users.csv', index=False)

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
            run_data.append([id, athlete_id, video_path, video_fps, video_resolution_x, video_resolution_y])
            
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

        df = pd.DataFrame(run_data, columns=['id', 'athlete_id', 'video_path', 'video_fps', 'video_resolution_x', 'video_resolution_y'])
        df.to_csv(export_path + 'runs.csv', index=False)
    
    def __str__(self):
        result = f'Organization: {self.name} ({self.id}) \n'
        result += f'Users: \n'
        for user in self.users.values():
            result += f'{str(user)}\n'
        result += f'Runs: \n'
        for run in self.runs.values():
            result += f'{str(run)}\n'
        result += 'Athletes: \n'
        for athlete in self.athletes.values():
            result += f'{str(athlete)}'
        return result