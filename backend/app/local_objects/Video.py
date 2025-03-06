from app.database import VideoDB

class Video:
    
    def __init__(self, id: str, path : str, fps: float, resolution: tuple[int, int]):
        self.id = id
        self.path = path
        self.fps = fps
        self.resolution = resolution
    
    def get_resolution_x(self) -> int:
        return self.resolution[0]
    
    def get_resolution_y(self) -> int:
        return self.resolution[1]
    
    def to_db(self):
        return VideoDB(id=self.id, path=self.path, fps=self.fps, resolution_x=self.resolution[0], resolution_y=self.resolution[1])

    @staticmethod
    def from_db(db_video: VideoDB):
        return Video(id=db_video.id, path=db_video.path, fps=db_video.fps, resolution=(db_video.resolution_x, db_video.resolution_y))
    
    def __str__(self):
        return f'Path: {self.path}; FPS: {self.fps}; Size: {self.resolution}'