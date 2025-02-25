import numpy as np
import pandas as pd
from Video import Video
import os
from moviepy import VideoFileClip

def get_video_from_path(path: str) -> Video:
        path, videofileclip = convert_to_mp4(path)
        fps = float(videofileclip.fps)
        resolution = videofileclip.size
        return Video(path, fps, resolution)

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


def calculate_x_velocity(pose_data: np.ndarray, start_10m_coords: tuple[int, int], end_10m_coords: tuple[int, int], fps: float):
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

@staticmethod
def smooth(data: np.ndarray, window_size: int):
    kernel = np.ones(window_size) / window_size
    return np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=0, arr=data)