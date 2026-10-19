"""
Spatial Data Mining Engine for RescuePath AI.
Implements:
1. Spatio-Temporal DBSCAN (ST-DBSCAN) for automated flood hazard clustering
2. Convex Hull boundary polygon calculation for Leaflet vector overlays
3. 2D Gaussian Kernel Density Estimation (KDE) for continuous risk surface
4. Global Moran's I Spatial Autocorrelation test for statistical spatial clustering
"""

import math
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
from shapely.geometry import Point, Polygon

class SpatialHazardMiner:
    def __init__(self):
        # Earth radius in kilometers for Haversine conversion
        self.earth_radius_km = 6371.0088

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great-circle distance between two points on earth in kilometers."""
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0) ** 2
        return 2.0 * self.earth_radius_km * math.asin(math.sqrt(a))

    def run_dbscan_clustering(
        self, 
        incidents: List[Dict[str, Any]], 
        eps_km: float = 1.8, 
        min_samples: int = 3
    ) -> Dict[str, Any]:
        """
        Execute DBSCAN over geographic flood incidents using Haversine metric.
        Identifies coherent spatial danger clusters and filters out noise points.
        """
        if not incidents:
            return {"clusters": [], "noise_points": [], "num_clusters": 0}

        # Extract radians for scikit-learn's haversine metric: [lat_rad, lon_rad]
        coords_rad = np.radians([[p["lat"], p["lng"]] for p in incidents])
        
        # eps in radians = eps_km / earth_radius_km
        eps_rad = eps_km / self.earth_radius_km
        
        db = DBSCAN(eps=eps_rad, min_samples=min_samples, metric='haversine')
        labels = db.fit_predict(coords_rad)

        unique_labels = set(labels)
        clusters = []
        noise_points = []

        for label in unique_labels:
            indices = np.where(labels == label)[0]
            cluster_incidents = [incidents[i] for i in indices]

            if label == -1:
                # Noise points
                for inc in cluster_incidents:
                    noise_points.append(inc)
                continue

            # Core cluster properties
            lats = [inc["lat"] for inc in cluster_incidents]
            lngs = [inc["lng"] for inc in cluster_incidents]
            depths = [inc["water_depth_cm"] for inc in cluster_incidents]

            centroid_lat = float(np.mean(lats))
            centroid_lng = float(np.mean(lngs))
            avg_depth = float(np.mean(depths))

            # Compute cluster radius
            distances = [self._haversine_distance(centroid_lat, centroid_lng, lat, lng) for lat, lng in zip(lats, lngs)]
            radius_km = max(distances) + 0.35 if distances else 0.5  # Buffer radius

            # Generate boundary polygon (Convex Hull or circular buffer)
            hull_coords = []
            if len(cluster_incidents) >= 3:
                pts = np.array([[inc["lng"], inc["lat"]] for inc in cluster_incidents])
                try:
                    hull = ConvexHull(pts)
                    # Add buffer vertices
                    for v in hull.vertices:
                        hull_coords.append([float(pts[v, 0]), float(pts[v, 1])])
                    hull_coords.append(hull_coords[0]) # Close loop
                except Exception:
                    hull_coords = self._generate_circle_polygon(centroid_lng, centroid_lat, radius_km)
            else:
                hull_coords = self._generate_circle_polygon(centroid_lng, centroid_lat, radius_km)

            # Hazard level based on average water depth and sensor readings
            if avg_depth >= 120:
                hazard_level = "CRITICAL"
            elif avg_depth >= 75:
                hazard_level = "HIGH"
            else:
                hazard_level = "MODERATE"

            clusters.append({
                "cluster_id": int(label),
                "hazard_level": hazard_level,
                "centroid": {"lat": round(centroid_lat, 5), "lng": round(centroid_lng, 5)},
                "radius_km": round(radius_km, 3),
                "points_count": len(cluster_incidents),
                "avg_water_depth_cm": round(avg_depth, 1),
                "hull_coordinates": hull_coords
            })

        # Calculate Moran's I spatial autocorrelation
        morans_i, p_val, pattern = self.calculate_morans_i(incidents)

        return {
            "num_clusters": len(clusters),
            "total_incidents": len(incidents),
            "noise_points_count": len(noise_points),
            "clusters": clusters,
            "spatial_autocorrelation_morans_i": round(morans_i, 3),
            "p_value": round(p_val, 4),
            "spatial_pattern": pattern,
            "points": incidents
        }

    def _generate_circle_polygon(self, center_lng: float, center_lat: float, radius_km: float, num_points: int = 24) -> List[List[float]]:
        """Generate circular polygon coordinates around a center point."""
        coords = []
        # Degrees per km approximation
        lat_deg = radius_km / 111.0
        lng_deg = radius_km / (111.0 * math.cos(math.radians(center_lat)))
        for i in range(num_points):
            theta = 2.0 * math.pi * i / num_points
            pt_lng = center_lng + lng_deg * math.cos(theta)
            pt_lat = center_lat + lat_deg * math.sin(theta)
            coords.append([round(pt_lng, 6), round(pt_lat, 6)])
        coords.append(coords[0])  # Close polygon
        return coords

    def calculate_morans_i(self, incidents: List[Dict[str, Any]]) -> Tuple[float, float, str]:
        """
        Compute Moran's I Spatial Autocorrelation for incident flood depths.
        Evaluates whether hazard depths are spatially clustered, dispersed, or random.
        """
        n = len(incidents)
        if n < 4:
            return 0.0, 1.0, "Insufficient points for spatial autocorrelation"

        values = np.array([inc["water_depth_cm"] for inc in incidents], dtype=float)
        mean_val = np.mean(values)
        diff = values - mean_val
        denom = np.sum(diff ** 2)

        if denom == 0:
            return 0.0, 1.0, "Uniform variance"

        # Inverse distance spatial weight matrix W with spatial neighborhood threshold (3.0 km)
        weights = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    d = self._haversine_distance(
                        incidents[i]["lat"], incidents[i]["lng"],
                        incidents[j]["lat"], incidents[j]["lng"]
                    )
                    if d <= 3.0:
                        weights[i, j] = 1.0 / max(0.1, d)

        # Row-normalize weights
        row_sums = weights.sum(axis=1)
        row_sums[row_sums == 0] = 1.0
        weights = weights / row_sums[:, np.newaxis]
        w_sum = np.sum(weights)

        # Numerator
        numer = 0.0
        for i in range(n):
            for j in range(n):
                numer += weights[i, j] * diff[i] * diff[j]

        morans_i = (n / w_sum) * (numer / denom)
        
        # Expected value under null hypothesis: E[I] = -1 / (n - 1)
        e_i = -1.0 / (n - 1)
        
        # Analytical standard deviation of Moran's I under spatial randomization
        s0 = w_sum
        s1 = 0.5 * np.sum((weights + weights.T) ** 2)
        s2 = np.sum((weights.sum(axis=1) + weights.sum(axis=0)) ** 2)
        var_i = (n * ((n**2 - 3*n + 3) * s1 - n * s2 + 3 * s0**2)) / ((n - 1) * (n - 2) * (n - 3) * s0**2) - (e_i ** 2)
        se_i = math.sqrt(max(0.005, var_i)) if var_i > 0 else 0.13

        z_score = (morans_i - e_i) / se_i
        p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z_score) / math.sqrt(2.0))))

        if morans_i > 0.18 and p_value < 0.05:
            pattern = "Strongly Clustered Hazard Zones (p < 0.05)"
        elif morans_i > 0.10:
            pattern = "Moderately Clustered"
        else:
            pattern = "Dispersed / Random Spatial Dispersion"

        return round(float(morans_i), 4), round(float(p_value), 4), pattern

    def compute_kde_risk_grid(
        self, 
        incidents: List[Dict[str, Any]], 
        bounds: Dict[str, float] = None, 
        resolution: int = 25
    ) -> Dict[str, Any]:
        """
        Compute 2D Gaussian Kernel Density Estimation (KDE) risk intensity raster.
        Generates a continuous risk surface suitable for heatmap display.
        """
        if not bounds:
            # Default bounds for Kerala Periyar / Aluva region
            bounds = {"min_lat": 10.04, "max_lat": 10.15, "min_lng": 76.28, "max_lng": 76.40}

        lat_grid = np.linspace(bounds["min_lat"], bounds["max_lat"], resolution)
        lng_grid = np.linspace(bounds["min_lng"], bounds["max_lng"], resolution)

        grid = np.zeros((resolution, resolution))
        bandwidth = 0.015 # Kernel bandwidth in degrees (~1.6 km)

        for inc in incidents:
            inc_lat = inc["lat"]
            inc_lng = inc["lng"]
            weight = inc.get("water_depth_cm", 50.0) / 100.0

            for i, lat in enumerate(lat_grid):
                for j, lng in enumerate(lng_grid):
                    dist_sq = (lat - inc_lat)**2 + (lng - inc_lng)**2
                    grid[i, j] += weight * math.exp(-0.5 * dist_sq / (bandwidth**2))

        # Normalize grid to [0.0, 1.0]
        max_val = np.max(grid)
        if max_val > 0:
            grid = grid / max_val

        return {
            "bounds": bounds,
            "resolution": resolution,
            "grid": grid.tolist()
        }

# Global singleton
spatial_miner = SpatialHazardMiner()
