"""
RescuePath AI - Dataset Exporter.
Serializes seed geographic datasets and time-series sequences into standard
CSV, GeoJSON, and JSON files in the data/ directory.
"""

import os
import sys
import json
import csv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.database.seed_data import get_region_data, REGIONS_METADATA

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def export_timeseries(filename, sequence, danger_threshold):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "hour_step", "rainfall_mm", "discharge_cumecs", 
            "soil_sat", "river_level_m", "danger_mark_m", "flood_state"
        ])
        for row in sequence:
            lvl = row["river_level_m"]
            if lvl >= danger_threshold * 1.05:
                state = "CRITICAL_INUNDATION"
            elif lvl >= danger_threshold:
                state = "DANGER_WARNING"
            elif lvl >= danger_threshold * 0.85:
                state = "ALERT"
            else:
                state = "NORMAL"

            writer.writerow([
                row["hour_step"],
                row["rainfall_mm"],
                row["discharge_cumecs"],
                row["soil_sat"],
                row["river_level_m"],
                danger_threshold,
                state
            ])
    print(f"[OK] Exported timeseries -> {filepath}")

def export_sensors_csv(filename, sensors):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "lat", "lng", "water_depth_cm", "severity", "sos_calls", "source"])
        for s in sensors:
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
    print(f"[OK] Exported sensors CSV -> {filepath}")

def export_sensors_geojson(filename, sensors):
    filepath = os.path.join(DATA_DIR, filename)
    features = []
    for s in sensors:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [s["lng"], s["lat"]]
            },
            "properties": {
                "id": s["id"],
                "name": s.get("name", s.get("source", "Telemetry Point")),
                "water_depth_cm": s["water_depth_cm"],
                "severity": s["severity"],
                "sos_calls": s.get("sos_calls", 0),
                "source": s.get("source", "iot_telemetry")
            }
        }
        features.append(feature)

    geojson_doc = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features
    }

    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(geojson_doc, f, indent=2)
    print(f"[OK] Exported sensors GeoJSON -> {filepath}")

def export_road_network(filename, nodes, edges):
    filepath = os.path.join(DATA_DIR, filename)
    edge_list = []
    for u, v, attrs in edges:
        edge_list.append({
            "from_node": u,
            "to_node": v,
            "road_name": attrs["road"],
            "length_km": attrs["length_km"],
            "speed_kmh": attrs["speed_kmh"],
            "hazard_factor": attrs.get("hazard_factor", 0.0)
        })

    network_doc = {
        "nodes": list(nodes.values()),
        "edges": edge_list
    }

    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(network_doc, f, indent=2)
    print(f"[OK] Exported road network JSON -> {filepath}")

def export_shelters_csv():
    filepath = os.path.join(DATA_DIR, "national_shelter_directory.csv")
    kerala_data = get_region_data("kerala_ernakulam")
    assam_data = get_region_data("assam_guwahati")
    all_shelters = kerala_data["shelters"] + assam_data["shelters"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "name", "region_id", "lat", "lng", "elevation_m",
            "total_capacity", "current_occupancy", "available_beds",
            "status", "food_packs_available", "medical_staff_present",
            "generator_active", "contact_phone"
        ])
        for s in all_shelters:
            writer.writerow([
                s["id"], s["name"], s["region_id"], s["lat"], s["lng"], s["elevation_m"],
                s["total_capacity"], s["current_occupancy"], s["available_beds"],
                s["status"], s["food_packs_available"], s["medical_staff_present"],
                s["generator_active"], s["contact_phone"]
            ])
    print(f"[OK] Exported shelter registry -> {filepath}")

def main():
    print("Exporting RescuePath AI Spatial & Sequential Datasets...")
    kerala_data = get_region_data("kerala_ernakulam")
    assam_data = get_region_data("assam_guwahati")
    
    # 1. Timeseries
    export_timeseries(
        "kerala_periyar_hydro_timeseries_72h.csv", 
        kerala_data["sequence"], 
        kerala_data["metadata"]["danger_threshold_m"]
    )
    export_timeseries(
        "assam_brahmaputra_hydro_timeseries_72h.csv", 
        assam_data["sequence"], 
        assam_data["metadata"]["danger_threshold_m"]
    )

    # 2. Sensor Telemetry
    export_sensors_csv("kerala_telemetry_sensors.csv", kerala_data["sensors"])
    export_sensors_geojson("kerala_telemetry_sensors.geojson", kerala_data["sensors"])

    export_sensors_csv("assam_telemetry_sensors.csv", assam_data["sensors"])
    export_sensors_geojson("assam_telemetry_sensors.geojson", assam_data["sensors"])

    # 3. Road Networks
    export_road_network("kerala_road_network_topology.json", kerala_data["nodes"], kerala_data["edges"])
    export_road_network("assam_road_network_topology.json", assam_data["nodes"], assam_data["edges"])

    # 4. Shelters
    export_shelters_csv()

    print("All datasets generated successfully in data/ directory!")

if __name__ == "__main__":
    main()
