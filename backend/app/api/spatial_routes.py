"""
Spatial Data Mining API Endpoints.
Exposes:
- ST-DBSCAN hazard clustering & convex hull boundaries
- 2D Kernel Density Estimation (KDE) risk raster surface
- Moran's I spatial autocorrelation evaluation
"""

from fastapi import APIRouter, Query
from backend.app.schemas.pydantic_models import (
    SpatialMiningResponse,
    KDERiskGridResponse
)
from backend.app.database.seed_data import get_region_data
from backend.app.core.spatial_miner import spatial_miner
from backend.app.core.scenario_simulator import scenario_simulator

router = APIRouter(prefix="/api/spatial", tags=["Spatial Data Mining"])

@router.get("/clusters", response_model=SpatialMiningResponse)
def get_spatial_clusters(
    region_id: str = "kerala_ernakulam",
    eps_km: float = Query(default=1.8, description="DBSCAN epsilon radius in kilometers"),
    min_samples: int = Query(default=3, description="DBSCAN min points to form a cluster")
):
    """
    Run DBSCAN clustering on spatial flood incident points and water sensors.
    Identifies high-density hazard zones and filters out isolated noise reports.
    Computes Moran's I spatial autocorrelation.
    """
    data = get_region_data(region_id)
    sensors = [dict(s) for s in data["sensors"]]

    # Adjust water depth if surge simulation is active
    sim_status = scenario_simulator.get_status(region_id)
    if sim_status.get("surge_active"):
        mult = sim_status.get("intensity", 1.5)
        for s in sensors:
            s["water_depth_cm"] = int(s["water_depth_cm"] * mult)

    cluster_result = spatial_miner.run_dbscan_clustering(
        sensors,
        eps_km=eps_km,
        min_samples=min_samples
    )

    return SpatialMiningResponse(
        region_id=region_id,
        total_incidents=cluster_result["total_incidents"],
        num_clusters=cluster_result["num_clusters"],
        noise_points_count=cluster_result["noise_points_count"],
        spatial_autocorrelation_morans_i=cluster_result["spatial_autocorrelation_morans_i"],
        p_value=cluster_result["p_value"],
        spatial_pattern=cluster_result["spatial_pattern"],
        clusters=cluster_result["clusters"],
        points=cluster_result["points"]
    )

@router.get("/kde-grid", response_model=KDERiskGridResponse)
def get_kde_risk_grid(
    region_id: str = "kerala_ernakulam",
    resolution: int = Query(default=25, ge=10, le=50)
):
    """
    Compute 2D Gaussian Kernel Density Estimation (KDE) flood risk surface.
    Returns normalized matrix [0.0 to 1.0] for live heatmap visualization.
    """
    data = get_region_data(region_id)
    sensors = data["sensors"]
    kde_result = spatial_miner.compute_kde_risk_grid(sensors, resolution=resolution)

    return KDERiskGridResponse(
        region_id=region_id,
        bounds=kde_result["bounds"],
        resolution=kde_result["resolution"],
        grid=kde_result["grid"]
    )

@router.get("/river-geometry")
def get_river_geometry(region_id: str = "kerala_ernakulam"):
    """
    Returns the GeoJSON line coordinates of the primary river channel.
    """
    data = get_region_data(region_id)
    return {
        "region_id": region_id,
        "river_name": data["metadata"]["river_name"],
        "geojson": {
            "type": "LineString",
            "coordinates": data["river"]
        }
    }
