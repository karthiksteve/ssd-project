import pytest
from backend.app.core.spatial_miner import spatial_miner
from backend.app.database.seed_data import get_region_data

def test_dbscan_clustering():
    data = get_region_data("kerala_ernakulam")
    sensors = data["sensors"]
    
    result = spatial_miner.run_dbscan_clustering(sensors, eps_km=1.8, min_samples=3)
    
    assert result["num_clusters"] >= 1
    assert result["total_incidents"] == len(sensors)
    assert result["noise_points_count"] >= 1  # Should filter isolated points as noise
    
    # Check cluster structure
    first_cluster = result["clusters"][0]
    assert "centroid" in first_cluster
    assert "hull_coordinates" in first_cluster
    assert len(first_cluster["hull_coordinates"]) >= 3
    assert first_cluster["hazard_level"] in ["MODERATE", "HIGH", "CRITICAL"]

def test_morans_i_autocorrelation():
    data = get_region_data("kerala_ernakulam")
    sensors = data["sensors"]
    
    morans_i, p_val, pattern = spatial_miner.calculate_morans_i(sensors)
    # Check that Moran's I is computed in valid bounds [-1, 1]
    assert -1.0 <= morans_i <= 1.0
    assert 0.0 <= p_val <= 1.0
    assert len(pattern) > 0

def test_kde_risk_grid():
    data = get_region_data("kerala_ernakulam")
    sensors = data["sensors"]
    
    res = 20
    kde = spatial_miner.compute_kde_risk_grid(sensors, resolution=res)
    assert kde["resolution"] == res
    assert len(kde["grid"]) == res
    assert len(kde["grid"][0]) == res
    # Max value should be normalized to 1.0
    max_val = max(max(row) for row in kde["grid"])
    assert 0.95 <= max_val <= 1.05
