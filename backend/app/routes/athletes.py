from fastapi import APIRouter, Depends, HTTPException
from app.Organization import *
from app.dependencies import get_organization_dependency


router = APIRouter()

@router.post("/")
def create_athlete(athlete: AthleteCreate, org: Organization = Depends(get_organization_dependency)):
    response = org.create_athlete(athlete.id, athlete.first_name, athlete.last_name)
    if not response:
        raise HTTPException(status_code=409, detail=f"Athlete with ID {athlete.id} already exists.")
    else:
        return response

@router.get("/{athlete_id}")
def get_athlete(athlete_id: str, org: Organization = Depends(get_organization_dependency)):
    athlete = org.get_athlete(athlete_id)
    if athlete:
        return athlete
    else:
        raise HTTPException(status_code=404, detail="Athlete not found")

@router.put("/")
def update_athlete(athlete: AthleteUpdate, org: Organization = Depends(get_organization_dependency)):
    response = org.edit_athlete(athlete.id, athlete.first_name, athlete.last_name)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Athlete not found")

@router.delete("/{athlete_id}")
def delete_athlete(athlete_id: str, org: Organization = Depends(get_organization_dependency)):
    response = org.delete_athlete(athlete_id)
    if response == -1:
        raise HTTPException(status_code=404, detail="Athlete not found")

@router.get("/", response_model=list[AthleteResponse])
def get_all_athletes(org: Organization = Depends(get_organization_dependency)):
    return org.get_all_athletes()