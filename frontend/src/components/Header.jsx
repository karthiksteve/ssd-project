import React from 'react';
import { ShieldAlert, Compass, RefreshCw, AlertTriangle } from 'lucide-react';

export default function Header({ 
  regionId, 
  setRegionId, 
  regions, 
  simulationStatus, 
  onRefresh,
  loading 
}) {
  return (
    <header className="header">
      <div className="header-left">
        <div className="logo-badge">
          <div className="logo-icon">
            <ShieldAlert size={22} color="#ffffff" />
          </div>
          <div>
            <h1 className="logo-title">RescuePath AI</h1>
          </div>
        </div>

        <span className="course-badge">CSE3068 Spatial & Sequential Data Mining</span>

        {simulationStatus?.surge_active && (
          <div className="badge-status severe">
            <span className="pulse-indicator" style={{ background: '#ef4444' }}></span>
            <span>CRISIS SIMULATION ACTIVE ({simulationStatus.scenario_name.replace('_', ' ')})</span>
          </div>
        )}
      </div>

      <div className="header-right">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Compass size={16} color="#94a3b8" />
          <select 
            className="select-custom"
            value={regionId}
            onChange={(e) => setRegionId(e.target.value)}
          >
            {regions.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>
        </div>

        <button 
          className="btn-primary" 
          onClick={onRefresh}
          disabled={loading}
          style={{ padding: '8px 12px', fontSize: '0.78rem' }}
          title="Refresh real-time telemetry"
        >
          <RefreshCw size={14} className={loading ? 'spin-anim' : ''} />
          Sync
        </button>
      </div>
    </header>
  );
}
