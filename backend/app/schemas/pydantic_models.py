from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Sequential Data Mining Schemas ---
class SequentialPredictionRequest(BaseModel):
    region_id: str = "kerala_ernakulam"
    rainfall_sequence: Optional[List[float]] = Field(
        default=None, 
        description="Sequential rainfall measurements over past intervals (mm/hour)"
    )
    upstream_discharge: Optional[float] = Field(
        default=None, 
        description="Current upstream dam/river discharge in cumecs (m^3/s)"
    )
    soil_saturation: Optional[float] = Field(
        default=None, 
        description="Soil moisture saturation index [0.0 to 1.0]"
    )

class ForecastStep(BaseModel):
    horizon_hours: int
    flood_probability: float
    risk_level: str  # LOW, MODERATE, HIGH, SEVERE
    expected_river_level_m: float
    warning_flag: bool
    driving_factors: List[str]

class SequentialPredictionResponse(BaseModel):
    region_id: str
    current_time: str
    status: str
    forecast_24h: ForecastStep
    forecast_48h: ForecastStep
    forecast_72h: ForecastStep
    sequence_trend: str
    historical_sequence: List[Dict[str, Any]]
    confidence_score: float

# --- Spatial Data Mining Schemas ---
class SpatialClusterRequest(BaseModel):
    region_id: str = "kerala_ernakulam"
    eps_km: float = Field(default=1.8, description="DBSCAN spatial epsilon in kilometers")
    min_samples: int = Field(default=3, description="DBSCAN min points to form a core cluster")
    temporal_window_hours: Optional[float] = Field(default=24.0, description="Temporal window for ST-DBSCAN")

class ClusterPoint(BaseModel):
    id: str
    lat: float
    lng: float
    water_depth_cm: float
    severity: str
    source: Optional[str] = None
    timestamp: Optional[str] = None

class ClusterPolygon(BaseModel):
    cluster_id: int
    hazard_level: str
    centroid: Dict[str, float]
    radius_km: float
    points_count: int
    avg_water_depth_cm: float
    hull_coordinates: List[List[float]]  # GeoJSON style [[lng, lat], ...]

class SpatialMiningResponse(BaseModel):
    region_id: str
    total_incidents: int
    num_clusters: int
    noise_points_count: int
    spatial_autocorrelation_morans_i: float
    p_value: float
    spatial_pattern: str  # e.g., "Significantly Clustered (p < 0.01)"
    clusters: List[ClusterPolygon]
    points: List[ClusterPoint]

class KDERiskGridResponse(BaseModel):
    region_id: str
    bounds: Dict[str, float]
    resolution: int
    grid: List[List[float]]  # 2D matrix of risk intensity [0.0 - 1.0]

# --- Routing Schemas ---
class RouteRequest(BaseModel):
    region_id: str = "kerala_ernakulam"
    start_lat: float
    start_lng: float
    shelter_id: Optional[str] = None  # If None, automatically allocates optimal safe shelter
    avoid_high_risk: bool = True
    risk_penalty_factor: float = Field(default=5.0, description="Risk penalty multiplier in A* cost function")

class RouteWaypoint(BaseModel):
    lat: float
    lng: float
    road_name: str
    step_hazard_score: float
    elevation_m: float

class EvacuationRouteDetails(BaseModel):
    route_type: str  # "rescuepath_safe" or "standard_shortest"
    is_safe: bool
    total_distance_km: float
    estimated_time_min: float
    risk_exposure_score: float
    submerged_segments_encountered: int
    waypoints: List[RouteWaypoint]
    geojson_line: Dict[str, Any]
    safety_summary: str

class EvacuationRoutingResponse(BaseModel):
    region_id: str
    start_location: Dict[str, float]
    target_shelter: Dict[str, Any]
    safe_route: EvacuationRouteDetails
    standard_route: EvacuationRouteDetails
    risk_reduction_percentage: float
    travel_time_difference_min: float
    recommendation: str

# --- Shelter Schemas ---
class ShelterInfo(BaseModel):
    id: str
    name: str
    region_id: str
    lat: float
    lng: float
    total_capacity: int
    current_occupancy: int
    available_beds: int
    status: str  # OPEN, NEAR_CAPACITY, FULL
    elevation_m: float
    food_packs_available: int
    medical_staff_present: bool
    generator_active: bool
    contact_phone: str

# --- Simulation Schemas ---
class SimulationTriggerRequest(BaseModel):
    region_id: str = "kerala_ernakulam"
    scenario: str = Field(
        default="dam_gate_release",
        description="Scenario type: 'monsoon_surge', 'dam_gate_release', 'flash_flood', or 'receding'"
    )
    intensity: float = Field(default=1.5, ge=0.5, le=3.0, description="Severity multiplier")

class SimulationResponse(BaseModel):
    scenario: str
    region_id: str
    applied_multiplier: float
    message: str
    new_active_clusters: int
    critical_roads_severed: List[str]
    forecast_updated: Dict[str, Any]
