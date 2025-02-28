from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from database_utils import Base

class AthleteDB(Base):
    __tablename__ = 'athletes'
    
    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Relationship with Run
    runs = relationship("RunDB", back_populates="athlete", cascade="all, delete-orphan")

class VideoDB(Base):
    __tablename__ = 'videos'
    
    id = Column(String, primary_key=True)
    path = Column(String, nullable=False)
    fps = Column(Float, nullable=False)
    resolution_x = Column(Integer, nullable=False)
    resolution_y = Column(Integer, nullable=False)

    # 1-to-1 Relationship with Run
    run = relationship("RunDB", back_populates="video", uselist=False)  # Ensures one-to-one

class RunDB(Base):
    __tablename__ = 'runs'
    
    id = Column(String, primary_key=True)
    athlete_id = Column(String, ForeignKey('athletes.id'), nullable=False)
    video_id = Column(String, ForeignKey('videos.id', ondelete="CASCADE"), unique=True, nullable=False)  # UNIQUE constraint for 1-to-1
    pose_data = Column(String, nullable=True)  # Stored as JSON string
    start_10m_x = Column(Integer, nullable=False)
    start_10m_y = Column(Integer, nullable=False)
    end_10m_x = Column(Integer, nullable=False)
    end_10m_y = Column(Integer, nullable=False)

    # Relationships
    athlete = relationship("AthleteDB", back_populates="runs")
    video = relationship("VideoDB", back_populates="run", uselist=False)  # Ensures 1-to-1