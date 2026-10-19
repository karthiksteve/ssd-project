import React, { useEffect } from 'react';
import { 
  MapContainer, 
  TileLayer, 
  Polyline, 
  Polygon, 
  CircleMarker, 
  Marker, 
  Popup, 
  useMapEvents,
  useMap
} from 'react-leaflet';
import L from 'leaflet';
import { Layers, ShieldCheck, AlertOctagon, Navigation, Home } from 'lucide-react';

// Fix standard Leaflet icon paths in React/Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// CartoDB Dark Matter tile endpoint with API key
const CARTO_API_KEY = import.meta.env.VITE_CARTO_API_KEY || 'cb1_3gyo_1_98d440b4d5b360f9ae5a96f4';
const TILE_URL = CARTO_API_KEY
  ? `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=${CARTO_API_KEY}`
  : 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';

// Helper component to handle map clicks & center changes
function MapEventHandler({ onMapClick, center, zoom }) {
  const map = useMap();

  useEffect(() => {
    if (center) {
      map.setView([center.lat, center.lng], zoom || 13, { animate: true });
    }
  }, [center, zoom, map]);

  useMapEvents({
    click(e) {
      if (onMapClick) {
        onMapClick(e.latlng);
      }
    }
  });

  return null;
}

export default function MapView({
  regionCenter,
  riverData,
  roadNetwork,
  clustersData,
  shelters,
  routeData,
  startLocation,
  onMapClick,
  activeLayerToggles
}) {
  const centerLat = regionCenter?.lat || 10.1076;
  const centerLng = regionCenter?.lng || 76.3516;

  // Convert GeoJSON coordinates [lng, lat] to Leaflet [lat, lng]
  const riverCoords = riverData?.geojson?.coordinates?.map(c => [c[1], c[0]]) || [];

  const safeRouteCoords = routeData?.safe_route?.geojson_line?.coordinates?.map(c => [c[1], c[0]]) || [];
  const stdRouteCoords = routeData?.standard_route?.geojson_line?.coordinates?.map(c => [c[1], c[0]]) || [];

  return (
    <div className="map-viewport-container">
      <MapContainer
        center={[centerLat, centerLng]}
        zoom={13}
        className="map-element"
        zoomControl={true}
      >
        <MapEventHandler 
          onMapClick={onMapClick} 
          center={regionCenter} 
          zoom={13} 
        />

        {/* Dark Matter CartoDB Basemap for Command Center Aesthetic */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url={TILE_URL}
          maxZoom={19}
        />

        {/* Primary River Channel Vector */}
        {activeLayerToggles.river && riverCoords.length > 0 && (
          <Polyline
            positions={riverCoords}
            pathOptions={{
              color: '#0284c7',
              weight: 8,
              opacity: 0.85,
              dashArray: '2, 6'
            }}
          >
            <Popup>
              <div style={{ padding: '6px' }}>
                <strong style={{ color: '#38bdf8' }}>{riverData?.river_name || 'River Channel'}</strong>
                <p style={{ fontSize: '0.78rem', color: '#cbd5e1', marginTop: '4px' }}>
                  Current Flow Status: High discharge / flood stage
                </p>
              </div>
            </Popup>
          </Polyline>
        )}

        {/* Road Network Graph Segments */}
        {activeLayerToggles.roads && roadNetwork?.edges?.map((edge, idx) => {
          const coords = edge.coordinates.map(c => [c[1], c[0]]);
          const hazard = edge.hazard_factor || 0.0;
          let color = '#34d399'; // Safe green
          if (hazard > 0.7) color = '#ef4444'; // Red
          else if (hazard > 0.35) color = '#f59e0b'; // Amber

          return (
            <Polyline
              key={`road-${idx}`}
              positions={coords}
              pathOptions={{
                color: color,
                weight: hazard > 0.7 ? 4 : 2.5,
                opacity: 0.65
              }}
            >
              <Popup>
                <div style={{ fontSize: '0.78rem' }}>
                  <strong>{edge.road_name}</strong>
                  <br />
                  Length: {edge.length_km} km | Speed: {edge.speed_kmh} km/h
                  <br />
                  Hazard Index: {(hazard * 100).toFixed(0)}%
                </div>
              </Popup>
            </Polyline>
          );
        })}

        {/* Spatial DBSCAN Hazard Cluster Polygons */}
        {activeLayerToggles.clusters && clustersData?.clusters?.map((cluster) => {
          const hullLatLngs = cluster.hull_coordinates.map(c => [c[1], c[0]]);
          const isCritical = cluster.hazard_level === 'CRITICAL';

          return (
            <Polygon
              key={`cluster-${cluster.cluster_id}`}
              positions={hullLatLngs}
              pathOptions={{
                color: isCritical ? '#dc2626' : '#d97706',
                fillColor: isCritical ? '#ef4444' : '#f59e0b',
                fillOpacity: 0.32,
                weight: 2,
                dashArray: '4, 4'
              }}
            >
              <Popup>
                <div style={{ padding: '6px' }}>
                  <span className={`badge-status ${isCritical ? 'severe' : 'high'}`}>
                    DBSCAN Cluster #{cluster.cluster_id + 1} ({cluster.hazard_level})
                  </span>
                  <div style={{ marginTop: '8px', fontSize: '0.8rem', lineHeight: '1.4' }}>
                    <p>Mean Water Depth: <strong>{cluster.avg_water_depth_cm} cm</strong></p>
                    <p>Radius: <strong>{cluster.radius_km} km</strong></p>
                    <p>Telemetry Points: <strong>{cluster.points_count}</strong></p>
                    <p style={{ color: '#f87171', marginTop: '4px', fontSize: '0.74rem' }}>
                      Avoided by RescuePath AI routing algorithm.
                    </p>
                  </div>
                </div>
              </Popup>
            </Polygon>
          );
        })}

        {/* Flood Telemetry / Incident Sensor Markers */}
        {activeLayerToggles.sensors && clustersData?.points?.map((pt) => {
          const isCritical = pt.water_depth_cm >= 100;
          return (
            <CircleMarker
              key={pt.id}
              center={[pt.lat, pt.lng]}
              radius={6}
              pathOptions={{
                color: isCritical ? '#ffffff' : '#f59e0b',
                fillColor: isCritical ? '#ef4444' : '#f59e0b',
                fillOpacity: 0.9,
                weight: 1.5
              }}
            >
              <Popup>
                <div style={{ fontSize: '0.78rem' }}>
                  <strong>{pt.source}</strong>
                  <p>Recorded Inundation: <strong>{pt.water_depth_cm} cm</strong></p>
                  <p>Severity: <span style={{ color: isCritical ? '#f87171' : '#fbbf24' }}>{pt.severity}</span></p>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}

        {/* Relief Shelters Markers */}
        {activeLayerToggles.shelters && shelters?.map((shelter) => {
          const occPercent = Math.round((shelter.current_occupancy / shelter.total_capacity) * 100);
          const isFull = shelter.available_beds <= 50;

          return (
            <CircleMarker
              key={shelter.id}
              center={[shelter.lat, shelter.lng]}
              radius={10}
              pathOptions={{
                color: '#ffffff',
                fillColor: isFull ? '#f59e0b' : '#10b981',
                fillOpacity: 0.95,
                weight: 2
              }}
            >
              <Popup>
                <div style={{ padding: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                    <Home size={16} color="#10b981" />
                    <strong>{shelter.name}</strong>
                  </div>
                  <div style={{ fontSize: '0.78rem', lineHeight: '1.4' }}>
                    <p>Elevation: <strong>{shelter.elevation_m}m (Safe High Ground)</strong></p>
                    <p>Occupancy: <strong>{shelter.current_occupancy} / {shelter.total_capacity} ({occPercent}%)</strong></p>
                    <p>Available Beds: <strong style={{ color: '#34d399' }}>{shelter.available_beds}</strong></p>
                    <p>Food Packs: <strong>{shelter.food_packs_available}</strong></p>
                    <p>Medical Staff: <strong>{shelter.medical_staff_present ? 'Yes' : 'Dispatched'}</strong></p>
                    <p style={{ marginTop: '4px', color: '#94a3b8' }}>Helpline: {shelter.contact_phone}</p>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}

        {/* Standard Unsafe Evacuation Route (Red Dashed Line) */}
        {stdRouteCoords.length > 0 && (
          <Polyline
            positions={stdRouteCoords}
            pathOptions={{
              color: '#ef4444',
              weight: 4,
              opacity: 0.8,
              dashArray: '8, 8'
            }}
          >
            <Popup>
              <div style={{ fontSize: '0.78rem', color: '#f87171' }}>
                <strong>Standard Shortest Route (Unsafe)</strong>
                <p>Traverses submerged danger corridors.</p>
                <p>Risk Score: {routeData.standard_route.risk_exposure_score}</p>
              </div>
            </Popup>
          </Polyline>
        )}

        {/* RescuePath AI Safe Route (Solid Glowing Green Line) */}
        {safeRouteCoords.length > 0 && (
          <Polyline
            positions={safeRouteCoords}
            pathOptions={{
              color: '#10b981',
              weight: 6,
              opacity: 0.95
            }}
          >
            <Popup>
              <div style={{ fontSize: '0.78rem', color: '#34d399' }}>
                <strong>RescuePath AI Safe Route (Recommended)</strong>
                <p>Bypasses high-risk clusters via safe elevated roads.</p>
                <p>Est. Time: {routeData.safe_route.estimated_time_min} min</p>
              </div>
            </Popup>
          </Polyline>
        )}

        {/* User Evacuee Origin Point Marker */}
        {startLocation && (
          <CircleMarker
            center={[startLocation.lat, startLocation.lng]}
            radius={8}
            pathOptions={{
              color: '#ffffff',
              fillColor: '#38bdf8',
              fillOpacity: 1,
              weight: 2
            }}
          >
            <Popup>
              <div style={{ fontSize: '0.78rem' }}>
                <strong>Evacuee Origin</strong>
                <p>Click elsewhere on the map to relocate start position.</p>
              </div>
            </Popup>
          </CircleMarker>
        )}
      </MapContainer>

      {/* Floating Instructions & Legend on Bottom Left */}
      <div className="map-hud-bottom">
        <div className="glass-panel" style={{ padding: '10px 16px', display: 'inline-flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
            <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#38bdf8', display: 'inline-block' }}></span>
            <span>Evacuee Origin (Click Map)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
            <span style={{ width: '16px', height: '4px', background: '#10b981', display: 'inline-block' }}></span>
            <span>RescuePath Safe Corridor</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
            <span style={{ width: '16px', height: '4px', background: '#ef4444', borderTop: '2px dashed #ef4444', display: 'inline-block' }}></span>
            <span>Unsafe Standard Route</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
            <span style={{ width: '12px', height: '12px', borderRadius: '2px', background: 'rgba(239, 68, 68, 0.4)', border: '1px solid #ef4444', display: 'inline-block' }}></span>
            <span>DBSCAN Hazard Zone</span>
          </div>
        </div>
      </div>
    </div>
  );
}
