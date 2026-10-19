import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import MapView from './components/MapView';
import SequentialTimeline from './components/SequentialTimeline';
import SpatialClusterPanel from './components/SpatialClusterPanel';
import EvacuationRouter from './components/EvacuationRouter';
import ShelterDirectory from './components/ShelterDirectory';
import SimulationControls from './components/SimulationControls';
import { apiService } from './services/api';
import { 
  Navigation, 
  Clock, 
  Network, 
  Home, 
  Flame, 
  Layers, 
  Eye, 
  EyeOff,
  AlertCircle 
} from 'lucide-react';

export default function App() {
  const [regionId, setRegionId] = useState('kerala_ernakulam');
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('route'); // 'route', 'sequential', 'spatial', 'shelters', 'simulation'

  // SSDM Data states
  const [sequentialData, setSequentialData] = useState(null);
  const [clustersData, setClustersData] = useState(null);
  const [roadNetwork, setRoadNetwork] = useState(null);
  const [riverData, setRiverData] = useState(null);
  const [shelters, setShelters] = useState([]);
  const [simulationStatus, setSimulationStatus] = useState(null);

  // Evacuation Routing state
  const [startLocation, setStartLocation] = useState({ lat: 10.1085, lng: 76.3535 }); // Aluva Manappuram
  const [selectedShelterId, setSelectedShelterId] = useState(null);
  const [routeData, setRouteData] = useState(null);

  // DBSCAN tuning state
  const [epsKm, setEpsKm] = useState(1.8);
  const [minSamples, setMinSamples] = useState(3);

  // Map layer visibility toggles
  const [activeLayerToggles, setActiveLayerToggles] = useState({
    river: true,
    roads: true,
    clusters: true,
    sensors: true,
    shelters: true
  });

  // Load regions on mount
  useEffect(() => {
    apiService.getRegions()
      .then(res => setRegions(res))
      .catch(err => console.error('Error fetching regions:', err));
  }, []);

  const REGION_DEFAULT_STARTS = {
    kerala_ernakulam: { lat: 10.1085, lng: 76.3535 },
    assam_guwahati: { lat: 26.1850, lng: 91.7450 }
  };

  // Fetch all regional data
  const loadAllData = async (currentRegion = regionId) => {
    setLoading(true);
    try {
      const activeStart = REGION_DEFAULT_STARTS[currentRegion] || { lat: 10.1085, lng: 76.3535 };
      setStartLocation(activeStart);
      setSelectedShelterId(null);

      const [seq, spat, roads, river, camps, sim] = await Promise.all([
        apiService.getSequentialPrediction(currentRegion),
        apiService.getSpatialClusters(currentRegion, epsKm, minSamples),
        apiService.getRoadNetwork(currentRegion),
        apiService.getRiverGeometry(currentRegion),
        apiService.getShelters(currentRegion),
        apiService.getSimulationStatus(currentRegion)
      ]);

      setSequentialData(seq);
      setClustersData(spat);
      setRoadNetwork(roads);
      setRiverData(river);
      setShelters(camps);
      setSimulationStatus(sim);

      // Automatically compute initial evacuation route from active start location
      const routeRes = await apiService.calculateEvacuationRoute(
        currentRegion,
        activeStart.lat,
        activeStart.lng,
        null
      );
      setRouteData(routeRes);
    } catch (err) {
      console.error('Failed to load platform data:', err);
    } finally {
      setLoading(false);
    }
  };

  // Trigger data load when region changes
  useEffect(() => {
    loadAllData(regionId);
  }, [regionId]);

  // Handle map click to update evacuee origin
  const handleMapClick = async (latlng) => {
    const newStart = { lat: latlng.lat, lng: latlng.lng };
    setStartLocation(newStart);
    try {
      const routeRes = await apiService.calculateEvacuationRoute(
        regionId,
        newStart.lat,
        newStart.lng,
        selectedShelterId
      );
      setRouteData(routeRes);
    } catch (err) {
      console.error('Error recalculating route from click:', err);
    }
  };

  // Re-run routing calculation on demand
  const handleCalculateRoute = async () => {
    setLoading(true);
    try {
      const routeRes = await apiService.calculateEvacuationRoute(
        regionId,
        startLocation.lat,
        startLocation.lng,
        selectedShelterId
      );
      setRouteData(routeRes);
    } catch (err) {
      console.error('Routing failed:', err);
    } finally {
      setLoading(false);
    }
  };

  // Re-run DBSCAN clustering with updated hyperparams
  const handleRecalculateClusters = async () => {
    setLoading(true);
    try {
      const spat = await apiService.getSpatialClusters(regionId, epsKm, minSamples);
      setClustersData(spat);
    } catch (err) {
      console.error('Clustering update failed:', err);
    } finally {
      setLoading(false);
    }
  };

  // Trigger simulated disaster event
  const handleTriggerSimulation = async (scenario, intensity) => {
    setLoading(true);
    try {
      const res = await apiService.triggerSimulation(regionId, scenario, intensity);
      // Reload affected layers
      await loadAllData(regionId);
      return res;
    } finally {
      setLoading(false);
    }
  };

  // Toggle map layer visibility
  const toggleLayer = (layerKey) => {
    setActiveLayerToggles(prev => ({ ...prev, [layerKey]: !prev[layerKey] }));
  };

  const currentRegionMeta = regions.find(r => r.id === regionId);

  return (
    <div className="app-container">
      <Header
        regionId={regionId}
        setRegionId={setRegionId}
        regions={regions}
        simulationStatus={simulationStatus}
        onRefresh={() => loadAllData(regionId)}
        loading={loading}
      />

      <div className="workspace-layout">
        {/* Left Operations Control Sidebar */}
        <div className="sidebar">
          {/* Navigation Tabs */}
          <div className="sidebar-tabs">
            <button
              className={`tab-btn ${activeTab === 'route' ? 'active' : ''}`}
              onClick={() => setActiveTab('route')}
            >
              <Navigation size={14} />
              Routing
            </button>
            <button
              className={`tab-btn ${activeTab === 'sequential' ? 'active' : ''}`}
              onClick={() => setActiveTab('sequential')}
            >
              <Clock size={14} />
              Forecast
            </button>
            <button
              className={`tab-btn ${activeTab === 'spatial' ? 'active' : ''}`}
              onClick={() => setActiveTab('spatial')}
            >
              <Network size={14} />
              Clusters
            </button>
            <button
              className={`tab-btn ${activeTab === 'shelters' ? 'active' : ''}`}
              onClick={() => setActiveTab('shelters')}
            >
              <Home size={14} />
              Shelters
            </button>
            <button
              className={`tab-btn ${activeTab === 'simulation' ? 'active' : ''}`}
              onClick={() => setActiveTab('simulation')}
            >
              <Flame size={14} />
              Crisis
            </button>
          </div>

          {/* Active Tab Panel Content */}
          <div className="sidebar-content">
            {activeTab === 'route' && (
              <EvacuationRouter
                regionId={regionId}
                startLocation={startLocation}
                shelters={shelters}
                selectedShelterId={selectedShelterId}
                setSelectedShelterId={setSelectedShelterId}
                routeData={routeData}
                onCalculateRoute={handleCalculateRoute}
                loading={loading}
              />
            )}

            {activeTab === 'sequential' && (
              <SequentialTimeline
                regionId={regionId}
                sequentialData={sequentialData}
              />
            )}

            {activeTab === 'spatial' && (
              <SpatialClusterPanel
                regionId={regionId}
                clustersData={clustersData}
                epsKm={epsKm}
                setEpsKm={setEpsKm}
                minSamples={minSamples}
                setMinSamples={setMinSamples}
                onRecalculate={handleRecalculateClusters}
                loading={loading}
              />
            )}

            {activeTab === 'shelters' && (
              <ShelterDirectory
                regionId={regionId}
                shelters={shelters}
                onSelectShelter={(id) => {
                  setSelectedShelterId(id);
                  setActiveTab('route');
                }}
              />
            )}

            {activeTab === 'simulation' && (
              <SimulationControls
                regionId={regionId}
                simulationStatus={simulationStatus}
                onTriggerSimulation={handleTriggerSimulation}
                loading={loading}
              />
            )}
          </div>
        </div>

        {/* Right Interactive GIS Map View */}
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
          {/* Floating Map Layer Toggles HUD */}
          <div className="map-hud-top">
            <div className="glass-panel" style={{ padding: '6px 12px', display: 'flex', gap: '8px', alignItems: 'center' }}>
              <Layers size={14} color="#94a3b8" />
              <span style={{ fontSize: '0.72rem', color: '#94a3b8', marginRight: '4px' }}>Layers:</span>
              
              <button
                onClick={() => toggleLayer('clusters')}
                style={{
                  background: activeLayerToggles.clusters ? 'rgba(239, 68, 68, 0.2)' : 'transparent',
                  border: `1px solid ${activeLayerToggles.clusters ? '#ef4444' : 'rgba(255,255,255,0.1)'}`,
                  color: activeLayerToggles.clusters ? '#fca5a5' : '#64748b',
                  fontSize: '0.7rem',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                DBSCAN Zones
              </button>

              <button
                onClick={() => toggleLayer('roads')}
                style={{
                  background: activeLayerToggles.roads ? 'rgba(16, 185, 129, 0.2)' : 'transparent',
                  border: `1px solid ${activeLayerToggles.roads ? '#10b981' : 'rgba(255,255,255,0.1)'}`,
                  color: activeLayerToggles.roads ? '#6ee7b7' : '#64748b',
                  fontSize: '0.7rem',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Road Network
              </button>

              <button
                onClick={() => toggleLayer('sensors')}
                style={{
                  background: activeLayerToggles.sensors ? 'rgba(245, 158, 11, 0.2)' : 'transparent',
                  border: `1px solid ${activeLayerToggles.sensors ? '#f59e0b' : 'rgba(255,255,255,0.1)'}`,
                  color: activeLayerToggles.sensors ? '#fcd34d' : '#64748b',
                  fontSize: '0.7rem',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Sensors
              </button>

              <button
                onClick={() => toggleLayer('shelters')}
                style={{
                  background: activeLayerToggles.shelters ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                  border: `1px solid ${activeLayerToggles.shelters ? '#38bdf8' : 'rgba(255,255,255,0.1)'}`,
                  color: activeLayerToggles.shelters ? '#7dd3fc' : '#64748b',
                  fontSize: '0.7rem',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Shelters
              </button>
            </div>
          </div>

          <MapView
            regionCenter={currentRegionMeta?.center}
            riverData={riverData}
            roadNetwork={roadNetwork}
            clustersData={clustersData}
            shelters={shelters}
            routeData={routeData}
            startLocation={startLocation}
            onMapClick={handleMapClick}
            activeLayerToggles={activeLayerToggles}
          />
        </div>
      </div>
    </div>
  );
}
