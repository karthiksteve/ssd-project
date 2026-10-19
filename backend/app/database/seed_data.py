"""
Seed geographic datasets and network models for RescuePath AI.
Calibrated to real-world flood topologies:
1. Kerala - Ernakulam / Aluva / Periyar River Basin (2018/2024 Flood Scenario)
2. Assam - Guwahati / Brahmaputra River Basin
"""

from typing import Dict, List, Any
import math

REGIONS_METADATA = {
    "kerala_ernakulam": {
        "id": "kerala_ernakulam",
        "name": "Kerala - Ernakulam (Periyar River Basin / Aluva)",
        "center": {"lat": 10.1076, "lng": 76.3516},
        "zoom": 13,
        "danger_threshold_m": 7.5,
        "extreme_threshold_m": 9.2,
        "description": "High-risk alluvial basin vulnerable to Periyar River dam releases (Idamalayar & Idukki) and monsoon cloudbursts.",
        "river_name": "Periyar River",
        "district": "Ernakulam",
        "state": "Kerala"
    },
    "assam_guwahati": {
        "id": "assam_guwahati",
        "name": "Assam - Guwahati (Brahmaputra River Basin)",
        "center": {"lat": 26.1850, "lng": 91.7550},
        "zoom": 13,
        "danger_threshold_m": 49.6,
        "extreme_threshold_m": 51.5,
        "description": "Recurrent severe flood zone along the Brahmaputra with urban inundation and riverbank erosion.",
        "river_name": "Brahmaputra River",
        "district": "Kamrup Metropolitan",
        "state": "Assam"
    }
}

# --- KERALA ERNAKULAM / ALUVA SEED DATA ---

KERALA_RIVER_COORDINATES = [
    [76.3950, 10.1500], # Upstream Malayattoor/Kalady
    [76.3800, 10.1380],
    [76.3650, 10.1220],
    [76.3540, 10.1110], # Aluva Manappuram
    [76.3450, 10.1060], # Aluva Railway bridge bend
    [76.3350, 10.0980], # Mangalapuzha branch split
    [76.3150, 10.0910], # Eloor industrial reach
    [76.2900, 10.0820], # Varapuzha downstream
    [76.2700, 10.0750]  # Toward Arabian Sea estuary
]

KERALA_SHELTERS: List[Dict[str, Any]] = [
    {
        "id": "shelter_kerala_1",
        "name": "UC College High Ground Relief Center",
        "region_id": "kerala_ernakulam",
        "lat": 10.1255,
        "lng": 76.3360,
        "elevation_m": 26.5,
        "total_capacity": 650,
        "current_occupancy": 320,
        "available_beds": 330,
        "status": "OPEN",
        "food_packs_available": 1200,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-484-260-3101"
    },
    {
        "id": "shelter_kerala_2",
        "name": "Kalamassery Community Operations Shelter",
        "region_id": "kerala_ernakulam",
        "lat": 10.0530,
        "lng": 76.3210,
        "elevation_m": 31.0,
        "total_capacity": 800,
        "current_occupancy": 410,
        "available_beds": 390,
        "status": "OPEN",
        "food_packs_available": 1800,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-484-254-8890"
    },
    {
        "id": "shelter_kerala_3",
        "name": "Rajagiri Disaster Response Camp, Kakkanad",
        "region_id": "kerala_ernakulam",
        "lat": 10.0120,
        "lng": 76.3580,
        "elevation_m": 38.0,
        "total_capacity": 950,
        "current_occupancy": 210,
        "available_beds": 740,
        "status": "OPEN",
        "food_packs_available": 2400,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-484-291-1122"
    },
    {
        "id": "shelter_kerala_4",
        "name": "Angamaly St. Joseph Evacuation Hub",
        "region_id": "kerala_ernakulam",
        "lat": 10.1880,
        "lng": 76.3860,
        "elevation_m": 34.0,
        "total_capacity": 500,
        "current_occupancy": 465,
        "available_beds": 35,
        "status": "NEAR_CAPACITY",
        "food_packs_available": 400,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-484-245-0909"
    }
]

# Real road network nodes across Aluva - Ernakulam corridor
KERALA_ROAD_NODES: Dict[str, Dict[str, Any]] = {
    "N1": {"id": "N1", "name": "Aluva Manappuram Temple Area (Low Basin)", "lat": 10.1085, "lng": 76.3535, "elev": 4.5, "base_hazard": 0.85},
    "N2": {"id": "N2", "name": "Aluva Railway Station / Bus Stand", "lat": 10.1090, "lng": 76.3580, "elev": 9.2, "base_hazard": 0.65},
    "N3": {"id": "N3", "name": "NH 544 Aluva Bridge Junction", "lat": 10.1050, "lng": 76.3510, "elev": 7.0, "base_hazard": 0.80},
    "N4": {"id": "N4", "name": "Bank Junction / Subhash Park", "lat": 10.1070, "lng": 76.3450, "elev": 11.5, "base_hazard": 0.40},
    "N5": {"id": "N5", "name": "Aluva Bypass / Paravur Kavala", "lat": 10.1150, "lng": 76.3480, "elev": 14.0, "base_hazard": 0.30},
    "N6": {"id": "N6", "name": "UC College Junction (Elevated)", "lat": 10.1240, "lng": 76.3370, "elev": 25.0, "base_hazard": 0.05},
    "N7": {"id": "N7", "name": "Muttom Metro Station / Highway", "lat": 10.0780, "lng": 76.3380, "elev": 13.0, "base_hazard": 0.25},
    "N8": {"id": "N8", "name": "Companypady / Ambattukavu", "lat": 10.0680, "lng": 76.3310, "elev": 16.0, "base_hazard": 0.15},
    "N9": {"id": "N9", "name": "Kalamassery Premier Junction", "lat": 10.0540, "lng": 76.3240, "elev": 29.0, "base_hazard": 0.02},
    "N10": {"id": "N10", "name": "Eloor Ferry Road (Submerged Zone)", "lat": 10.0890, "lng": 76.3210, "elev": 5.2, "base_hazard": 0.90},
    "N11": {"id": "N11", "name": "Kuttamassery / Thottakkattukara", "lat": 10.1190, "lng": 76.3630, "elev": 12.0, "base_hazard": 0.35},
    "N12": {"id": "N12", "name": "Choornikkara Safe Bypass", "lat": 10.0920, "lng": 76.3560, "elev": 18.0, "base_hazard": 0.10},
    "N13": {"id": "N13", "name": "Seaport-Airport Link High Corridor", "lat": 10.0410, "lng": 76.3500, "elev": 33.0, "base_hazard": 0.01},
    "N14": {"id": "N14", "name": "Kakkanad Civil Station Ridge", "lat": 10.0140, "lng": 76.3560, "elev": 39.0, "base_hazard": 0.00}
}

# Road segments (edges) with length (km), road name, and capacity
KERALA_ROAD_EDGES = [
    # Manappuram to Railway Station (Elevated high-water ramp - safe detour)
    ("N1", "N2", {"road": "Manappuram Elevated Evacuation Ramp", "length_km": 0.90, "speed_kmh": 35, "hazard_factor": 0.15}),
    # Manappuram to NH Bridge (Low-level submerged riverbank causeway - short but impassable in floods)
    ("N1", "N3", {"road": "Periyar Riverbank Submerged Causeway", "length_km": 0.45, "speed_kmh": 40, "hazard_factor": 0.95}),
    # Railway station to Bank Junction
    ("N2", "N4", {"road": "Railway Square Road", "length_km": 1.45, "speed_kmh": 35, "hazard_factor": 0.45}),
    # NH Bridge to Bank Junction
    ("N3", "N4", {"road": "Old Bridge Approach", "length_km": 0.70, "speed_kmh": 40, "hazard_factor": 0.60}),
    # Bank Junction to Paravur Kavala
    ("N4", "N5", {"road": "Paravur Road Bypass", "length_km": 1.10, "speed_kmh": 45, "hazard_factor": 0.25}),
    # Paravur Kavala to UC College (Safe high ground corridor)
    ("N5", "N6", {"road": "UC College Elevated Avenue", "length_km": 1.60, "speed_kmh": 50, "hazard_factor": 0.05}),
    # NH Bridge to Muttom along NH 544 (Heavy traffic, moderate flood risk)
    ("N3", "N7", {"road": "NH 544 Highway Corridor", "length_km": 3.40, "speed_kmh": 55, "hazard_factor": 0.50}),
    # Bank junction through Eloor (Flooded industrial sector)
    ("N4", "N10", {"road": "Eloor Industrial Access", "length_km": 2.90, "speed_kmh": 30, "hazard_factor": 0.90}),
    ("N10", "N8", {"road": "Eloor-Ambattukavu Link", "length_km": 2.50, "speed_kmh": 35, "hazard_factor": 0.75}),
    # Muttom to Ambattukavu
    ("N7", "N8", {"road": "Metro Viaduct Highway", "length_km": 1.30, "speed_kmh": 45, "hazard_factor": 0.20}),
    # Ambattukavu to Kalamassery
    ("N8", "N9", {"road": "Premier Junction Access", "length_km": 1.80, "speed_kmh": 50, "hazard_factor": 0.05}),
    # Safe East Bypass (Choornikkara corridor)
    ("N2", "N11", {"road": "Kuttamassery Road", "length_km": 1.35, "speed_kmh": 40, "hazard_factor": 0.25}),
    ("N11", "N12", {"road": "East Choornikkara Safe Ridge", "length_km": 2.40, "speed_kmh": 45, "hazard_factor": 0.10}),
    ("N12", "N7", {"road": "Muttom East Link", "length_km": 2.20, "speed_kmh": 45, "hazard_factor": 0.15}),
    # Kalamassery to Seaport-Airport link to Kakkanad
    ("N9", "N13", {"road": "HMT - Seaport Expressway", "length_km": 3.10, "speed_kmh": 60, "hazard_factor": 0.02}),
    ("N13", "N14", {"road": "Kakkanad InfoPark Highway", "length_km": 3.60, "speed_kmh": 60, "hazard_factor": 0.00})
]

# Flood incident & telemetry sensor points for Spatial Mining (DBSCAN + KDE)
KERALA_SENSOR_INCIDENTS = [
    {"id": "inc_01", "lat": 10.1082, "lng": 76.3530, "water_depth_cm": 140, "severity": "CRITICAL", "source": "River Gauge S1 - Manappuram"},
    {"id": "inc_02", "lat": 10.1075, "lng": 76.3512, "water_depth_cm": 115, "severity": "CRITICAL", "source": "Highway Underpass CWC"},
    {"id": "inc_03", "lat": 10.1060, "lng": 76.3498, "water_depth_cm": 95, "severity": "HIGH", "source": "Citizen SOS Call #104"},
    {"id": "inc_04", "lat": 10.1095, "lng": 76.3545, "water_depth_cm": 125, "severity": "CRITICAL", "source": "Aluva Ghat Sensor"},
    {"id": "inc_05", "lat": 10.1042, "lng": 76.3520, "water_depth_cm": 85, "severity": "HIGH", "source": "Police Control Van #3"},
    # Eloor industrial cluster
    {"id": "inc_06", "lat": 10.0895, "lng": 76.3215, "water_depth_cm": 130, "severity": "CRITICAL", "source": "Eloor Ferry Flood Gauge"},
    {"id": "inc_07", "lat": 10.0910, "lng": 76.3230, "water_depth_cm": 105, "severity": "HIGH", "source": "Industrial Estate Sensor #7"},
    {"id": "inc_08", "lat": 10.0880, "lng": 76.3200, "water_depth_cm": 145, "severity": "CRITICAL", "source": "Eloor Lowland Monitoring"},
    # Varapuzha downstream cluster
    {"id": "inc_09", "lat": 10.0815, "lng": 76.2920, "water_depth_cm": 90, "severity": "HIGH", "source": "Varapuzha Bridge Post"},
    {"id": "inc_10", "lat": 10.0830, "lng": 76.2950, "water_depth_cm": 80, "severity": "MODERATE", "source": "Panchayat Distress Alert"},
    {"id": "inc_11", "lat": 10.0805, "lng": 76.2890, "water_depth_cm": 110, "severity": "HIGH", "source": "NDRF Survey Boat #2"},
    # Isolated noise points (tested by DBSCAN to ensure noise filtering works)
    {"id": "inc_noise1", "lat": 10.1350, "lng": 76.3680, "water_depth_cm": 25, "severity": "LOW", "source": "Minor Waterlogging Report"},
    {"id": "inc_noise2", "lat": 10.0350, "lng": 76.3350, "water_depth_cm": 20, "severity": "LOW", "source": "Drain Overflow Call"}
]

# Baseline historical sequential rainfall time series (past 7 days in 6h intervals)
# Features: [timestamp_hour, rainfall_mm, upstream_dam_discharge_cumecs, soil_saturation_ratio]
KERALA_HISTORICAL_SEQUENCE = [
    {"hour_step": -72, "rainfall_mm": 12.5, "discharge_cumecs": 450, "soil_sat": 0.58, "river_level_m": 4.8},
    {"hour_step": -66, "rainfall_mm": 18.0, "discharge_cumecs": 520, "soil_sat": 0.62, "river_level_m": 5.1},
    {"hour_step": -60, "rainfall_mm": 24.2, "discharge_cumecs": 610, "soil_sat": 0.67, "river_level_m": 5.5},
    {"hour_step": -54, "rainfall_mm": 35.8, "discharge_cumecs": 740, "soil_sat": 0.72, "river_level_m": 6.0},
    {"hour_step": -48, "rainfall_mm": 48.0, "discharge_cumecs": 920, "soil_sat": 0.78, "river_level_m": 6.6},
    {"hour_step": -42, "rainfall_mm": 62.5, "discharge_cumecs": 1150, "soil_sat": 0.84, "river_level_m": 7.3},
    {"hour_step": -36, "rainfall_mm": 88.0, "discharge_cumecs": 1420, "soil_sat": 0.89, "river_level_m": 8.1}, # Exceeds Danger Level (7.5m)
    {"hour_step": -30, "rainfall_mm": 104.2, "discharge_cumecs": 1780, "soil_sat": 0.93, "river_level_m": 8.8},
    {"hour_step": -24, "rainfall_mm": 122.0, "discharge_cumecs": 2100, "soil_sat": 0.96, "river_level_m": 9.4},
    {"hour_step": -18, "rainfall_mm": 115.5, "discharge_cumecs": 2250, "soil_sat": 0.98, "river_level_m": 9.6},
    {"hour_step": -12, "rainfall_mm": 98.0, "discharge_cumecs": 2180, "soil_sat": 0.97, "river_level_m": 9.3},
    {"hour_step": -6,  "rainfall_mm": 85.0, "discharge_cumecs": 1980, "soil_sat": 0.96, "river_level_m": 8.9},
    {"hour_step": 0,   "rainfall_mm": 74.0, "discharge_cumecs": 1820, "soil_sat": 0.95, "river_level_m": 8.6}
]

# --- ASSAM GUWAHATI / BRAHMAPUTRA SEED DATA ---

ASSAM_RIVER_COORDINATES = [
    [91.8100, 26.2080], # Upstream Kharghuli hills
    [91.7850, 26.1980], # Uzanbazar River Ghat
    [91.7600, 26.1900], # Sukreswar Ghat / Panbazar
    [91.7450, 26.1840], # Bharalumukh (River Confluence)
    [91.7250, 26.1760], # Pandu Port Reach
    [91.7000, 26.1720], # Saraighat Bridge Approach
    [91.6750, 26.1640]  # Downstream Jalukbari Reach
]

ASSAM_SHELTERS: List[Dict[str, Any]] = [
    {
        "id": "shelter_assam_1",
        "name": "Gauhati University High Ridge Shelter, Jalukbari",
        "region_id": "assam_guwahati",
        "lat": 26.1550,
        "lng": 91.6620,
        "elevation_m": 54.0,
        "total_capacity": 900,
        "current_occupancy": 380,
        "available_beds": 520,
        "status": "OPEN",
        "food_packs_available": 1600,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-361-257-0415"
    },
    {
        "id": "shelter_assam_2",
        "name": "Khanapara Administrative High Relief Center",
        "region_id": "assam_guwahati",
        "lat": 26.1260,
        "lng": 91.8150,
        "elevation_m": 48.5,
        "total_capacity": 1050,
        "current_occupancy": 410,
        "available_beds": 640,
        "status": "OPEN",
        "food_packs_available": 2200,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-361-223-7090"
    },
    {
        "id": "shelter_assam_3",
        "name": "Assam Engineering College Camp, Jalukbari",
        "region_id": "assam_guwahati",
        "lat": 26.1420,
        "lng": 91.6640,
        "elevation_m": 52.0,
        "total_capacity": 750,
        "current_occupancy": 290,
        "available_beds": 460,
        "status": "OPEN",
        "food_packs_available": 1400,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-361-257-0121"
    },
    {
        "id": "shelter_assam_4",
        "name": "Dispur Capital Complex Emergency Center",
        "region_id": "assam_guwahati",
        "lat": 26.1420,
        "lng": 91.7910,
        "elevation_m": 61.0,
        "total_capacity": 800,
        "current_occupancy": 760,
        "available_beds": 40,
        "status": "NEAR_CAPACITY",
        "food_packs_available": 600,
        "medical_staff_present": True,
        "generator_active": True,
        "contact_phone": "+91-361-226-0222"
    }
]

ASSAM_ROAD_NODES: Dict[str, Dict[str, Any]] = {
    "AN1": {"id": "AN1", "name": "MG Road Riverside Ghat (Low Basin)", "lat": 26.1850, "lng": 91.7450, "elev": 48.2, "base_hazard": 0.92},
    "AN2": {"id": "AN2", "name": "Fancy Bazar Commercial Center", "lat": 26.1820, "lng": 91.7420, "elev": 49.5, "base_hazard": 0.70},
    "AN3": {"id": "AN3", "name": "Panbazar Overbridge Ridge", "lat": 26.1840, "lng": 91.7510, "elev": 53.0, "base_hazard": 0.40},
    "AN4": {"id": "AN4", "name": "Guwahati Central Station / Paltan Bazar", "lat": 26.1760, "lng": 91.7530, "elev": 54.5, "base_hazard": 0.30},
    "AN5": {"id": "AN5", "name": "GS Road High Flyover (Bhangagarh)", "lat": 26.1610, "lng": 91.7680, "elev": 58.0, "base_hazard": 0.15},
    "AN6": {"id": "AN6", "name": "Ganeshguri Elevated Corridor", "lat": 26.1520, "lng": 91.7820, "elev": 60.5, "base_hazard": 0.08},
    "AN7": {"id": "AN7", "name": "Dispur Capital Complex Ridge", "lat": 26.1420, "lng": 91.7910, "elev": 61.0, "base_hazard": 0.05},
    "AN8": {"id": "AN8", "name": "Khanapara High Relief Hub", "lat": 26.1260, "lng": 91.8150, "elev": 65.0, "base_hazard": 0.00},
    "AN9": {"id": "AN9", "name": "Bharalumukh Lowland Causeway (Submerged)", "lat": 26.1780, "lng": 91.7310, "elev": 47.8, "base_hazard": 0.96},
    "AN10": {"id": "AN10", "name": "Maligaon High Transit Highway", "lat": 26.1580, "lng": 91.7050, "elev": 53.0, "base_hazard": 0.18},
    "AN11": {"id": "AN11", "name": "Jalukbari Rotary High Viaduct", "lat": 26.1480, "lng": 91.6680, "elev": 59.0, "base_hazard": 0.02}
}

ASSAM_ROAD_EDGES = [
    # Submerged riverside causeways (hazardous in spate)
    ("AN1", "AN9", {"road": "Brahmaputra Riverside Bund Road", "length_km": 1.55, "speed_kmh": 30, "hazard_factor": 0.95}),
    ("AN9", "AN10", {"road": "Pandu Lowland Reach Road", "length_km": 2.90, "speed_kmh": 35, "hazard_factor": 0.88}),
    ("AN1", "AN2", {"road": "MG Road Riverside Causeway", "length_km": 0.50, "speed_kmh": 35, "hazard_factor": 0.85}),
    # Safe elevated bypasses
    ("AN1", "AN3", {"road": "Panbazar Approach Elevated Link", "length_km": 0.85, "speed_kmh": 40, "hazard_factor": 0.35}),
    ("AN2", "AN4", {"road": "Fancy-Paltan Central Road", "length_km": 1.40, "speed_kmh": 40, "hazard_factor": 0.40}),
    ("AN3", "AN4", {"road": "Panbazar High Overbridge", "length_km": 0.90, "speed_kmh": 45, "hazard_factor": 0.15}),
    ("AN4", "AN5", {"road": "GS Road High Corridor North", "length_km": 2.20, "speed_kmh": 50, "hazard_factor": 0.15}),
    ("AN5", "AN6", {"road": "Bhangagarh-Ganeshguri Flyover", "length_km": 1.80, "speed_kmh": 55, "hazard_factor": 0.08}),
    ("AN6", "AN7", {"road": "GS Road Dispur Expressway", "length_km": 1.50, "speed_kmh": 55, "hazard_factor": 0.05}),
    ("AN7", "AN8", {"road": "Dispur-Khanapara Ridge Highway", "length_km": 2.80, "speed_kmh": 60, "hazard_factor": 0.01}),
    # West corridor to Jalukbari
    ("AN4", "AN10", {"road": "AT Road Maligaon High Corridor", "length_km": 4.90, "speed_kmh": 50, "hazard_factor": 0.15}),
    ("AN10", "AN11", {"road": "NH 27 Jalukbari Flyover Expressway", "length_km": 3.80, "speed_kmh": 60, "hazard_factor": 0.02})
]

ASSAM_SENSOR_INCIDENTS = [
    {"id": "as_inc_01", "lat": 26.1848, "lng": 91.7445, "water_depth_cm": 155, "severity": "CRITICAL", "source": "Brahmaputra CWC Station #4"},
    {"id": "as_inc_02", "lat": 26.1785, "lng": 91.7305, "water_depth_cm": 140, "severity": "CRITICAL", "source": "Bharalu River Sluice Gate"},
    {"id": "as_inc_03", "lat": 26.1825, "lng": 91.7415, "water_depth_cm": 110, "severity": "CRITICAL", "source": "Fancy Bazar Municipal Inundation Post"},
    {"id": "as_inc_04", "lat": 26.1860, "lng": 91.7460, "water_depth_cm": 135, "severity": "CRITICAL", "source": "Uzanbazar Ferry Ghat Gauge"},
    {"id": "as_inc_05", "lat": 26.1770, "lng": 91.7290, "water_depth_cm": 95, "severity": "HIGH", "source": "Pandu Port Telemetry Node"},
    # Pandu - Kamakhya Cluster
    {"id": "as_inc_06", "lat": 26.1720, "lng": 91.7180, "water_depth_cm": 120, "severity": "HIGH", "source": "Kamakhya Foothill Gauge"},
    {"id": "as_inc_07", "lat": 26.1735, "lng": 91.7195, "water_depth_cm": 105, "severity": "HIGH", "source": "Railway Lowland Sensor #9"},
    {"id": "as_inc_08", "lat": 26.1710, "lng": 91.7160, "water_depth_cm": 130, "severity": "CRITICAL", "source": "Brahmaputra Embankment Monitor"},
    # Downstream Cluster
    {"id": "as_inc_09", "lat": 26.1680, "lng": 91.6980, "water_depth_cm": 85, "severity": "HIGH", "source": "Maligaon Overpass Inflow Post"},
    {"id": "as_inc_10", "lat": 26.1695, "lng": 91.7010, "water_depth_cm": 90, "severity": "HIGH", "source": "Saraighat Approach Telemetry"},
    # Noise points
    {"id": "as_noise1", "lat": 26.1450, "lng": 91.7850, "water_depth_cm": 20, "severity": "LOW", "source": "Dispur Drain Overspill"},
    {"id": "as_noise2", "lat": 26.1280, "lng": 91.8100, "water_depth_cm": 15, "severity": "LOW", "source": "Khanapara Puddle Sensor"}
]

ASSAM_HISTORICAL_SEQUENCE = [
    {"hour_step": -72, "rainfall_mm": 18.0, "discharge_cumecs": 28000, "soil_sat": 0.65, "river_level_m": 47.8},
    {"hour_step": -66, "rainfall_mm": 25.5, "discharge_cumecs": 31000, "soil_sat": 0.70, "river_level_m": 48.2},
    {"hour_step": -60, "rainfall_mm": 38.0, "discharge_cumecs": 35000, "soil_sat": 0.76, "river_level_m": 48.7},
    {"hour_step": -54, "rainfall_mm": 54.0, "discharge_cumecs": 41000, "soil_sat": 0.82, "river_level_m": 49.2},
    {"hour_step": -48, "rainfall_mm": 72.0, "discharge_cumecs": 48000, "soil_sat": 0.88, "river_level_m": 49.8}, # Exceeds Danger Level (49.6m)
    {"hour_step": -42, "rainfall_mm": 95.0, "discharge_cumecs": 56000, "soil_sat": 0.93, "river_level_m": 50.4},
    {"hour_step": -36, "rainfall_mm": 115.0, "discharge_cumecs": 64000, "soil_sat": 0.96, "river_level_m": 50.9},
    {"hour_step": -30, "rainfall_mm": 130.0, "discharge_cumecs": 69000, "soil_sat": 0.98, "river_level_m": 51.3},
    {"hour_step": -24, "rainfall_mm": 125.0, "discharge_cumecs": 68000, "soil_sat": 0.98, "river_level_m": 51.5}, # Extreme Level (51.5m)
    {"hour_step": -18, "rainfall_mm": 105.0, "discharge_cumecs": 64000, "soil_sat": 0.97, "river_level_m": 51.2},
    {"hour_step": -12, "rainfall_mm": 88.0, "discharge_cumecs": 59000, "soil_sat": 0.95, "river_level_m": 50.8},
    {"hour_step": -6,  "rainfall_mm": 70.0, "discharge_cumecs": 53000, "soil_sat": 0.94, "river_level_m": 50.3},
    {"hour_step": 0,   "rainfall_mm": 62.0, "discharge_cumecs": 49000, "soil_sat": 0.93, "river_level_m": 49.9}
]

def get_region_data(region_id: str) -> Dict[str, Any]:
    """Helper to return region geographic components."""
    if region_id == "assam_guwahati":
        return {
            "metadata": REGIONS_METADATA["assam_guwahati"],
            "shelters": ASSAM_SHELTERS,
            "nodes": ASSAM_ROAD_NODES,
            "edges": ASSAM_ROAD_EDGES,
            "sensors": ASSAM_SENSOR_INCIDENTS,
            "river": ASSAM_RIVER_COORDINATES,
            "sequence": ASSAM_HISTORICAL_SEQUENCE
        }
    # Default to Kerala Ernakulam
    return {
        "metadata": REGIONS_METADATA.get(region_id, REGIONS_METADATA["kerala_ernakulam"]),
        "shelters": KERALA_SHELTERS,
        "nodes": KERALA_ROAD_NODES,
        "edges": KERALA_ROAD_EDGES,
        "sensors": KERALA_SENSOR_INCIDENTS,
        "river": KERALA_RIVER_COORDINATES,
        "sequence": KERALA_HISTORICAL_SEQUENCE
    }
