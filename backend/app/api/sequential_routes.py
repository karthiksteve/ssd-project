"""
Sequential Data Mining API Endpoints.
Provides 24h, 48h, 72h flood risk forecasts based on sequence-to-sequence temporal modeling.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from backend.app.schemas.pydantic_models import (
    SequentialPredictionRequest,
    SequentialPredictionResponse
)
from backend.app.database.seed_data import get_region_data
from backend.app.core.sequential_miner import sequential_miner
from backend.app.core.scenario_simulator import scenario_simulator

router = APIRouter(prefix="/api/sequential", tags=["Sequential Data Mining"])

@router.get("/predict", response_model=SequentialPredictionResponse)
def get_sequential_prediction(region_id: str = "kerala_ernakulam"):
    """
    Get multi-step sequential flood prediction for 24h, 48h, and 72h horizons.
    Uses historical time-series sequences of precipitation, river discharge, and soil saturation.
    """
    data = get_region_data(region_id)
    sequence = data.get("sequence", [])
    
    # Check if active simulation alters current surge
    sim_status = scenario_simulator.get_status(region_id)
    multiplier = sim_status.get("intensity", 1.0) if sim_status.get("surge_active") else 1.0

    forecast_data = sequential_miner.predict_multi_step_horizon(sequence, surge_multiplier=multiplier)

    return SequentialPredictionResponse(
        region_id=region_id,
        current_time=datetime.now(timezone.utc).isoformat(),
        status="ACTIVE_MONITORING",
        forecast_24h=forecast_data["forecast_24h"],
        forecast_48h=forecast_data["forecast_48h"],
        forecast_72h=forecast_data["forecast_72h"],
        sequence_trend=forecast_data["sequence_trend"],
        historical_sequence=sequence,
        confidence_score=forecast_data["confidence_score"]
    )

@router.post("/predict_custom", response_model=SequentialPredictionResponse)
def post_custom_sequential_prediction(payload: SequentialPredictionRequest):
    """
    Allows custom sequence inputs to test hypothesis or hypothetical rainfall curves.
    """
    data = get_region_data(payload.region_id)
    sequence = data.get("sequence", []).copy()

    # If custom rainfall array is provided, adapt sequence
    if payload.rainfall_sequence:
        sequence = []
        for i, val in enumerate(payload.rainfall_sequence):
            sequence.append({
                "hour_step": - (len(payload.rainfall_sequence) - i) * 6,
                "rainfall_mm": float(val),
                "discharge_cumecs": payload.upstream_discharge or 1200.0,
                "soil_sat": payload.soil_saturation or 0.85,
                "river_level_m": 6.0 + (val / 50.0)
            })

    forecast_data = sequential_miner.predict_multi_step_horizon(sequence)

    return SequentialPredictionResponse(
        region_id=payload.region_id,
        current_time=datetime.now(timezone.utc).isoformat(),
        status="CUSTOM_HYPOTHESIS_SIMULATION",
        forecast_24h=forecast_data["forecast_24h"],
        forecast_48h=forecast_data["forecast_48h"],
        forecast_72h=forecast_data["forecast_72h"],
        sequence_trend=forecast_data["sequence_trend"],
        historical_sequence=sequence,
        confidence_score=forecast_data["confidence_score"]
    )
