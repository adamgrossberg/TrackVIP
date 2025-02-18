import numpy as np
import matplotlib.pyplot as plt

class Visualizer:

    # Return path to generated plot
    @staticmethod
    def create_velocity_graph(velocity_data: np.ndarray, fps: float):
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