"""
Simulation API Endpoints.
Allows operators and evaluators to trigger disaster scenarios:
- Dam Gate Release (e.g. Idamalayar/Idukki)
- Extreme Monsoon Cloudburst
- Flash Flood Event
- Receding Flood Recovery
"""

from fastapi import APIRouter
from backend.app.schemas.pydantic_models import (
    SimulationTriggerRequest,
    SimulationResponse
)
from backend.app.core.scenario_simulator import scenario_simulator

router = APIRouter(prefix="/api/simulation", tags=["Disaster Simulation"])

@router.post("/trigger", response_model=SimulationResponse)
def trigger_disaster_scenario(payload: SimulationTriggerRequest):
    """
    Simulate a disaster surge or flood condition in real time.
    """
    res = scenario_simulator.trigger_scenario(
        region_id=payload.region_id,
        scenario=payload.scenario,
        intensity=payload.intensity
    )
    return SimulationResponse(**res)

@router.get("/status")
def get_simulation_status(region_id: str = "kerala_ernakulam"):
    """
    Check current active simulation condition.
    """
    return scenario_simulator.get_status(region_id)
