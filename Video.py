class Video:
    
    def __init__(self, path : str, fps: float, resolution: tuple[int, int]):
        self.path = path
        self.fps = fps
        self.resolution = resolution
    
    def get_resolution_x(self) -> int:
        return self.resolution[0]
    
    def get_resolution_y(self) -> int:
        return self.resolution[1]
    
    def __str__(self):
        return f'Path: {self.path}; FPS: {self.fps}; Size: {self.resolution}'