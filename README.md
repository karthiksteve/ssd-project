# RescuePath AI: Intelligent Disaster Response & Evacuation Platform
### Sequential and Spatial Data Mining (CSE3068) — Academic Project

**Submitted By:** Karthikeyan A (23MIA1123)  
**Course:** CSE3068 Sequential and Spatial Data Mining (SSDM)

---

## 1. Executive Summary

India experiences devastating recurring floods affecting over 7.5 million hectares annually (NDMA). Conventional disaster response systems operate in silos: meteorologists forecast rainfall, transport departments track roads, and evacuation officials make decisions manually with static, outdated maps.

**RescuePath AI** solves this problem by uniting **Sequential Data Mining** (for 24–72 hour advance predictive hazard forecasting) and **Spatial Data Mining** (for automated hazard clustering, continuous risk heatmaps, and dynamic risk-penalized road evacuation routing) into a unified, production-grade interactive platform.

---

## 2. Core SSDM Algorithmic Pillars

### A. Sequential Data Mining (Time-Series Sequence Prediction)
- **Multi-Step Horizon Forecasting**: Predicts flood probability and river gauge heights at **+24 Hours, +48 Hours, and +72 Hours** from multivariate temporal sequences:
  $$X_t = [\text{Rainfall}_t, \text{Upstream Discharge}_t, \text{Soil Saturation}_t, \text{Gauge Height}_t]$$
- **Sliding-Window Feature Extraction**:
  - Temporal rate of rise: $\Delta \text{Level} / \Delta t$
  - Cumulative rainfall over sliding intervals (12h, 24h, 72h)
  - Non-linear runoff saturation coupling index: $\text{Rain}_{24h} \times (\text{Soil\_Sat})^{1.8}$
- **Trajectory Trend Analysis**: Classifies sequence state into *Escalating Flood Crest*, *Prolonged Inundation*, or *De-escalating Recession*.

### B. Spatial Data Mining (Geographic Clustering & Autocorrelation)
- **Spatio-Temporal DBSCAN (ST-DBSCAN)**:
  - Uses geographic **Haversine distance** ($\varepsilon_{spatial} = 1.8$ km) and $MinPts = 3$ to group telemetry sensors and citizen SOS calls into coherent hazard zones.
  - Automatically isolates and filters out random noise/minor waterlogging outliers.
  - Generates Convex Hull polygon boundaries for real-time GIS rendering.
- **Global Moran's I Spatial Autocorrelation**:
  $$I = \frac{N}{\sum_{ij} w_{ij}} \frac{\sum_{ij} w_{ij}(x_i - \bar{x})(x_j - \bar{x})}{\sum_i (x_i - \bar{x})^2}$$
  Validates whether flood depths are statistically clustered ($I > 0.35, p < 0.05$) across administrative wards versus dispersed randomly.
- **2D Gaussian Kernel Density Estimation (KDE)**:
  Generates a smooth, normalized risk intensity raster surface:
  $$f(x, y) = \frac{1}{n h^2 2\pi} \sum_{i=1}^n \exp\left(-\frac{d((x,y), p_i)^2}{2 h^2}\right)$$

### C. Spatial Graph Mining (Dynamic Evacuation Routing)
- **Road Network Graph**: $G = (V, E)$ constructed via NetworkX, calibrated to real flood basins (e.g., Kerala Periyar Basin / Aluva and Assam Brahmaputra).
- **Dynamic Cost Function (Edge Impedance)**:
  $$\text{Cost}_{standard}(e) = \text{TravelTime}(e)$$
  $$\text{Cost}_{safe}(e) = \text{TravelTime}(e) \times (1 + \lambda_{risk} \times \text{HazardLevel}(e)^2)$$
  Submerged corridors ($\text{HazardLevel} \ge 0.75$) are dynamically severed ($\text{Cost} = \infty$).
- **Pareto-Optimal Safe Navigation**:
  Computes and visually contrasts two paths:
  1. 🔴 **Standard Shortest Path (Dijkstra)**: Traverses hazardous submerged roads.
  2. 🟢 **RescuePath AI Safe Corridor (A\*)**: Navigates around DBSCAN hazard clusters to the optimal high-ground shelter, achieving up to an **85%+ reduction in risk exposure**.

---

## 3. System Architecture

```
                                  +-----------------------------+
                                  |   Web Command Center UI     |
                                  |  (React 18 + Leaflet + Vite)|
                                  +--------------+--------------+
                                                 | REST / JSON
                                                 v
                                  +-----------------------------+
                                  |    FastAPI Python Backend   |
                                  +--------------+--------------+
                                                 |
             +-----------------------------------+-----------------------------------+
             |                                   |                                   |
             v                                   v                                   v
+-------------------------+         +-------------------------+         +-------------------------+
| Sequential Data Mining  |         |   Spatial Data Mining   |         |  Spatial Graph Router   |
| - Multi-step 24/48/72h  |         | - ST-DBSCAN Clustering  |         | - Risk-Penalized A*     |
| - Hydrologic Coupling   |         | - Moran's I Autocorr    |         | - Pareto Shelter Alloc  |
| - Trend Classification  |         | - 2D Gaussian KDE       |         | - Submerged Severance   |
+-------------------------+         +-------------------------+         +-------------------------+
```

---

## 4. Quick Start Guide

### Option 1: Single-Command Master Launcher (Recommended)
Run the root launcher to start both Backend and Frontend concurrently and open your default browser:
```powershell
python run_demo.py
```
- **Web Dashboard**: `http://localhost:5173`
- **Backend API & Swagger Docs**: `http://127.0.0.1:8000/docs`

---

### Option 2: Individual Service Startup

#### 1. Backend (FastAPI)
```powershell
# From project root
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Frontend (Vite + React)
```powershell
cd frontend
npm run dev
```

---

## 5. Running Unit Tests
To verify all sequential, spatial, and graph routing algorithms:
```powershell
python -m pytest backend/tests -v
```
All 9 automated unit tests validate feature extraction, 24/48/72h forecasting, DBSCAN cluster formation, Moran's I boundaries, and A* risk avoidance.

---

## 6. Academic Jupyter Notebook
For live presentation during project review, an interactive exploratory notebook is provided in:
```
notebooks/ssdm_exploratory_analysis.ipynb
```
Contains step-by-step code execution, mathematical formulas, and algorithm outputs.

---

## 7. Technology Stack
- **Languages**: Python 3.11+ / 3.14, JavaScript (ES2022)
- **Geospatial & Graph Mining**: Shapely, NetworkX, Scikit-learn, SciPy
- **Backend API**: FastAPI, Uvicorn, Pydantic
- **Frontend Dashboard**: React 18, Leaflet, React-Leaflet, Lucide Icons, Vite
- **Testing**: PyTest
