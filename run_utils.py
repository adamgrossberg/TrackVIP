import numpy as np
import pandas as pd
from Video import Video
import os
from moviepy import VideoFileClip
import cv2
import mediapipe as mp
from tqdm import tqdm
import matplotlib.pyplot as plt

def get_video_from_path(path: str, run_id:str) -> Video:
        id = run_id + '_video'
        path, videofileclip = convert_to_mp4(path)
        fps = float(videofileclip.fps)
        resolution = videofileclip.size
        return Video(id, path, fps, resolution)

def convert_to_mp4(path: str) -> str:

    if os.path.exists(path):
        # Extract the directory and file name without extension
        directory, filename = os.path.split(path)
        path_without_extension, original_filetype = os.path.splitext(filename)

        if original_filetype == '.mp4':

            return path, VideoFileClip(path)
        
        else:

            # Create the output file path with the same name but with .mp4 extension
            output_file_path = os.path.join(directory, path_without_extension + '.mp4')
            
            # Load the .MOV video file
            clip = VideoFileClip(path)
            
            # Save the clip as an .MP4 file
            clip.write_videofile(output_file_path, codec="libx264", audio_codec="aac")

            try:
                #Delete original video file
                os.remove(path)
            except PermissionError:
                pass

            return output_file_path, clip
    else:
        raise FileNotFoundError(f'{path} not found.')

def get_pose_data_from_video(video: Video, export_video: bool, run_id: str) -> np.ndarray:
    path = video.path

    # Initialize pose estimator
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    # set cap to the input video path on your device
    cap = cv2.VideoCapture(path)
    frame_width = video.get_resolution_x()
    frame_height = video.get_resolution_y()
    fps = int(video.fps)

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
    progress_bar = tqdm(total=total_frames, desc="Applying Pose Estimation", unit="frame")

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

def calculate_x_velocity(pose_data: np.ndarray, start_10m_coords: tuple[int, int], end_10m_coords: tuple[int, int], fps: float) -> np.ndarray:
    pose_data_with_com = np.append(pose_data, np.reshape(np.average(pose_data, axis=1), (pose_data.shape[0], 1, pose_data.shape[1])), axis=1)

    #Extract x-coordinates of landmarks from data. Shape (num_frames, num_landmarks)
    x_coords = pose_data_with_com[:, :, 0]

    #Calculate instantaneous velocity of points in pixels/frame
    result_in_pixels_per_frame = np.diff(x_coords, axis=0)

    #Convert pixels/frame to meters/second
    meters_per_pixel = 10 / abs(start_10m_coords[0] - end_10m_coords[0])
    frames_per_second = fps
    result = result_in_pixels_per_frame * meters_per_pixel * frames_per_second

    result = smooth(result, 5)

    return result

def smooth(data: np.ndarray, window_size: int) -> np.ndarray:
    kernel = np.ones(window_size) / window_size
    return np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=0, arr=data)

def create_velocity_graph(velocity_data: np.ndarray, fps: float) -> str:
    save_path = './output/graphs/velocity_time.png'
    num_frames, num_points = velocity_data.shape
    time_axis = np.arange(num_frames) / fps  # Time in seconds

    plt.figure(figsize=(10, 6))  # Set figure size

    # Plot velocity of each point
    plt.plot(time_axis, velocity_data[:, 0], label=f"Left hip")
    plt.plot(time_axis, velocity_data[:, 1], label=f"Right hip")
    plt.plot(time_axis, velocity_data[:, 2], label=f"CoM approximation")

    # Labels and title
    plt.xlabel("Time (seconds)")
    plt.ylabel("Velocity (meters/second)")
    plt.title("Instantaneous Velocity of Points Over Time")
    plt.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.15, 1))  # Add legend outside plot
    plt.grid(True, linestyle="--", alpha=0.6)  # Add grid

    # Save figure
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()  # Close plot to avoid display issues in some environments

    return save_path