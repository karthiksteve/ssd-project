"""
Disaster Scenario Simulator for RescuePath AI.
Maintains live crisis states and dynamically modulates sequential and spatial hazards.
"""

from typing import Dict, Any, List
from backend.app.database.seed_data import get_region_data
from backend.app.core.sequential_miner import sequential_miner
from backend.app.core.spatial_miner import spatial_miner

class ScenarioSimulator:
    def __init__(self):
        self.active_scenarios: Dict[str, Dict[str, Any]] = {
            "kerala_ernakulam": {
                "scenario_name": "nominal_monsoon",
                "intensity": 1.0,
                "surge_active": False,
                "description": "Seasonal monsoon rainfall with active river monitoring."
            },
            "assam_guwahati": {
                "scenario_name": "nominal_monsoon",
                "intensity": 1.0,
                "surge_active": False,
                "description": "Normal high-water season along the Brahmaputra channel."
            }
        }

    def trigger_scenario(self, region_id: str, scenario: str, intensity: float = 1.5) -> Dict[str, Any]:
        """
        Dynamically trigger a simulated disaster event.
        Scenarios: 'dam_gate_release', 'monsoon_surge', 'flash_flood', 'receding'
        """
        if region_id not in self.active_scenarios:
            region_id = "kerala_ernakulam"

        surge_active = (scenario != "receding")
        
        self.active_scenarios[region_id] = {
            "scenario_name": scenario,
            "intensity": intensity,
            "surge_active": surge_active,
            "description": self._get_description(scenario, intensity)
        }

        # Calculate updated sequential forecast under this scenario
        data = get_region_data(region_id)
        base_seq = data["sequence"]
        updated_forecast = sequential_miner.predict_multi_step_horizon(
            base_seq, 
            surge_multiplier=intensity if surge_active else 0.65
        )

        # Modulate sensor incidents based on scenario
        sensors = data["sensors"].copy()
        severed_roads = []
        if surge_active:
            for s in sensors:
                s["water_depth_cm"] = int(s["water_depth_cm"] * intensity)
            severed_roads = [
                "Periyar Riverbank Link (Submerged: Depth > 1.8m)",
                "Manappuram Ghat Road (Impasse: High Flow)",
                "Eloor Lowland Industrial Access (Flooded)"
            ]

        # Spatial clusters under updated scenario
        cluster_data = spatial_miner.run_dbscan_clustering(sensors, eps_km=1.8, min_samples=3)

        return {
            "scenario": scenario,
            "region_id": region_id,
            "applied_multiplier": intensity,
            "message": f"Simulation active: {scenario.replace('_', ' ').title()} at {intensity}x intensity.",
            "new_active_clusters": cluster_data["num_clusters"],
            "critical_roads_severed": severed_roads,
            "forecast_updated": updated_forecast
        }

    def get_status(self, region_id: str) -> Dict[str, Any]:
        return self.active_scenarios.get(region_id, self.active_scenarios["kerala_ernakulam"])

    def _get_description(self, scenario: str, intensity: float) -> str:
        if scenario == "dam_gate_release":
            return f"Idamalayar & Idukki Reservoir sluice gates opened ({int(intensity*1800)} cumecs). Periyar river overtopping banks."
        elif scenario == "monsoon_surge":
            return f"Extreme monsoon cloudburst ({int(intensity*90)}mm/24h) causing severe urban drainage blockages."
        elif scenario == "flash_flood":
            return f"Sudden upstream catchment cloudburst producing high-velocity flash flood surge."
        elif scenario == "receding":
            return "Precipitation subsided. Reservoir discharge regulated. Flood waters draining into estuary."
        return "Nominal monsoon operations."

# Global singleton
scenario_simulator = ScenarioSimulator()
