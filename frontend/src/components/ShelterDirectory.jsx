import React from 'react';
import { Home, Users, PackageCheck, HeartPulse, Zap, Phone, Download } from 'lucide-react';
import { apiService } from '../services/api';

export default function ShelterDirectory({ shelters, onSelectShelter, regionId = 'kerala_ernakulam' }) {
  const handleExportCsv = () => {
    apiService.downloadSheltersCsv(regionId);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Home size={18} color="#10b981" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Designated Relief Shelters</h3>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            onClick={handleExportCsv}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              padding: '4px 10px',
              background: 'rgba(30, 41, 59, 0.8)',
              border: '1px solid rgba(16, 185, 129, 0.4)',
              borderRadius: '6px',
              color: '#34d399',
              fontSize: '0.72rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            <Download size={12} />
            Export CSV
          </button>
          <span className="badge-status safe" style={{ fontSize: '0.68rem' }}>
            {shelters.length} Verified Camps
          </span>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {shelters.map((s) => {
          const occPercent = Math.round((s.current_occupancy / s.total_capacity) * 100);
          const isNearFull = s.available_beds <= 50;

          return (
            <div
              key={s.id}
              className="glass-panel"
              style={{
                padding: '14px',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
                cursor: 'pointer'
              }}
              onClick={() => onSelectShelter && onSelectShelter(s.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <strong style={{ fontSize: '0.84rem', color: '#ffffff' }}>{s.name}</strong>
                  <p style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '2px' }}>
                    Elevation: {s.elevation_m}m (Safe Ridge)
                  </p>
                </div>
                <span className={`badge-status ${isNearFull ? 'high' : 'safe'}`}>
                  {s.available_beds} BEDS FREE
                </span>
              </div>

              {/* Occupancy Progress Bar */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: '#94a3b8', marginBottom: '3px' }}>
                  <span>Occupancy: {s.current_occupancy} / {s.total_capacity}</span>
                  <span>{occPercent}%</span>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.08)', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
                  <div 
                    style={{ 
                      width: `${occPercent}%`, 
                      height: '100%', 
                      background: isNearFull ? '#f59e0b' : '#10b981',
                      borderRadius: '3px'
                    }} 
                  />
                </div>
              </div>

              {/* Badges for supplies & medical */}
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '4px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.7rem', color: '#cbd5e1' }}>
                  <PackageCheck size={12} color="#38bdf8" />
                  <span>{s.food_packs_available} Food Packs</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.7rem', color: '#cbd5e1' }}>
                  <HeartPulse size={12} color="#f43f5e" />
                  <span>{s.medical_staff_present ? 'Medical Staff Onsite' : 'First Aid Only'}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.7rem', color: '#cbd5e1' }}>
                  <Zap size={12} color="#fbbf24" />
                  <span>{s.generator_active ? 'Backup Gen Active' : 'Grid Power'}</span>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.72rem', color: '#94a3b8', marginTop: '2px' }}>
                <Phone size={12} />
                <span>Control Room: {s.contact_phone}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
