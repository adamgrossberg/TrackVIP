import numpy as np
import pandas as pd

class Calculator:
    
    @staticmethod
    def append_average(data: np.ndarray):
        com = np.reshape(np.average(data, axis=1), (data.shape[0], 1, data.shape[1])) #average over the points dimension, shape (num_frames, 1, 2)
        return np.append(data, com, axis=1)
    

    # Return instantaneous x velocity at each frame as a (P, F) numpy array
    @staticmethod
    def calculate_x_velocity(pose_data: np.ndarray, start_10m_coords: tuple[int, int], end_10m_coords: tuple[int, int], fps: float, export_csv: bool):
        pose_data_with_com = Calculator.append_average(pose_data)

        #Extract x-coordinates of landmarks from data. Shape (num_frames, num_landmarks)
        x_coords = pose_data_with_com[:, :, 0]

        #Calculate instantaneous velocity of points in pixels/frame
        result_in_pixels_per_frame = np.diff(x_coords, axis=0)

        #Convert pixels/frame to meters/second
        meters_per_pixel = 10 / abs(start_10m_coords[0] - end_10m_coords[0])
        frames_per_second = fps
        result = result_in_pixels_per_frame * meters_per_pixel * frames_per_second

        result = Calculator.smooth(result, 5)

        if export_csv:
            export_path = './output/csv/velocity.csv'
            num_frames = result.shape[0]

            # Create DataFrame with Time and Velocity Columns
            df = pd.DataFrame(result, columns=[f"Point {i+1}" for i in range(result.shape[1])])
            df.insert(0, "Frame #", np.arange(num_frames))  # Add time column

            # Save to CSV
            df.to_csv(export_path, index=False)

        return result
    
    @staticmethod
    def smooth(data: np.ndarray, window_size: int):
        kernel = np.ones(window_size) / window_size
        return np.apply_along_axis(lambda m: np.convolve(m, kernel, mode='same'), axis=0, arr=data)