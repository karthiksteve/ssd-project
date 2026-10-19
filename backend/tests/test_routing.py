import pytest
from backend.app.core.graph_router import graph_router
from backend.app.database.seed_data import get_region_data

def test_build_network_graph():
    G = graph_router.build_network_graph("kerala_ernakulam")
    assert len(G.nodes) > 10
    assert len(G.edges) > 10
    
    # Check node and edge attributes
    sample_node = list(G.nodes.values())[0]
    assert "lat" in sample_node
    assert "lng" in sample_node
    assert "elev" in sample_node

    sample_edge = list(G.edges.values())[0]
    assert "length_km" in sample_edge
    assert "standard_weight" in sample_edge
    assert "safe_weight" in sample_edge

def test_find_nearest_node():
    G = graph_router.build_network_graph("kerala_ernakulam")
    # Coordinates of Aluva Manappuram
    nearest = graph_router.find_nearest_node(G, 10.1080, 76.3530)
    assert nearest == "N1"

def test_evacuation_routing_safety_comparison():
    # Starting at Aluva Manappuram (N1 - low elevation, flooded riverbank)
    routes = graph_router.compute_evacuation_routes(
        region_id="kerala_ernakulam",
        start_lat=10.1085,
        start_lng=76.3535,
        flood_surge_active=True
    )
    
    assert "safe_route" in routes
    assert "standard_route" in routes
    assert "target_shelter" in routes
    
    safe = routes["safe_route"]
    std = routes["standard_route"]
    
    # Standard route should take the hazardous direct river path
    # Safe route should divert to elevated road corridors
    assert safe["risk_exposure_score"] <= std["risk_exposure_score"]
    assert routes["risk_reduction_percentage"] >= 0.0
    assert len(safe["waypoints"]) > 0
    assert len(std["waypoints"]) > 0
