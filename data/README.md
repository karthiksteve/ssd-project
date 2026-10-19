# RescuePath AI: Spatial & Sequential Datasets Directory

This directory contains the primary spatial, sequential, and logistical datasets used by **RescuePath AI** for predictive flood modeling and dynamic evacuation routing across Indian river basins.

---

## 1. Directory Structure

```
data/
├── kerala_periyar_hydro_timeseries_72h.csv     # 72-hour hydro-meteorological time-series (Periyar Basin)
├── assam_brahmaputra_hydro_timeseries_72h.csv  # 72-hour hydro-meteorological time-series (Brahmaputra Basin)
├── kerala_telemetry_sensors.csv               # Spatial telemetry & citizen SOS points (Ernakulam/Aluva)
├── kerala_telemetry_sensors.geojson           # GeoJSON FeatureCollection of Kerala telemetry
├── assam_telemetry_sensors.csv                # Spatial telemetry & citizen SOS points (Guwahati/Kamrup)
├── assam_telemetry_sensors.geojson            # GeoJSON FeatureCollection of Assam telemetry
├── kerala_road_network_topology.json          # NetworkX-compatible road vertices & impedance edges
├── assam_road_network_topology.json           # Road network for Kamrup Metropolitan corridor
├── national_shelter_directory.csv             # Relief shelters registry (capacities, beds, supplies)
└── README.md                                  # This documentation
```

---

## 2. Dataset Schemas & Metadata

### A. Sequential Hydro-Meteorological Time-Series (`*.csv`)
Sequential time-series sampled at 6-hour intervals across the past 72 hours ($t = -72\text{h}$ to $t = 0\text{h}$):

| Column | Unit / Format | Description |
| :--- | :--- | :--- |
| `hour_step` | Hours | Relative timestamp relative to present ($t=0$). Negative values represent past observations. |
| `timestamp` | ISO-8601 UTC | Absolute calendar timestamp of measurement. |
| `rainfall_mm` | mm / 6h | Cumulative catchment precipitation from automatic weather stations (AWS). |
| `discharge_cumecs` | $\text{m}^3/\text{s}$ | Upstream reservoir discharge (e.g., Idamalayar & Idukki dams in Kerala). |
| `soil_sat` | Index $[0.0 - 1.0]$ | Topsoil moisture saturation index derived from satellite radar / lysimeter sensors. |
| `river_level_m` | Meters | River gauge height at critical gauging stations (e.g., Aluva Manappuram / Pandu Ghat). |
| `danger_mark_m` | Meters | Official Central Water Commission (CWC) Danger Level threshold. |
| `flood_state` | Categorical | Operational status: `NORMAL`, `ALERT`, `WARNING`, or `CRITICAL_INUNDATION`. |

### B. Spatial Telemetry & Citizen SOS Reports (`*.csv` & `*.geojson`)
Spatial point incidents evaluated by ST-DBSCAN for hazard zone clustering:

| Column | Unit / Format | Description |
| :--- | :--- | :--- |
| `id` | String | Unique telemetry or citizen incident report ID. |
| `name` | String | Location or administrative ward name. |
| `lat` | Decimal Degrees | Latitude in WGS 84 (EPSG:4326). |
| `lng` | Decimal Degrees | Longitude in WGS 84 (EPSG:4326). |
| `water_depth_cm` | Centimeters | Ground-level flood water depth measured by ultrasonic IoT telemetry or field reports. |
| `severity` | Categorical | `NORMAL`, `ELEVATED`, `CRITICAL`, or `SEVERE`. |
| `sos_calls` | Integer | Volume of SOS emergency calls received within 1.8 km radius in the past 6 hours. |
| `source` | Categorical | Data origin: `cwc_gauge`, `iot_sensor`, `citizen_sos`, or `ndrf_field_report`. |

### C. Road Network Graph Topology (`*.json`)
Multi-attributed topological graph representing the regional transportation network:
- **`nodes`**: Road junctions with elevation ($m$), geographic coordinates, and baseline hazard vulnerability.
- **`edges`**: Road segments with physical length ($\text{km}$), speed limit ($\text{km/h}$), nominal travel time ($\text{min}$), and dynamic flood impedance factors. Submerged roads ($\text{Hazard} \ge 0.75$) are severed dynamically during active surges.

### D. National Relief Shelter Directory (`national_shelter_directory.csv`)
Logistical database of pre-identified flood relief centers:
- `id`, `name`, `region_id`, `lat`, `lng`, `elevation_m`
- `total_capacity`, `current_occupancy`, `available_beds`, `status` (`OPEN`, `NEAR_CAPACITY`, `FULL`)
- `food_packs_available`, `medical_staff_present`, `generator_active`, `contact_phone`
