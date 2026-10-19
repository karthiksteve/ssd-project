"""
Dynamic Spatial Routing API Endpoints.
Calculates risk-aware evacuation paths comparing:
1. Standard Shortest Route (unaware of flood hazards, prone to submerged traps)
2. RescuePath AI Safe Route (A* algorithm navigating around DBSCAN clusters and lowlands)
"""

from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import (
    RouteRequest,
    EvacuationRoutingResponse
)
from backend.app.database.seed_data import get_region_data
from backend.app.core.graph_router import graph_router
from backend.app.core.scenario_simulator import scenario_simulator

router = APIRouter(prefix="/api/routing", tags=["Dynamic Evacuation Routing"])

@router.post("/evacuate", response_model=EvacuationRoutingResponse)
def compute_evacuation_path(payload: RouteRequest):
    """
    Calculate dynamic evacuation path from user GPS location to safe shelter.
    Compares standard shortest route vs AI-optimized safe corridor.
    """
    sim_status = scenario_simulator.get_status(payload.region_id)
    surge_active = sim_status.get("surge_active", False)

    try:
        routing_result = graph_router.compute_evacuation_routes(
            region_id=payload.region_id,
            start_lat=payload.start_lat,
            start_lng=payload.start_lng,
            shelter_id=payload.shelter_id,
            flood_surge_active=surge_active
        )
        return routing_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing calculation error: {str(e)}")

@router.get("/road-network")
def get_road_network_topology(region_id: str = "kerala_ernakulam"):
    """
    Returns the full road network graph vertices and segments for GIS visualization.
    """
    data = get_region_data(region_id)
    nodes = data["nodes"]
    edges = data["edges"]

    edge_lines = []
    for u, v, attrs in edges:
        if u in nodes and v in nodes:
            edge_lines.append({
                "from_node": u,
                "to_node": v,
                "road_name": attrs["road"],
                "length_km": attrs["length_km"],
                "speed_kmh": attrs["speed_kmh"],
                "hazard_factor": attrs.get("hazard_factor", 0.0),
                "coordinates": [
                    [nodes[u]["lng"], nodes[u]["lat"]],
                    [nodes[v]["lng"], nodes[v]["lat"]]
                ]
            })

    return {
        "region_id": region_id,
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "nodes": list(nodes.values()),
        "edges": edge_lines
    }
