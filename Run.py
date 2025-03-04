from run_utils import *
import json
from database import RunDB

class Run:

    def __init__(self, id: str, athlete_id: str, video_path: str, 
                 video=None, pose_data=None, start_10m_coords=None, end_10m_coords=None):
        self.id = id
        self.athlete_id = athlete_id
        
        if video:
            self.video = video
        else:
            # Create Video object that contains path to mp4, fps, resolution fields
            self.video = get_video_from_path(video_path, self.id)
            print(f'Created Video object: {str(self.video)}')
            input('Press enter to continue...')

        if pose_data is not None:
            self.pose_data = pose_data
        else:
            self.pose_data = get_pose_data_from_video(self.video, export_video=True, run_id=self.id)
            print('Pose detection applied successfully.')
            input('Press enter to continue...')

        if start_10m_coords:
            self.start_10m_coords = start_10m_coords
        else:
            self.start_10m_coords = (int(input('Start pixel value of 10m: ')), 0)
        
        if end_10m_coords:
            self.end_10m_coords = end_10m_coords
        else:
            self.end_10m_coords = (int(input('End pixel value of 10m: ')), 0)

        # Calculate the velocity data using Calculator
        self.velocity_data = calculate_x_velocity(self.pose_data, self.start_10m_coords, self.end_10m_coords, self.video.fps)

    def to_db(self):
        return RunDB(
            id=self.id,
            athlete_id=self.athlete_id,
            video_id=self.video.id,
            pose_data=json.dumps(self.pose_data.tolist()),  # Convert to JSON string
            start_10m_x=self.start_10m_coords[0],
            start_10m_y=self.start_10m_coords[1],
            end_10m_x=self.end_10m_coords[0],
            end_10m_y=self.end_10m_coords[1]
        )

    @staticmethod
    def from_db(db_run):
        return Run(
            id=db_run.id,
            athlete_id=db_run.athlete_id,
            video_id=db_run.video_id,
            pose_data=np.array(json.loads(db_run.pose_data)),  # Convert JSON string back to dict
            start_10m_coords=(db_run.start_10m_x, db_run.start_10m_y),
            end_10m_coords=(db_run.end_10m_x, db_run.end_10m_y)
        )
    
    def __str__(self):
        result = f'{self.id + ':':<20}{self.athlete_id:<20}'
        return result