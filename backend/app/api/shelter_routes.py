"""
Shelter Logistics & Capacity API Endpoints.
Provides status, bed occupancy, supply levels, and contacts for emergency relief centers.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.schemas.pydantic_models import ShelterInfo
from backend.app.database.seed_data import get_region_data

router = APIRouter(prefix="/api/shelters", tags=["Shelters & Logistics"])

@router.get("", response_model=List[ShelterInfo])
def get_shelters(region_id: str = "kerala_ernakulam"):
    """
    Get all active disaster relief shelters in the designated district.
    """
    data = get_region_data(region_id)
    return data.get("shelters", [])

@router.get("/{shelter_id}", response_model=ShelterInfo)
def get_shelter_by_id(shelter_id: str, region_id: str = "kerala_ernakulam"):
    """
    Retrieve live logistics metrics for a single designated shelter.
    """
    data = get_region_data(region_id)
    shelter = next((s for s in data.get("shelters", []) if s["id"] == shelter_id), None)
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return shelter
