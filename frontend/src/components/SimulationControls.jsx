import React, { useState } from 'react';
import { Flame, Sliders, AlertOctagon, RotateCcw, Play, Check } from 'lucide-react';

export default function SimulationControls({
  regionId,
  simulationStatus,
  onTriggerSimulation,
  loading
}) {
  const [selectedScenario, setSelectedScenario] = useState('dam_gate_release');
  const [intensity, setIntensity] = useState(1.6);
  const [feedback, setFeedback] = useState(null);

  const handleTrigger = async () => {
    try {
      const result = await onTriggerSimulation(selectedScenario, intensity);
      setFeedback(result);
    } catch (err) {
      console.error(err);
    }
  };

  const handleReset = async () => {
    try {
      const result = await onTriggerSimulation('receding', 1.0);
      setFeedback(result);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Flame size={18} color="#ef4444" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Disaster Crisis Simulator</h3>
        </div>
        <span className="badge-status severe" style={{ fontSize: '0.68rem' }}>
          Real-Time Stress Test
        </span>
      </div>

      <div className="glass-panel" style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div>
          <span className="metric-label">Disaster Surge Scenario</span>
          <select 
            className="select-custom" 
            style={{ width: '100%', marginTop: '4px' }}
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
          >
            <option value="dam_gate_release">Idamalayar / Idukki Dam Sluice Gate Release</option>
            <option value="monsoon_surge">Extreme 72-Hour Monsoon Cloudburst (150mm)</option>
            <option value="flash_flood">Upstream Flash Flood Inrush</option>
            <option value="receding">Receding Waters (Recovery Phase)</option>
          </select>
        </div>

        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
            <span style={{ color: '#cbd5e1' }}>Surge Multiplier Intensity:</span>
            <strong style={{ color: '#ef4444' }}>{intensity}x</strong>
          </div>
          <input
            type="range"
            min="1.0"
            max="2.5"
            step="0.1"
            value={intensity}
            onChange={(e) => setIntensity(parseFloat(e.target.value))}
            style={{ width: '100%', accentColor: '#ef4444' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '10px', marginTop: '6px' }}>
          <button 
            className="btn-danger" 
            onClick={handleTrigger}
            disabled={loading}
            style={{ flex: 2, justifyContent: 'center' }}
          >
            <Play size={14} />
            Inject Disaster Surge
          </button>

          <button 
            className="btn-primary" 
            onClick={handleReset}
            disabled={loading}
            style={{ flex: 1, justifyContent: 'center', background: '#334155' }}
            title="Reset to nominal conditions"
          >
            <RotateCcw size={14} />
            Reset
          </button>
        </div>
      </div>

      {/* Live Simulation Feedback Banner */}
      {feedback && (
        <div 
          style={{ 
            background: 'rgba(30, 41, 59, 0.7)', 
            border: '1px solid rgba(239, 68, 68, 0.4)', 
            borderRadius: '8px', 
            padding: '12px',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <AlertOctagon size={16} color="#ef4444" />
            <strong style={{ fontSize: '0.8rem', color: '#f87171' }}>
              {feedback.message}
            </strong>
          </div>
          <p style={{ fontSize: '0.74rem', color: '#cbd5e1' }}>
            Active Spatial Clusters: <strong>{feedback.new_active_clusters}</strong>
          </p>
          {feedback.critical_roads_severed?.length > 0 && (
            <div style={{ marginTop: '4px' }}>
              <span style={{ fontSize: '0.7rem', color: '#fca5a5', fontWeight: 600 }}>Severed Road Segments:</span>
              <ul style={{ paddingLeft: '16px', fontSize: '0.7rem', color: '#e2e8f0', marginTop: '2px' }}>
                {feedback.critical_roads_severed.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
