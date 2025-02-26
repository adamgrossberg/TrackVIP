from Organization import Organization
from typing import Tuple
import os

def add_athlete_is_valid(org: Organization, athlete_id: str) -> Tuple[bool, str]:
    result = True
    message = 'Invalid.'
    
    if athlete_id in org.athletes.keys():
        result = False
        message += f' Athlete with ID {athlete_id} already exists.'
    
    return result, message

def add_run_is_valid(org: Organization, run_id: str, athlete_id: str, video_path: str) -> Tuple[bool, str]:
    result = True
    message = 'Invalid.'

    if run_id in org.runs.keys():
        result = False
        message += f' Run with ID {run_id} already exists.'
    if athlete_id not in org.athletes.keys():
        result = False
        message += f' Athlete with ID {athlete_id} does not exist.'
    if not os.path.exists(video_path):
        result = False
        message += f' Video at {video_path} does not exist.'
    
    return result, message

def edit_athlete_is_valid(org: Organization, athlete_id: str) -> Tuple[bool, str]:
    result = True
    message = 'Invalid.'

    if athlete_id not in org.athletes.keys():
        result = False
        message += f' Athlete with ID {athlete_id} does not exist.'

    return result, message

def edit_run_is_valid(org: Organization, run_id: str, athlete_id: str) -> Tuple[bool, str]:
    result = True
    message = 'Invalid.'

    if run_id not in org.runs.keys():
        result = False
        message += f' Run with ID {run_id} does not exist.'
    if athlete_id not in org.athletes.keys():
        result = False
        message += f' Athlete with ID {athlete_id} does not exist.'

    return result, message