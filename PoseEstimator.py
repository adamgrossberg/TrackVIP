from Video import Video
import numpy as np
import cv2
import mediapipe as mp
from tqdm import tqdm
import pandas as pd
import os

#Static class to apply pose estimation model to video
class PoseEstimator:

    # Return pose data as a numpy array of shape (F, P, 2) where P is the # of points and F is the number of frames
    @staticmethod
    def get_pose_data_from_video(video: Video, export_video: bool, run_id: str):
        path = video.get_path()

        # Initialize pose estimator
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        # set cap to the input video path on your device
        cap = cv2.VideoCapture(path)
        frame_width = video.get_resolution_x()
        frame_height = video.get_resolution_y()
        fps = int(video.get_fps())

        # Set output configuration
        if export_video:
            os.makedirs('./output_videos', exist_ok=True)
            output_path = f'./output_videos/{run_id}_pose.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for .mp4 files
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        # Initialize array to store pose estimation data
        pose_data = []
        key_landmarks = [mp_pose.PoseLandmark.LEFT_HIP, 
                         mp_pose.PoseLandmark.RIGHT_HIP]


        # Initialize tqdm progress bar
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = tqdm(total=total_frames, desc="Processing Frames", unit="frame")

        while cap.isOpened():
            # read frame
            ret, frame = cap.read()
            if not ret:
                break
            try:
                progress_bar.update(1)

                # resize the frame 
                frame = cv2.resize(frame, (frame_width, frame_height))
                # convert to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                #process frame
                pose_results = pose.process(frame_rgb)
                
                # store results
                if pose_results.pose_landmarks:
                    frame_landmarks = []
                    for landmark in key_landmarks:
                        current_landmark = pose_results.pose_landmarks.landmark[landmark]
                        frame_landmarks.append([current_landmark.x * frame_width, current_landmark.y * frame_height])

                    pose_data.append(frame_landmarks)
                
                    
                
                #video output
                if export_video:
                    if pose_results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        for landmark in key_landmarks:
                            cv2.circle(frame, (int(current_landmark.x * frame.shape[1]), int(current_landmark.y * frame.shape[0])), 10, (0, 255, 0), -1)
                    out.write(frame)
                
            except:
                break

            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        if export_video:
            out.release()
        cv2.destroyAllWindows()

        pose_data = np.array(pose_data) # Numpy array of size (num_frames, num_landmarks, num_dimensions). num_dimensions is 2 (x, y)

        return pose_data
    

    @staticmethod
    def export_pose_data_to_csv(data: np.ndarray):
        save_path = './output/csv/position.csv'
        num_frames, num_points, _ = data.shape

        # Reshape position array to (num_frames, num_points * 2) -> Flatten x, y for each point
        reshaped_positions = data.reshape(num_frames, num_points * 2)

        # Create column names: "Point 1 X", "Point 1 Y", "Point 2 X", "Point 2 Y", etc.
        column_names = []
        for i in range(num_points):
            column_names.append(f"Point {i+1} X")
            column_names.append(f"Point {i+1} Y")

        # Create DataFrame
        df = pd.DataFrame(reshaped_positions, columns=column_names)
        df.insert(0, "Frame #", np.arange(num_frames))  # Insert time column at the beginning

        # Save to CSV
        df.to_csv(save_path, index=False)