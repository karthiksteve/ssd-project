import React, { useState } from 'react';
import { Clock, TrendingUp, AlertTriangle, Droplets, Activity, Download } from 'lucide-react';
import { apiService } from '../services/api';

export default function SequentialTimeline({ sequentialData, regionId = 'kerala_ernakulam' }) {
  const [activeHorizon, setActiveHorizon] = useState(24);

  if (!sequentialData) {
    return (
      <div className="glass-panel" style={{ padding: '20px', textAlign: 'center' }}>
        <p style={{ color: '#94a3b8' }}>Loading sequential predictive models...</p>
      </div>
    );
  }

  const handleExportTimeseries = () => {
    apiService.downloadTimeseriesCsv(regionId);
  };

  const forecast = activeHorizon === 24 
    ? sequentialData.forecast_24h 
    : activeHorizon === 48 
      ? sequentialData.forecast_48h 
      : sequentialData.forecast_72h;

  const probPercent = Math.round(forecast.flood_probability * 100);
  const isSevere = forecast.risk_level === 'SEVERE';
  const isHigh = forecast.risk_level === 'HIGH';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Title & Horizon Selector */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Clock size={18} color="#38bdf8" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Sequential Multi-Step Forecast</h3>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            onClick={handleExportTimeseries}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              padding: '4px 10px',
              background: 'rgba(30, 41, 59, 0.8)',
              border: '1px solid rgba(56, 189, 248, 0.4)',
              borderRadius: '6px',
              color: '#38bdf8',
              fontSize: '0.72rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            <Download size={12} />
            Export CSV
          </button>
          <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
            {(sequentialData.confidence_score * 100).toFixed(1)}% Conf
          </span>
        </div>
      </div>

      {/* Horizon Tabs: 24h, 48h, 72h */}
      <div style={{ display: 'flex', gap: '8px', background: 'rgba(15, 23, 42, 0.6)', padding: '4px', borderRadius: '8px' }}>
        {[24, 48, 72].map((h) => (
          <button
            key={h}
            onClick={() => setActiveHorizon(h)}
            style={{
              flex: 1,
              padding: '8px',
              border: 'none',
              borderRadius: '6px',
              fontSize: '0.78rem',
              fontWeight: 600,
              cursor: 'pointer',
              background: activeHorizon === h ? 'linear-gradient(135deg, #0284c7, #2563eb)' : 'transparent',
              color: activeHorizon === h ? '#ffffff' : '#94a3b8',
              transition: 'all 0.2s'
            }}
          >
            +{h} Hours
          </button>
        ))}
      </div>

      {/* Active Horizon Predictive Card */}
      <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span className="metric-label">Forecast Horizon: +{forecast.horizon_hours} Hours</span>
          <span className={`badge-status ${isSevere ? 'severe' : isHigh ? 'high' : 'safe'}`}>
            {forecast.risk_level} INUNDATION RISK
          </span>
        </div>

        {/* Probability Gauge Bar */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Flood Inundation Probability</span>
            <span className="metric-value" style={{ color: isSevere ? '#ef4444' : isHigh ? '#f59e0b' : '#10b981' }}>
              {probPercent}%
            </span>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.08)', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
            <div 
              style={{ 
                width: `${probPercent}%`, 
                height: '100%', 
                background: isSevere 
                  ? 'linear-gradient(90deg, #f59e0b, #ef4444)' 
                  : isHigh 
                    ? 'linear-gradient(90deg, #10b981, #f59e0b)' 
                    : '#10b981',
                borderRadius: '4px',
                transition: 'width 0.4s ease'
              }} 
            />
          </div>
        </div>

        {/* River Gauge Level */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '6px', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Droplets size={16} color="#38bdf8" />
            <span style={{ fontSize: '0.78rem', color: '#cbd5e1' }}>Expected River Level:</span>
          </div>
          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', fontFamily: 'var(--font-mono)' }}>
              {forecast.expected_river_level_m} m
            </span>
            <span style={{ fontSize: '0.68rem', color: '#94a3b8', display: 'block' }}>
              Danger Mark: 7.50m
            </span>
          </div>
        </div>
      </div>

      {/* Sequential Trend Classification */}
      <div className="glass-panel" style={{ padding: '14px', display: 'flex', alignItems: 'center', gap: '12px' }}>
        <TrendingUp size={20} color="#f59e0b" />
        <div>
          <span className="metric-label">Sequence State Classification</span>
          <p style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f8fafc', marginTop: '2px' }}>
            {sequentialData.sequence_trend}
          </p>
        </div>
      </div>

      {/* Hydrologic Coupling Drivers */}
      <div>
        <span className="metric-label" style={{ display: 'block', marginBottom: '8px' }}>
          Identified Driving Hydrologic Factors
        </span>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {forecast.driving_factors.map((factor, idx) => (
            <div 
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.75rem',
                color: '#cbd5e1',
                background: 'rgba(15, 23, 42, 0.5)',
                padding: '8px 10px',
                borderRadius: '6px',
                borderLeft: '2px solid #38bdf8'
              }}
            >
              <Activity size={14} color="#38bdf8" />
              <span>{factor}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Historical Sequence Data Table */}
      <div>
        <span className="metric-label" style={{ display: 'block', marginBottom: '8px' }}>
          Historical Observations (-72h to Present)
        </span>
        <div style={{ maxHeight: '160px', overflowY: 'auto', background: 'rgba(15, 23, 42, 0.6)', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.06)' }}>
          <table style={{ width: '100%', fontSize: '0.7rem', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ background: 'rgba(255,255,255,0.04)', color: '#94a3b8' }}>
                <th style={{ padding: '6px 8px' }}>Time</th>
                <th style={{ padding: '6px 8px' }}>Rain</th>
                <th style={{ padding: '6px 8px' }}>Discharge</th>
                <th style={{ padding: '6px 8px' }}>Soil Sat</th>
                <th style={{ padding: '6px 8px' }}>River Lvl</th>
              </tr>
            </thead>
            <tbody>
              {sequentialData.historical_sequence.map((step, idx) => (
                <tr key={idx} style={{ borderTop: '1px solid rgba(255,255,255,0.03)', color: '#cbd5e1' }}>
                  <td style={{ padding: '5px 8px', fontFamily: 'var(--font-mono)' }}>{step.hour_step}h</td>
                  <td style={{ padding: '5px 8px' }}>{step.rainfall_mm}mm</td>
                  <td style={{ padding: '5px 8px' }}>{step.discharge_cumecs}</td>
                  <td style={{ padding: '5px 8px' }}>{(step.soil_sat * 100).toFixed(0)}%</td>
                  <td style={{ padding: '5px 8px', fontWeight: 600 }}>{step.river_level_m}m</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
