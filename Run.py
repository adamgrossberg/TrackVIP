from run_utils import *
from PoseEstimator import PoseEstimator as pose
from Visualizer import Visualizer as viz

class Run:

    def __init__(self, id: str, athlete_id: str, video_path: str, 
                 fps=None, resolution=None, pose_data=None, start_10m_coords=None, end_10m_coords=None):
        self.id = id
        self.athlete_id = athlete_id
        
        if fps and resolution:
            self.video = Video(video_path, fps, resolution)
        else:
            # Create Video object that contains path to mp4, fps, resolution fields
            self.video = get_video_from_path(video_path)
            print(f'Created Video object: {str(self.video)}')
            input('Press enter to continue...')

        if pose_data.any():
            self.pose_data = pose_data
        else:
            # Use PoseEstimator to get pose estimation points from video in a np array
            self.pose_data = pose.get_pose_data_from_video(self.video, export_video=True)
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
        self.velocity_data = calculate_x_velocity(self.pose_data, self.start_10m_coords, self.end_10m_coords, self.video.get_fps())

    
    def get_athlete(self):
        return self.athlete

    def get_video(self):
        return self.video
    
    def get_pose_data(self):
        return self.pose_data
    
    def get_velocity_data(self):
        return self.velocity_data
    
    def __str__(self):
        result = f'{self.id + ':':<20}{self.athlete_id:<20}'
        return result