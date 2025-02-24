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

    def add_run(self, id: str, athlete_id: str, video_path: str):
        self.runs[id] = Run(id, athlete_id, video_path)
    
    def add_user(self, id: str, name: str, can_view: bool, can_add: bool):
        self.users[id] = User(id, name, can_view, can_add)

    def edit_athlete(self, id: str, first_name: str, last_name: str):
        self.athletes[id].first_name = first_name
        self.athletes[id].last_name = last_name

    def edit_run(self, id: str, athlete_id: str, video_path: str):
        self.runs[id].athlete_id = athlete_id
    
    def edit_user(self, id: str, name: str, can_view: bool, can_add: bool):
        self.users[id].name = name
        self.users[id].can_view = can_view
        self.users[id].can_add = can_view

    def delete_athlete(self, id: str):
        self.athletes.pop(id)
    
    def delete_run(self, id: str):
        self.runs.pop(id)
    
    def delete_user(self, id: str):
        self.users.pop(id)

    def save_to_csv(self):
        export_path = f'./save_data/{self.id}/'
        os.makedirs(export_path + 'pose_data', exist_ok=True)

        #Organization information (just name for now)
        name_arr = np.array([['name'], [self.name]])
        np.savetxt(export_path + f'{self.id}_info.csv', name_arr, fmt='%s', delimiter=',')

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

    def load_from_csv(self, id: str):
        self.id = id
        self.athletes = {}
        self.runs = {}
        self.users = {}

        input_path = f'./save_data/{id}/'
        org_info = np.loadtxt(input_path + f'{id}_info.csv', dtype=str, delimiter=',', skiprows=1)
        self.name = org_info
        #Load Users from csv
        user_data = np.loadtxt(input_path + 'users.csv', dtype=str, delimiter=',', skiprows=1)
        if isinstance(user_data[0], str):
            user_data = [user_data]
        for user in user_data:
            user_id = user[0]
            user_name = user[1]
            can_view = (user[2] == 'True')
            can_add = (user[3] == 'True')
            self.users[user_id] = User(user_id, user_name, can_view, can_add)
        #Load Athletes from csv
        athlete_data = np.loadtxt(input_path + 'athletes.csv', dtype=str, delimiter=',', skiprows=1)
        if isinstance(athlete_data[0], str):
            athlete_data = [athlete_data]
        for athlete in athlete_data:
            athlete_id = athlete[0]
            first_name = athlete[1]
            last_name = athlete[2]
            self.athletes[athlete_id] = Athlete(athlete_id, first_name, last_name)
        #Load Runs and pose data from csv
        run_data = np.loadtxt(input_path + 'runs.csv', dtype=str, delimiter=',', skiprows=1)
        if isinstance(run_data[0], str):
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

            self.runs[run_id] = Run(run_id, athlete_id, video_path, video_fps, (video_resolution_x, video_resolution_y), pose_data, 
                                    (start_10m_coords_x, start_10m_coords_y), (end_10m_coords_x, end_10m_coords_y))

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