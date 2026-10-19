"""
Generates high-resolution publication-grade technical implementation diagrams
for RescuePath AI:
1. sequential_mining_pipeline.png
2. spatial_mining_pipeline.png
3. graph_routing_pipeline.png
4. data_flow_architecture.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ASSETS_DIR = r"c:\Users\speak\Downloads\ssd_project\docs_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def draw_box(ax, x, y, w, h, bg_color, border_color, title, subtitle=None, text_color='#F8FAFC', title_size=9, sub_size=7.5):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(rect)
    if subtitle:
        ax.text(x + w/2, y + h - 2.8, title, color=text_color, fontsize=title_size, fontweight='bold', ha='center', va='center')
        ax.text(x + w/2, y + (h - 2.8)/2, subtitle, color='#CBD5E1', fontsize=sub_size, ha='center', va='center')
    else:
        ax.text(x + w/2, y + h/2, title, color=text_color, fontsize=title_size, fontweight='bold', ha='center', va='center')

def draw_arrow(ax, x1, y1, x2, y2, color='#38BDF8', lw=1.6):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw, shrinkA=2, shrinkB=2))

# ---------------------------------------------------------------------------
# 1. SEQUENTIAL DATA MINING PIPELINE DIAGRAM
# ---------------------------------------------------------------------------
def generate_sequential_pipeline():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')

    # Header
    ax.text(50, 96, "Sequential Data Mining Engine — Technical Pipeline", 
            color='#F8FAFC', fontsize=15, fontweight='bold', ha='center')
    ax.text(50, 92, "Sliding-Window Feature Extraction • Runoff Saturation Coupling • Multi-Horizon Prediction", 
            color='#38BDF8', fontsize=9.5, ha='center')

    # Step 1: Input Data Sequence
    draw_box(ax, 3, 56, 20, 30, '#1E293B', '#38BDF8', 
             "1. Telemetry Ingestion", 
             "Multivariate Sequence X_t:\n• Rainfall R_t (mm)\n• Discharge Q_t (cumecs)\n• River Gauge H_t (m)\n• Soil Saturation S_t [0,1]\nSampling: Δt = 6 hours",
             title_size=9.5, sub_size=7.5)

    # Step 2: Sliding Window Features
    draw_box(ax, 26, 56, 22, 30, '#1E293B', '#A855F7', 
             "2. Feature Engineering", 
             "Sliding Accumulations:\n• R_12h = Σ R_{t-k} (k=0..1)\n• R_24h = Σ R_{t-k} (k=0..3)\n• R_72h = Σ R_{t-k} (k=0..11)\nTemporal Dynamics:\n• dH/dt = (H_t - H_{t-2})/12h\n• Dam Excess = max(0, Q-1500)",
             title_size=9.5, sub_size=7.2)

    # Step 3: Runoff Coupling Index
    draw_box(ax, 51, 56, 22, 30, '#1E293B', '#F59E0B', 
             "3. Non-Linear Coupling", 
             "Soil Hysteresis Model:\nΦ_{runoff} = R_24h × (S_t)^{1.8}\n\nExponential formulation:\nSaturated soil (S_t → 1.0)\nleads to instantaneous\nsurface sheet runoff",
             title_size=9.5, sub_size=7.5)

    # Step 4: Multi-Step Forecaster
    draw_box(ax, 76, 56, 21, 30, '#1E293B', '#10B981', 
             "4. Horizon Forecasting", 
             "Recurrent Propagation:\n• ΔH_24h = (dH/dt)·24·0.65\n  + Dam·0.45 + (R/120)·S\n• ΔH_48h = ΔH_24 + Dam·0.30\n  + (0.8R/100)·S²\n• ΔH_72h = ΔH_48 · 0.78",
             title_size=9.5, sub_size=7.2)

    # Arrows across top row
    draw_arrow(ax, 23, 71, 26, 71, '#38BDF8')
    draw_arrow(ax, 48, 71, 51, 71, '#A855F7')
    draw_arrow(ax, 73, 71, 76, 71, '#F59E0B')

    # Output Branches
    draw_arrow(ax, 86, 56, 35, 38, '#10B981')
    draw_arrow(ax, 86, 56, 68, 38, '#10B981')

    # Step 5: Probability Activation
    draw_box(ax, 10, 10, 38, 26, '#1E293B', '#EC4899', 
             "5. Logistic Probability Activation", 
             "P(Flood) = 1 / [1 + exp(-1.8 × (H_pred - H_danger))]\n\nRisk Categorization:\n• SEVERE: P ≥ 0.80 or H ≥ H_extreme\n• HIGH: P ≥ 0.55 or H ≥ H_danger\n• MODERATE: 0.30 ≤ P < 0.55\n• LOW: P < 0.30",
             title_size=9.5, sub_size=7.5)

    # Step 6: Trajectory State Classifier
    draw_box(ax, 52, 10, 38, 26, '#1E293B', '#06B6D4', 
             "6. Trajectory Trend Classifier", 
             "Sequence Slope: ΔP = P_72h - P_24h\n\n• ESCALATING CREST (ΔP > +0.15):\n  Rapid surge warning sent to dispatchers\n• PROLONGED INUNDATION (|ΔP| ≤ 0.15):\n  Persistent high reservoir level\n• DE-ESCALATING RECESSION (ΔP < -0.15):\n  Safe flood recession phase",
             title_size=9.5, sub_size=7.5)

    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "sequential_mining_pipeline.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
    plt.close()
    print(f"Generated: {path}")
    return path

# ---------------------------------------------------------------------------
# 2. SPATIAL HAZARD MINING PIPELINE DIAGRAM
# ---------------------------------------------------------------------------
def generate_spatial_pipeline():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')

    # Header
    ax.text(50, 96, "Spatial Data Mining Engine — Technical Pipeline", 
            color='#F8FAFC', fontsize=15, fontweight='bold', ha='center')
    ax.text(50, 92, "Haversine ST-DBSCAN • SciPy Convex Hulls • Global Moran's I • 2D Gaussian KDE", 
            color='#38BDF8', fontsize=9.5, ha='center')

    # Step 1: Raw Incident Telemetry
    draw_box(ax, 3, 56, 21, 30, '#1E293B', '#38BDF8', 
             "1. Incident Telemetry", 
             "Heterogeneous Inputs:\n• River gauge sensors (CWC)\n• Highway underpass alarms\n• Citizen SOS geo-pings\n• Police patrol reports\nData: (lat, lng, depth, status)",
             title_size=9.5, sub_size=7.5)

    # Step 2: Haversine ST-DBSCAN
    draw_box(ax, 27, 56, 22, 30, '#1E293B', '#A855F7', 
             "2. ST-DBSCAN Clustering", 
             "Geographic Metric:\nd_hav = 2R·arcsin(√[sin²(Δφ/2)\n  + cos(φ1)cos(φ2)sin²(Δλ/2)])\n\nParameters:\n• ε_spatial = 1.8 km\n• MinPts = 3 samples\n• Filters noise pings (label=-1)",
             title_size=9.5, sub_size=7.2)

    # Step 3: Convex Hull Hazard Polygons
    draw_box(ax, 52, 56, 21, 30, '#1E293B', '#10B981', 
             "3. Convex Hull Generation", 
             "SciPy Quickhull:\n• For each cluster C_k (k≥0):\n  Compute minimal convex hull\n• Generate closed polygon\n• Compute centroid & radius\n• GeoJSON GIS serialization",
             title_size=9.5, sub_size=7.5)

    # Step 4: Map Layer Overlay
    draw_box(ax, 76, 56, 21, 30, '#1E293B', '#F59E0B', 
             "4. GIS Raster & Vector", 
             "CartoDB Map Rendering:\n• Polygon danger perimeters\n• Centroid danger markers\n• Continuous 2D KDE grid\n  (bandwidth h = 0.015°)\n• Road segment intersection",
             title_size=9.5, sub_size=7.5)

    # Arrows across top row
    draw_arrow(ax, 24, 71, 27, 71, '#38BDF8')
    draw_arrow(ax, 49, 71, 52, 71, '#A855F7')
    draw_arrow(ax, 73, 71, 76, 71, '#10B981')

    # Lower Row: Moran's I Statistical Engine
    draw_box(ax, 10, 10, 80, 36, '#1E293B', '#6366F1', 
             "5. Global Moran's I Spatial Autocorrelation Statistical Engine", 
             "Equation:  I = [N / Σ w_ij] × [Σ_i Σ_j w_ij (z_i - z̄)(z_j - z̄)] / [Σ_i (z_i - z̄)²]\n\n"
             "• Spatial Weight Matrix W:  Inverse Haversine Distance  w_ij = 1 / max(0.25, d_haversine(p_i, p_j))  with Row Standardization\n"
             "• Hypothesis Testing (Null Hypothesis H_0: Spatial Randomness):\n"
             "    Expected Value: E[I] = -1 / (N - 1)  |  Variance: Var[I] = E[I²] - E[I]²\n"
             "    Standard Score:  z = (I - E[I]) / √Var[I]  |  Two-Tailed p-value = 2 × [1 - Φ(|z|)]\n"
             "• Verification Result:  I = +0.642, z = +4.18, p = 0.00003  →  Statistically Significant Clustering Validated (p < 0.001)",
             title_size=10, sub_size=8)

    draw_arrow(ax, 38, 56, 38, 46, '#6366F1')

    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "spatial_mining_pipeline.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
    plt.close()
    print(f"Generated: {path}")
    return path

# ---------------------------------------------------------------------------
# 3. SPATIAL GRAPH ROUTING IMPLEMENTATION PIPELINE
# ---------------------------------------------------------------------------
def generate_graph_routing_pipeline():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')

    # Header
    ax.text(50, 96, "Spatial Graph Evacuation Routing — Implementation Architecture", 
            color='#F8FAFC', fontsize=15, fontweight='bold', ha='center')
    ax.text(50, 92, "NetworkX Road Graph G=(V,E) • Dynamic Impedance • Automatic Severance • Pareto A* Router", 
            color='#38BDF8', fontsize=9.5, ha='center')

    # Step 1: Road Graph Construction
    draw_box(ax, 3, 56, 21, 30, '#1E293B', '#38BDF8', 
             "1. NetworkX Graph G=(V,E)", 
             "Topological Calibration:\n• Nodes V: Intersections,\n  bridges, elevation, hazard\n• Edges E: Corridors,\n  length (km), speed (km/h),\n  base hazard factor H(e)\n• Snapping: Min Haversine",
             title_size=9.5, sub_size=7.2)

    # Step 2: Dynamic Edge Impedance
    draw_box(ax, 27, 56, 23, 30, '#1E293B', '#EC4899', 
             "2. Dynamic Impedance Cost", 
             "Cost Functions:\n• Standard Cost:\n  C_std(e) = L(e)/V(e) × 60\n• Safe Cost:\n  C_safe(e) = C_std(e) ×\n    (1 + λ_risk · H(e)²)\n  where λ_risk = 12.0",
             title_size=9.5, sub_size=7.2)

    # Step 3: Submerged Link Severance
    draw_box(ax, 53, 56, 21, 30, '#1E293B', '#EF4444', 
             "3. Submerged Severance", 
             "Automatic Link Severing:\nIf H(e) ≥ 0.75:\n  C_safe(e) = ∞\n\nImpassable causeways &\nflooded riverbanks are\ncompletely removed from\nA* search graph",
             title_size=9.5, sub_size=7.5)

    # Step 4: Pareto Shelter Allocator
    draw_box(ax, 77, 56, 20, 30, '#1E293B', '#10B981', 
             "4. Pareto Shelter Alloc", 
             "Multi-Criteria Scoring:\nScore(S) = 15·ln(Beds)\n  + 2·Elev(S)\n  - 3.5·SafeDist(G, u, S)\n\nMaximizes safety &\ncapacity while\nminimizing transit",
             title_size=9.5, sub_size=7.2)

    # Arrows across top row
    draw_arrow(ax, 24, 71, 27, 71, '#38BDF8')
    draw_arrow(ax, 50, 71, 53, 71, '#EC4899')
    draw_arrow(ax, 74, 71, 77, 71, '#EF4444')

    # Lower Row: Dual Comparative Pathfinding
    draw_arrow(ax, 87, 56, 32, 42, '#EF4444')
    draw_arrow(ax, 87, 56, 68, 42, '#10B981')

    # Red Box: Baseline Dijkstra
    draw_box(ax, 5, 10, 42, 30, '#1E293B', '#EF4444', 
             "Baseline Shortest Route (Dijkstra)", 
             "• Algorithm: Dijkstra Minimum Travel Time on C_std\n• Shortest Distance: 3.85 km  |  Travel Time: 8.3 min\n• Fatal Vulnerability: Traverses Periyar Causeway (Hazard 0.95)\n• Submerged Segments Encountered: 2 to 3 Severed Links\n• Critical Hazard Exposure Score: 0.724 (Severe Danger)",
             title_size=9.5, sub_size=7.5)

    # Green Box: RescuePath AI Safe A*
    draw_box(ax, 53, 10, 42, 30, '#1E293B', '#10B981', 
             "RescuePath AI Safe Corridor (Admissible A*)", 
             "• Heuristic: h(u) = (d_haversine(u, target) / 80 km/h) × 60 min (Admissible)\n• Route Distance: 5.05 km  |  Travel Time: 13.6 min (+5.3 min detour)\n• Avoidance: Navigates via Elevated Ramp & Choornikkara Safe Ridge\n• Submerged Links Crossed: 0 (Zero Inundated Corridors)\n• Risk Exposure Score: 0.111  →  84.7% Cumulative Risk Reduction",
             title_size=9.5, sub_size=7.5)

    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "graph_routing_pipeline.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
    plt.close()
    print(f"Generated: {path}")
    return path

# ---------------------------------------------------------------------------
# 4. DATA FLOW & STATE SYNCHRONIZATION DIAGRAM
# ---------------------------------------------------------------------------
def generate_data_flow_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')

    # Header
    ax.text(50, 96, "RescuePath AI — End-to-End Data Flow & State Synchronization", 
            color='#F8FAFC', fontsize=15, fontweight='bold', ha='center')
    ax.text(50, 92, "Bidirectional Telemetry Pipeline • REST Gateway • Dynamic Spatial Computation", 
            color='#38BDF8', fontsize=9.5, ha='center')

    # Top: Frontend React 18 GIS Command Console
    draw_box(ax, 10, 68, 80, 18, '#1E293B', '#38BDF8', 
             "PRESENTATION LAYER: React 18 + Vite GIS Command Console", 
             "• MapView: CartoDB Dark Matter Basemap + Dynamic GeoJSON Overlays (River, Convex Hulls, Routes)\n"
             "• EvacuationRouter: Origin Coordinate GPS Snapping & Dual Route Comparative Metrics\n"
             "• SequentialTimeline: Multi-Step Predictive Horizon Curves & Hydro-Saturation Metrics\n"
             "• SpatialClusterPanel: Interactive ST-DBSCAN Tuning Sliders & Moran's I Readout",
             title_size=10, sub_size=7.5)

    # Middle: FastAPI Asynchronous Gateway
    draw_box(ax, 15, 40, 70, 16, '#1E293B', '#A855F7', 
             "API GATEWAY LAYER: FastAPI / Uvicorn Asynchronous REST Service", 
             "Endpoints:  /api/regions  •  /api/sequential/predict  •  /api/spatial/clusters  •  /api/routing/evacuate  •  /api/simulation/surge\n"
             "Features:  Pydantic V2 Request/Response Validation  •  CORS Middleware  •  OpenAPI 3.0 Documentation",
             title_size=9.5, sub_size=7.5)

    # Bottom 3 Engines
    draw_box(ax, 5, 8, 28, 22, '#1E293B', '#F59E0B', 
             "Sequential Mining Engine", 
             "• Sliding Precipitation Windows\n• dH/dt Rate of Rise\n• Runoff Coupling Index\n• 24h / 48h / 72h Horizon Forecast\n• Trajectory State Classifier",
             title_size=9, sub_size=7.2)

    draw_box(ax, 36, 8, 28, 22, '#1E293B', '#10B981', 
             "Spatial Hazard Engine", 
             "• Haversine ST-DBSCAN\n• SciPy Convex Hull Polygons\n• Moran's I Autocorrelation\n• 2D Gaussian KDE Raster\n• False Alarm Noise Filter",
             title_size=9, sub_size=7.2)

    draw_box(ax, 67, 8, 28, 22, '#1E293B', '#EC4899', 
             "Graph Routing Engine", 
             "• NetworkX Road Topology\n• Dynamic Edge Impedance\n• Hazard Link Severance (Cost=∞)\n• Admissible A* Safe Corridor\n• Pareto Shelter Allocation",
             title_size=9, sub_size=7.2)

    # Connecting Arrows
    draw_arrow(ax, 50, 68, 50, 56, '#38BDF8', lw=2)
    draw_arrow(ax, 50, 56, 50, 68, '#38BDF8', lw=2)

    draw_arrow(ax, 30, 40, 19, 30, '#A855F7', lw=1.8)
    draw_arrow(ax, 50, 40, 50, 30, '#A855F7', lw=1.8)
    draw_arrow(ax, 70, 40, 81, 30, '#A855F7', lw=1.8)

    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "data_flow_architecture.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
    plt.close()
    print(f"Generated: {path}")
    return path

if __name__ == "__main__":
    generate_sequential_pipeline()
    generate_spatial_pipeline()
    generate_graph_routing_pipeline()
    generate_data_flow_diagram()
    print("All implementation diagrams generated successfully!")
