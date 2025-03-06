from pydantic import BaseModel

class AthleteResponse(BaseModel):
    id: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class AthleteCreate(BaseModel):
    id: str
    first_name: str
    last_name: str

class AthleteUpdate(BaseModel):
    id: str
    first_name: str
    last_name: str

class RunResponse(BaseModel):
    id: str
    athlete_id: str
    video_path: str

class RunCreate(BaseModel):
    id: str
    athlete_id: str
    video_path: str
    start_10m_coords_x: int
    start_10_coords_y: int
    end_10m_coords_x: int
    end_10_coords_y: int

class RunUpdate(BaseModel):
    id: str
    athlete_id: str