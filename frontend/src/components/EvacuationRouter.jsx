import React from 'react';
import { Navigation, ShieldCheck, AlertTriangle, ArrowRight, MapPin, CheckCircle, Crosshair, FileDown } from 'lucide-react';
import { apiService } from '../services/api';

export default function EvacuationRouter({
  regionId = 'kerala_ernakulam',
  startLocation,
  shelters,
  selectedShelterId,
  setSelectedShelterId,
  routeData,
  onCalculateRoute,
  loading
}) {
  const safe = routeData?.safe_route;
  const std = routeData?.standard_route;

  const handleDownloadManifest = () => {
    if (!startLocation) return;
    apiService.downloadDispatchManifest(
      regionId,
      startLocation.lat,
      startLocation.lng,
      selectedShelterId
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Navigation size={18} color="#10b981" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Evacuation Corridor Engine</h3>
        </div>
        <span className="badge-status safe" style={{ fontSize: '0.68rem' }}>
          A* + Risk Impedance
        </span>
      </div>

      {/* Start Location & Target Selection Card */}
      <div className="glass-panel" style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div>
          <span className="metric-label" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <MapPin size={14} color="#38bdf8" />
            Evacuee Origin Position
          </span>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px' }}>
            <span style={{ fontSize: '0.8rem', color: '#f8fafc', fontFamily: 'var(--font-mono)' }}>
              {startLocation ? `${startLocation.lat.toFixed(4)}°N, ${startLocation.lng.toFixed(4)}°E` : '10.1085°N, 76.3535°E'}
            </span>
            <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
              (Click map to adjust)
            </span>
          </div>
        </div>

        <div>
          <span className="metric-label">Designated Relief Shelter</span>
          <select 
            className="select-custom" 
            style={{ width: '100%', marginTop: '4px' }}
            value={selectedShelterId || ''}
            onChange={(e) => setSelectedShelterId(e.target.value || null)}
          >
            <option value="">-- Auto-Allocate Optimal Safe Shelter --</option>
            {shelters.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.available_beds} beds free)
              </option>
            ))}
          </select>
        </div>

        <button 
          className="btn-primary" 
          onClick={onCalculateRoute}
          disabled={loading}
          style={{ justifyContent: 'center', marginTop: '4px', background: 'linear-gradient(135deg, #059669, #10b981)' }}
        >
          <Crosshair size={15} />
          Compute Evacuation Corridors
        </button>
      </div>

      {/* Route Comparison Analytics */}
      {routeData && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Risk Reduction Banner */}
          <div 
            style={{ 
              background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.25))',
              border: '1px solid rgba(16, 185, 129, 0.4)',
              borderRadius: '10px',
              padding: '12px 14px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <ShieldCheck size={24} color="#34d399" />
              <div>
                <strong style={{ fontSize: '0.86rem', color: '#f0fdf4' }}>
                  {routeData.risk_reduction_percentage}% Flood Risk Avoided
                </strong>
                <p style={{ fontSize: '0.72rem', color: '#a7f3d0', marginTop: '2px' }}>
                  Detour Delta: +{routeData.travel_time_difference_min.toFixed(1)} mins
                </p>
              </div>
            </div>
          </div>

          {/* Comparison Cards: Safe vs Standard */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            {/* RescuePath Safe Corridor */}
            <div 
              style={{ 
                background: 'rgba(6, 78, 59, 0.35)', 
                border: '1px solid rgba(16, 185, 129, 0.35)', 
                borderRadius: '8px', 
                padding: '12px' 
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                <CheckCircle size={14} color="#34d399" />
                <strong style={{ fontSize: '0.78rem', color: '#34d399' }}>RescuePath Route</strong>
              </div>
              <p style={{ fontSize: '0.75rem', color: '#e2e8f0' }}>Distance: <strong>{safe?.total_distance_km} km</strong></p>
              <p style={{ fontSize: '0.75rem', color: '#e2e8f0' }}>Time: <strong>{safe?.estimated_time_min} min</strong></p>
              <p style={{ fontSize: '0.75rem', color: '#a7f3d0' }}>Hazard Index: <strong>{(safe?.risk_exposure_score * 100).toFixed(0)}%</strong></p>
              <p style={{ fontSize: '0.7rem', color: '#34d399', marginTop: '4px' }}>Submerged Segments: 0</p>
            </div>

            {/* Standard Route */}
            <div 
              style={{ 
                background: 'rgba(127, 29, 29, 0.25)', 
                border: '1px solid rgba(239, 68, 68, 0.35)', 
                borderRadius: '8px', 
                padding: '12px' 
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                <AlertTriangle size={14} color="#f87171" />
                <strong style={{ fontSize: '0.78rem', color: '#f87171' }}>Standard Route</strong>
              </div>
              <p style={{ fontSize: '0.75rem', color: '#e2e8f0' }}>Distance: <strong>{std?.total_distance_km} km</strong></p>
              <p style={{ fontSize: '0.75rem', color: '#e2e8f0' }}>Time: <strong>{std?.estimated_time_min} min</strong></p>
              <p style={{ fontSize: '0.75rem', color: '#fca5a5' }}>Hazard Index: <strong>{(std?.risk_exposure_score * 100).toFixed(0)}%</strong></p>
              <p style={{ fontSize: '0.7rem', color: '#f87171', marginTop: '4px' }}>
                Submerged Segments: <strong>{std?.submerged_segments_encountered}</strong>
              </p>
            </div>
          </div>

          {/* Export Dispatch Brief Button */}
          <button
            onClick={handleDownloadManifest}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              padding: '10px 14px',
              background: 'rgba(30, 41, 59, 0.85)',
              border: '1px solid rgba(56, 189, 248, 0.4)',
              borderRadius: '8px',
              color: '#38bdf8',
              fontSize: '0.8rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            <FileDown size={16} />
            Download Official Evacuation Dispatch Manifest
          </button>

          {/* Recommendation Note */}
          <div style={{ fontSize: '0.75rem', color: '#cbd5e1', lineHeight: '1.4', fontStyle: 'italic', background: 'rgba(15, 23, 42, 0.5)', padding: '8px 12px', borderRadius: '6px' }}>
            {routeData.recommendation}
          </div>

          {/* Turn-by-Turn Waypoint Sequence */}
          <div>
            <span className="metric-label" style={{ display: 'block', marginBottom: '8px' }}>
              Safe Corridor Waypoint Sequence
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', maxHeight: '180px', overflowY: 'auto' }}>
              {safe?.waypoints.map((wp, idx) => (
                <div 
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontSize: '0.74rem',
                    background: 'rgba(15, 23, 42, 0.6)',
                    padding: '6px 10px',
                    borderRadius: '6px',
                    borderLeft: `2px solid ${wp.step_hazard_score > 0.5 ? '#f59e0b' : '#10b981'}`
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ color: '#64748b', fontFamily: 'var(--font-mono)', fontSize: '0.68rem' }}>#{idx+1}</span>
                    <span>{wp.road_name}</span>
                  </div>
                  <span style={{ color: '#94a3b8', fontSize: '0.7rem' }}>
                    Elev: {wp.elevation_m}m
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
