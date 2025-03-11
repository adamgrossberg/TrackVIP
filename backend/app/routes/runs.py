from fastapi import APIRouter, Depends, HTTPException
from app.Organization import *
from app.dependencies import get_organization_dependency


router = APIRouter()

@router.post("/")
def create_run(run: RunCreate, org: Organization = Depends(get_organization_dependency)):
    response = org.create_run(run.id, run.athlete_id, run.video_path, run.start_10m_coords_x, run.start_10m_coords_y,
                              run.end_10m_coords_x, run.end_10m_coords_y)
    if not response:
        raise HTTPException(status_code=409, detail=f"Run with ID {run.id} already exists")
    else:
        return response

@router.get("/{run_id}")
def get_run(run_id: str, org: Organization = Depends(get_organization_dependency)):
    run = org.get_run(run_id)
    if run:
        return run
    else:
        raise HTTPException(status_code=404, detail="Run not found")

@router.put("/")
def update_run(run: RunUpdate, org: Organization = Depends(get_organization_dependency)):
    response = org.edit_run(run.id, run.athlete_id)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Run not found")

@router.delete("/{run_id}")
def delete_run(run_id: str, org: Organization = Depends(get_organization_dependency)):
    response = org.delete_run(run_id)
    if response == -1:
        raise HTTPException(status_code=404, detail="Run not found")
    
@router.get("/", response_model=list[RunResponse])
def get_all_runs(org: Organization = Depends(get_organization_dependency)):
    return org.get_all_runs()