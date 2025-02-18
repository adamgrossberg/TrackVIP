from VideoProcessor import VideoProcessor as vp
from PoseEstimator import PoseEstimator as pose
from Calculator import Calculator as calc
from Visualizer import Visualizer as viz

class Run:

    def __init__(self, video_path: str, athlete: str):
        self.athlete = athlete
        
        # Use VideoProcessor to create Video object that contains path to mp4, fps, resolution fields
        self.video = vp.get_video_from_path(video_path)
        print(f'Created Video object: {str(self.video)}')
        input('Press enter to continue...')

        # Use PoseEstimator to get pose estimation points from video in a np array
        self.pose_data = pose.get_pose_data_from_video(self.video, export_video=True, export_csv=True)
        print('Pose detection applied successfully.')
        input('Press enter to continue...')

        # Set the start and end coordinates of the 10m reference in the video
        self.start_10m_coords = (int(input('Start pixel value of 10m: ')), 0)
        self.end_10m_coords = (int(input('End pixel value of 10m: ')), 0)

        # Calculate the velocity data using Calculator
        self.velocity_data = calc.calculate_x_velocity(self.pose_data, self.start_10m_coords, self.end_10m_coords, self.video.get_fps(), export_csv=True)
        print('Velocity calculated successfully.')
        input('Press enter to continue...')

        # Create graphs using Visualizer
        self.graphs = viz.create_velocity_graph(self.velocity_data, self.video.get_fps())
        print('Graph(s) created successfully.')
    
    def get_athlete(self):
        return self.athlete

    def get_video(self):
        return self.video
    
    def get_pose_data(self):
        return self.pose_data
    
    def get_velocity_data(self):
        return self.velocity_data