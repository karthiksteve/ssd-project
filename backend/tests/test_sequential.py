import pytest
from backend.app.core.sequential_miner import sequential_miner
from backend.app.database.seed_data import get_region_data

def test_sequential_features_extraction():
    data = get_region_data("kerala_ernakulam")
    sequence = data["sequence"]
    
    feats = sequential_miner.extract_sequential_features(sequence)
    assert "rain_recent_24h" in feats
    assert "rate_of_rise" in feats
    assert feats["rain_recent_24h"] > 0
    assert feats["current_discharge"] > 0

def test_predict_multi_step_horizon():
    data = get_region_data("kerala_ernakulam")
    sequence = data["sequence"]
    
    forecast = sequential_miner.predict_multi_step_horizon(sequence)
    assert "forecast_24h" in forecast
    assert "forecast_48h" in forecast
    assert "forecast_72h" in forecast
    
    f24 = forecast["forecast_24h"]
    assert 0.0 <= f24["flood_probability"] <= 1.0
    assert f24["expected_river_level_m"] > 3.0
    assert f24["risk_level"] in ["LOW", "MODERATE", "HIGH", "SEVERE"]
    assert len(f24["driving_factors"]) > 0

def test_surge_multiplier_escalation():
    data = get_region_data("kerala_ernakulam")
    sequence = data["sequence"]
    
    normal = sequential_miner.predict_multi_step_horizon(sequence, surge_multiplier=1.0)
    surged = sequential_miner.predict_multi_step_horizon(sequence, surge_multiplier=1.6)
    
    # Severe surge should increase river level and flood probability
    assert surged["forecast_24h"]["expected_river_level_m"] >= normal["forecast_24h"]["expected_river_level_m"]
    assert surged["forecast_48h"]["flood_probability"] >= normal["forecast_48h"]["flood_probability"]
