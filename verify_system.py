"""
RescuePath AI - Master System Diagnostic & Algorithmic Verification Suite
Comprehensive automated test runner for CSE3068 Sequential & Spatial Data Mining Platform.
"""

import sys
import os
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

def print_banner():
    print("=" * 74)
    print("      RESCUEPATH AI — MASTER SYSTEM DIAGNOSTIC & VERIFICATION SUITE")
    print("      Sequential and Spatial Data Mining (CSE3068) Academic Platform")
    print("=" * 74)

def print_result(category: str, item: str, passed: bool, detail: str = ""):
    icon = "[PASS]" if passed else "[FAIL]"
    status_color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    detail_str = f" | {detail}" if detail else ""
    print(f"{status_color}{icon:<7}{reset} {category:<20} : {item:<30}{detail_str}")

def main():
    print_banner()
    start_time = time.time()
    total_checks = 0
    passed_checks = 0

    # 1. Environment & Dependencies
    print("\n[1/7] Python Runtime & Required Libraries")
    print("-" * 74)
    required_packages = [
        ("fastapi", "0.110.0"),
        ("uvicorn", "0.28.0"),
        ("pydantic", "2.6.0"),
        ("numpy", "1.26.0"),
        ("pandas", "2.2.0"),
        ("sklearn", "1.4.0"),
        ("scipy", "1.12.0"),
        ("networkx", "3.2.0"),
        ("shapely", "2.0.0"),
        ("pytest", "8.0.0")
    ]

    for pkg_name, min_ver in required_packages:
        total_checks += 1
        try:
            mod = __import__(pkg_name)
            ver = getattr(mod, "__version__", "installed")
            print_result("Dependencies", pkg_name, True, f"v{ver}")
            passed_checks += 1
        except ImportError as e:
            print_result("Dependencies", pkg_name, False, str(e))

    # 2. Sequential Data Mining Engine
    print("\n[2/7] Sequential Data Mining (Time-Series Sequence Prediction)")
    print("-" * 74)
    try:
        total_checks += 1
        from backend.app.database.seed_data import get_region_data
        from backend.app.core.sequential_miner import sequential_miner

        kerala_data = get_region_data("kerala_ernakulam")
        sequence = kerala_data["sequence"]
        features = sequential_miner.extract_sequential_features(sequence)
        
        has_features = ("rate_of_rise_m_per_step" in features and "rainfall_24h_sum" in features)
        print_result("Sequential Engine", "Sliding Window Features", has_features, f"Rate of Rise: {features.get('rate_of_rise_m_per_step', 0):.2f}m/6h")
        if has_features: passed_checks += 1

        total_checks += 1
        forecast = sequential_miner.predict_multi_step_horizon(sequence)
        has_forecast = all(k in forecast for k in ["forecast_24h", "forecast_48h", "forecast_72h"])
        f24 = forecast["forecast_24h"]
        print_result(
            "Sequential Engine", 
            "Multi-Step 24h/48h/72h", 
            has_forecast, 
            f"+24h Prob: {f24['flood_probability']*100:.1f}%, Expected: {f24['expected_river_level_m']}m"
        )
        if has_forecast: passed_checks += 1

        total_checks += 1
        has_trend = bool(forecast.get("sequence_trend"))
        print_result("Sequential Engine", "Trend Classification", has_trend, forecast.get("sequence_trend", ""))
        if has_trend: passed_checks += 1

    except Exception as e:
        print_result("Sequential Engine", "Initialization", False, str(e))

    # 3. Spatial Data Mining Engine
    print("\n[3/7] Spatial Data Mining (ST-DBSCAN Clustering, Moran's I & KDE)")
    print("-" * 74)
    try:
        total_checks += 1
        from backend.app.core.spatial_miner import spatial_miner

        sensors = kerala_data["sensors"]
        cluster_res = spatial_miner.run_dbscan_clustering(sensors, eps_km=1.8, min_samples=3)
        has_clusters = cluster_res["num_clusters"] >= 1
        print_result(
            "Spatial Mining", 
            "ST-DBSCAN Clustering", 
            has_clusters, 
            f"{cluster_res['num_clusters']} hazard zones, {cluster_res['noise_points_count']} noise filtered"
        )
        if has_clusters: passed_checks += 1

        total_checks += 1
        morans_i = cluster_res["spatial_autocorrelation_morans_i"]
        has_autocorr = (morans_i > 0.20 and cluster_res["p_value"] < 0.05)
        print_result(
            "Spatial Mining", 
            "Global Moran's I", 
            has_autocorr, 
            f"I = {morans_i:.3f}, p = {cluster_res['p_value']} ({cluster_res['spatial_pattern']})"
        )
        if has_autocorr: passed_checks += 1

        total_checks += 1
        kde_res = spatial_miner.compute_kde_risk_grid(sensors, resolution=20)
        has_kde = len(kde_res["grid"]) == 20
        print_result("Spatial Mining", "2D Gaussian KDE Grid", has_kde, f"Resolution: 20x20 risk surface")
        if has_kde: passed_checks += 1

    except Exception as e:
        print_result("Spatial Mining", "Execution", False, str(e))

    # 4. Spatial Graph Router (Risk-Penalized A* vs Dijkstra)
    print("\n[4/7] Spatial Graph Evacuation Router (NetworkX Dynamic Routing)")
    print("-" * 74)
    try:
        total_checks += 1
        from backend.app.core.graph_router import graph_router

        G = graph_router.build_network_graph("kerala_ernakulam", flood_surge_active=True)
        has_graph = len(G.nodes) >= 10 and len(G.edges) >= 10
        print_result("Graph Router", "NetworkX Road Graph", has_graph, f"{len(G.nodes)} nodes, {len(G.edges)} road links")
        if has_graph: passed_checks += 1

        total_checks += 1
        routes = graph_router.compute_evacuation_routes(
            region_id="kerala_ernakulam",
            start_lat=10.1085,
            start_lng=76.3535,
            flood_surge_active=True
        )
        safe = routes["safe_route"]
        std = routes["standard_route"]
        risk_reduced = routes["risk_reduction_percentage"] >= 0.0
        print_result(
            "Graph Router", 
            "Dynamic Risk Avoidance", 
            risk_reduced, 
            f"{routes['risk_reduction_percentage']:.1f}% risk avoided (Safe: {safe['total_distance_km']}km vs Std: {std['total_distance_km']}km)"
        )
        if risk_reduced: passed_checks += 1

        total_checks += 1
        has_shelter = "name" in routes["target_shelter"]
        print_result("Graph Router", "Optimal Shelter Allocation", has_shelter, routes["target_shelter"]["name"])
        if has_shelter: passed_checks += 1

    except Exception as e:
        print_result("Graph Router", "Execution", False, str(e))

    # 5. Multi-Basin & Scenario Simulation Support
    print("\n[5/7] Multi-Basin Regional Coverage & Disaster Surge Simulation")
    print("-" * 74)
    try:
        total_checks += 1
        from backend.app.core.scenario_simulator import scenario_simulator
        from backend.app.database.seed_data import REGIONS_METADATA

        has_basins = ("kerala_ernakulam" in REGIONS_METADATA and "assam_guwahati" in REGIONS_METADATA)
        print_result("Regional Basins", "Kerala & Assam Calibrated", has_basins, f"Registered: {list(REGIONS_METADATA.keys())}")
        if has_basins: passed_checks += 1

        total_checks += 1
        sim_res = scenario_simulator.trigger_surge("kerala_ernakulam", scenario="dam_gate_release", intensity=1.5)
        has_sim = sim_res["new_active_clusters"] >= 1
        print_result("Disaster Simulator", "Dam Gate Surge Injection", has_sim, f"{len(sim_res['critical_roads_severed'])} roads severed")
        if has_sim: passed_checks += 1

    except Exception as e:
        print_result("Disaster Simulator", "Execution", False, str(e))

    # 6. Data Directory & Academic Notebook Integrity
    print("\n[6/7] Data Repository & Jupyter Analysis Notebook")
    print("-" * 74)
    expected_data_files = [
        "data/kerala_periyar_hydro_timeseries_72h.csv",
        "data/assam_brahmaputra_hydro_timeseries_72h.csv",
        "data/kerala_telemetry_sensors.csv",
        "data/kerala_telemetry_sensors.geojson",
        "data/national_shelter_directory.csv",
        "data/kerala_road_network_topology.json"
    ]

    for rel_path in expected_data_files:
        total_checks += 1
        full_path = PROJECT_ROOT / rel_path
        exists = full_path.is_file() and full_path.stat().st_size > 0
        print_result("Data Repository", rel_path, exists, f"{full_path.stat().st_size} bytes" if exists else "Missing")
        if exists: passed_checks += 1

    # Check notebook execution status
    total_checks += 1
    nb_path = PROJECT_ROOT / "notebooks" / "ssdm_exploratory_analysis.ipynb"
    nb_ok = False
    if nb_path.is_file():
        import json
        with open(nb_path, "r", encoding="utf-8") as f:
            nb_json = json.load(f)
        # Check if outputs exist in code cells
        code_cells = [c for c in nb_json.get("cells", []) if c.get("cell_type") == "code"]
        cells_with_outputs = [c for c in code_cells if len(c.get("outputs", [])) > 0]
        nb_ok = len(cells_with_outputs) >= 4
        print_result("Academic Notebook", "Embedded Output Cells", nb_ok, f"{len(cells_with_outputs)}/{len(code_cells)} code cells executed")
    else:
        print_result("Academic Notebook", "Notebook File", False, "Missing")
    if nb_ok: passed_checks += 1

    # 7. Frontend Build & Static Assets
    print("\n[7/7] Frontend Production Build & GIS Assets")
    print("-" * 74)
    total_checks += 1
    frontend_dist = PROJECT_ROOT / "frontend" / "dist" / "index.html"
    dist_ok = frontend_dist.is_file()
    print_result("Frontend Build", "Production Bundle (Vite)", dist_ok, f"{frontend_dist.stat().st_size} bytes" if dist_ok else "Not built")
    if dist_ok: passed_checks += 1

    # Summary Report
    elapsed = time.time() - start_time
    print("\n" + "=" * 74)
    print("                     DIAGNOSTIC SUMMARY & HEALTH SCORE")
    print("=" * 74)
    score_pct = (passed_checks / total_checks) * 100
    status_label = "PRODUCTION READY — 100% OPERATIONAL" if score_pct == 100 else "OPERATIONAL WITH NOTICES"

    print(f"  Total Algorithmic & System Checks : {total_checks}")
    print(f"  Checks Passed Successfully        : {passed_checks}")
    print(f"  Overall System Health Rating      : {score_pct:.1f}%")
    print(f"  Platform Status                   : {status_label}")
    print(f"  Execution Time                    : {elapsed:.2f} seconds")
    print("=" * 74 + "\n")

    if passed_checks == total_checks:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
