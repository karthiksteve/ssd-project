"""
RescuePath AI - Emergency Evacuation Dispatch & Data Export API.
Generates printable disaster response manifests and CSV data exports for emergency responders.
"""

from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse
from typing import Optional
from datetime import datetime, timezone
import io
import csv
from backend.app.database.seed_data import get_region_data
from backend.app.core.graph_router import graph_router
from backend.app.core.scenario_simulator import scenario_simulator

router = APIRouter(prefix="/api/export", tags=["Emergency Dispatch & Data Export"])

@router.get("/dispatch-manifest")
def generate_dispatch_manifest(
    region_id: str = Query("kerala_ernakulam", description="Disaster basin ID"),
    start_lat: float = Query(..., description="Evacuee latitude"),
    start_lng: float = Query(..., description="Evacuee longitude"),
    shelter_id: Optional[str] = Query(None, description="Optional designated shelter ID"),
    download: bool = Query(False, description="Whether to trigger file download attachment")
):
    """
    Generates an official Emergency Evacuation Dispatch Manifest
    with turn-by-turn guidance, hazard bypass analytics, and shelter logistics.
    """
    data = get_region_data(region_id)
    sim_status = scenario_simulator.get_status(region_id)
    surge_active = sim_status.get("surge_active", False)

    try:
        routes = graph_router.compute_evacuation_routes(
            region_id=region_id,
            start_lat=start_lat,
            start_lng=start_lng,
            shelter_id=shelter_id,
            flood_surge_active=surge_active
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing calculation failed: {str(e)}")

    safe = routes["safe_route"]
    std = routes["standard_route"]
    shelter = routes["target_shelter"]
    region_meta = data["metadata"]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Build formatted Markdown manifest
    lines = [
        "=" * 76,
        "   NATIONAL DISASTER MANAGEMENT AUTHORITY (NDMA) / STATE DISASTER RESPONSE",
        "         EMERGENCY EVACUATION DISPATCH MANIFEST — RESCUEPATH AI",
        "=" * 76,
        f"Issued: {timestamp} | Basin: {region_meta['name']}",
        f"Evacuee Origin GPS : {start_lat:.5f}°N, {start_lng:.5f}°E",
        f"Surge Status       : {'CRITICAL ACTIVE SURGE' if surge_active else 'MONITORED PEAK STAGE'}",
        "-" * 76,
        "",
        "1. DESIGNATED RELIEF DESTINATION",
        f"   Shelter Name      : {shelter['name']}",
        f"   Elevation         : {shelter['elevation_m']} m (Flood High Ground)",
        f"   Capacity Status   : {shelter['current_occupancy']} / {shelter['total_capacity']} ({shelter['status']})",
        f"   Available Beds    : {shelter['available_beds']}",
        f"   Food Supplies     : {shelter['food_packs_available']} Emergency Rations",
        f"   Medical Officer   : {'On Site' if shelter['medical_staff_present'] else 'En Route'}",
        f"   Emergency Power   : {'Generator Active' if shelter['generator_active'] else 'Grid'}",
        f"   Emergency Contact : {shelter['contact_phone']}",
        "",
        "2. EVACUATION CORRIDOR SUMMARY & RISK REDUCTION",
        f"   Optimal Corridor  : RescuePath AI Safe Path (Risk-Penalized A*)",
        f"   Total Safe Distance: {safe['total_distance_km']:.2f} km",
        f"   Estimated Transit : {safe['estimated_time_min']:.1f} minutes",
        f"   Risk Exposure     : {safe['risk_exposure_score']:.2f} / 1.00",
        f"   Flood Risk Avoided: {routes['risk_reduction_percentage']:.1f}% vs Shortest Path",
        f"   Time Trade-off    : +{routes['travel_time_difference_min']:.1f} mins detour to bypass deep floodwater",
        "",
        "3. HAZARD CONTRAST (STANDARD SHORTEST PATH WARNING)",
        f"   Standard Route    : {std['total_distance_km']:.2f} km | {std['estimated_time_min']:.1f} mins",
        f"   Standard Risk     : {std['risk_exposure_score']:.2f} / 1.00 (HIGH DANGER)",
        f"   Submerged Links   : {std['submerged_segments_encountered']} impassable flooded corridor(s)",
        "   WARNING: Direct shortest route traverses severely flooded lowlands. DO NOT TAKE.",
        "",
        "4. STEP-BY-STEP WAYPOINT NAVIGATION GUIDANCE",
        f"{'Step':<5} | {'Road Corridor':<36} | {'Elev':<6} | {'Hazard':<8} | {'Status'}",
        "-" * 76
    ]

    for idx, wp in enumerate(safe["waypoints"], 1):
        status = "CRITICAL HAZARD" if wp["step_hazard_score"] > 0.6 else ("ELEVATED" if wp["step_hazard_score"] > 0.3 else "CLEAR/SAFE")
        lines.append(
            f"{idx:<5} | {wp['road_name'][:36]:<36} | {wp['elevation_m']:>4.1f}m | {wp['step_hazard_score']:>6.2f} | {status}"
        )

    lines.extend([
        "-" * 76,
        "",
        "5. NDMA CITIZEN FLOOD SAFETY PROTOCOLS",
        "   - Do NOT attempt to walk, swim, or drive through moving water above 15 cm.",
        "   - Pack waterproof emergency bag: ID cards, dry food, medications, flashlight.",
        "   - Turn off domestic main gas valves and electric circuit breakers before leaving.",
        "   - Follow designated glowing green route markers on the RescuePath AI app.",
        "   - State Disaster Control Room Toll-Free Emergency Helpline: 1077 or 112.",
        "=" * 76,
        "   END OF DISPATCH MANIFEST — RESCUEPATH AI AUTOMATED DISASTER DISPATCH"
    ])

    manifest_text = "\n".join(lines)

    headers = {}
    if download:
        filename = f"evacuation_manifest_{region_id}_{int(datetime.now(timezone.utc).timestamp())}.txt"
        headers["Content-Disposition"] = f'attachment; filename="{filename}"'

    return PlainTextResponse(content=manifest_text, media_type="text/plain; charset=utf-8", headers=headers)

@router.get("/shelters-csv")
def export_shelters_csv(region_id: Optional[str] = None):
    """
    Exports live relief shelters registry as a CSV download.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "name", "region_id", "lat", "lng", "elevation_m",
        "total_capacity", "current_occupancy", "available_beds",
        "status", "food_packs_available", "medical_staff_present",
        "generator_active", "contact_phone"
    ])

    regions_to_export = [region_id] if region_id else ["kerala_ernakulam", "assam_guwahati"]
    for reg in regions_to_export:
        data = get_region_data(reg)
        for s in data["shelters"]:
            writer.writerow([
                s["id"], s["name"], s["region_id"], s["lat"], s["lng"], s["elevation_m"],
                s["total_capacity"], s["current_occupancy"], s["available_beds"],
                s["status"], s["food_packs_available"], s["medical_staff_present"],
                s["generator_active"], s["contact_phone"]
            ])

    filename = f"shelters_{region_id or 'all_regions'}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.get("/sensors-csv")
def export_sensors_csv(region_id: str = "kerala_ernakulam"):
    """
    Exports sensor telemetry data as a CSV download.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "lat", "lng", "water_depth_cm", "severity", "sos_calls", "source"])

    data = get_region_data(region_id)
    for s in data["sensors"]:
        writer.writerow([
            s.get("id"),
            s.get("name", s.get("source", "Telemetry Point")),
            s.get("lat"),
            s.get("lng"),
            s.get("water_depth_cm"),
            s.get("severity"),
            s.get("sos_calls", 0),
            s.get("source", "iot_telemetry")
        ])

    filename = f"telemetry_sensors_{region_id}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.get("/timeseries-csv")
def export_timeseries_csv(region_id: str = "kerala_ernakulam"):
    """
    Exports 72-hour hydro-meteorological sequence as a CSV download.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["hour_step", "rainfall_mm", "discharge_cumecs", "soil_sat", "river_level_m", "danger_mark_m"])

    data = get_region_data(region_id)
    danger_m = data["metadata"]["danger_threshold_m"]
    for row in data["sequence"]:
        writer.writerow([
            row["hour_step"],
            row["rainfall_mm"],
            row["discharge_cumecs"],
            row["soil_sat"],
            row["river_level_m"],
            danger_m
        ])

    filename = f"hydrology_timeseries_{region_id}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
