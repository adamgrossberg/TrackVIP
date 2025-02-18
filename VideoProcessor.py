from Video import Video
from moviepy import VideoFileClip
import os

class VideoProcessor:
    @staticmethod
    def get_video_from_path(path: str) -> Video:
        path, videofileclip = VideoProcessor.convert_to_mp4(path)
        fps = VideoProcessor.extract_fps(videofileclip)
        resolution = VideoProcessor.extract_resolution(videofileclip)
        return Video(path, fps, resolution)
    
    # Converts video to mp4 and returns path to converted video.
    @staticmethod
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

                print('Done.')
                return output_file_path, clip
        else:
            raise FileNotFoundError(f'{path} not found.')
    
    # Return the framerate of the given video as a float
    @staticmethod
    def extract_fps(videofileclip: VideoFileClip) -> float:
        return float(videofileclip.fps)

    # Return resolution of the video as a tuple (x, y)
    @staticmethod
    def extract_resolution(videofileclip: VideoFileClip) -> tuple[int, int]:
        return videofileclip.size