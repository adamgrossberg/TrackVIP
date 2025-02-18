class Video:
    
    def __init__(self, path : str, fps: float, resolution: tuple[int, int]):
        self.path = path
        self.fps = fps
        self.resolution = resolution
    
    def get_path(self):
        return self.path
    
    def get_fps(self):
        return self.fps
    
    def get_resolution(self):
        return self.resolution
    
    def get_resolution_x(self):
        return self.resolution[0]
    
    def get_resolution_y(self):
        return self.resolution[1]
    
    def __str__(self):
        return f'Path: {self.path}; FPS: {self.fps}; Size: {self.resolution}'