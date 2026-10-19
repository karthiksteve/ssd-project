"""
RescuePath AI - Main FastAPI Application.
Production-grade disaster response and evacuation platform using Sequential & Spatial Data Mining.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.sequential_routes import router as sequential_router
from backend.app.api.spatial_routes import router as spatial_router
from backend.app.api.routing_routes import router as routing_router
from backend.app.api.shelter_routes import router as shelter_router
from backend.app.api.simulation_routes import router as simulation_router
from backend.app.api.export_routes import router as export_router
from backend.app.database.seed_data import REGIONS_METADATA

app = FastAPI(
    title="RescuePath AI - Sequential & Spatial Data Mining Platform",
    description=(
        "Intelligent Disaster Response and Evacuation Platform for flood crisis management in India. "
        "Integrates multi-step sequential prediction (24h/48h/72h), spatial hazard clustering (DBSCAN & KDE), "
        "and risk-penalized A* evacuation pathfinding on road network graphs."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local React/Vite development and production access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(sequential_router)
app.include_router(spatial_router)
app.include_router(routing_router)
app.include_router(shelter_router)
app.include_router(simulation_router)
app.include_router(export_router)

@app.get("/")
def root():
    return {
        "platform": "RescuePath AI",
        "course": "CSE3068 Sequential and Spatial Data Mining",
        "status": "OPERATIONAL",
        "docs": "/docs",
        "supported_regions": list(REGIONS_METADATA.keys())
    }

@app.get("/api/regions")
def get_regions():
    """Returns available disaster analysis basins."""
    return list(REGIONS_METADATA.values())

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "RescuePath AI Backend"}
