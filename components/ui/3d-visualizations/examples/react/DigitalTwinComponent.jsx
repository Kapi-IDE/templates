/**
 * React Digital Twin Component
 *
 * Example integration of Digital Twin component with React
 * Demonstrates proper lifecycle management and cleanup
 */

import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { DigitalTwin } from '../../digital-twin/DigitalTwin.js';

export function DigitalTwinComponent({ models = [], documentMapping = {} }) {
  const containerRef = useRef(null);
  const twinRef = useRef(null);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [telemetry, setTelemetry] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!containerRef.current || twinRef.current) return;

    // Initialize Digital Twin
    twinRef.current = new DigitalTwin(containerRef.current, {
      backgroundColor: 0x111122,
      enableTelemetry: true,
      enableDocumentMapping: true,
      enableAnimations: true,

      onModelSelect: (modelId, model) => {
        setSelectedAsset(modelId);
      },

      onModelDeselect: () => {
        setSelectedAsset(null);
        setTelemetry(null);
        setDocuments([]);
      },

      onTelemetryUpdate: (modelId, telemetryData) => {
        setTelemetry({ modelId, ...telemetryData });
      },

      onDocumentsLoad: (modelId, documentIds) => {
        setDocuments(documentIds);
      }
    });

    // Load models
    const loadModels = async () => {
      try {
        for (const modelConfig of models) {
          await twinRef.current.loadModel(modelConfig);
        }

        // Set document mapping
        if (Object.keys(documentMapping).length > 0) {
          twinRef.current.setDocumentMapping(documentMapping);
        }

        setLoading(false);
      } catch (error) {
        console.error('Error loading models:', error);
        setLoading(false);
      }
    };

    loadModels();

    // Cleanup on unmount
    return () => {
      if (twinRef.current) {
        twinRef.current.dispose();
        twinRef.current = null;
      }
    };
  }, [models, documentMapping]);

  return (
    <div className="digital-twin-wrapper" style={{ position: 'relative' }}>
      {/* 3D Canvas Container */}
      <div
        ref={containerRef}
        style={{
          width: '100%',
          height: '600px',
          backgroundColor: '#111122'
        }}
      />

      {/* Loading Indicator */}
      {loading && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            color: 'white',
            fontSize: '18px'
          }}
        >
          Loading 3D Models...
        </div>
      )}

      {/* Telemetry Panel */}
      {telemetry && (
        <div
          className="telemetry-panel"
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            color: 'white',
            padding: '15px',
            borderRadius: '8px',
            minWidth: '250px'
          }}
        >
          <h3 style={{ margin: '0 0 10px 0' }}>
            Asset: {selectedAsset}
          </h3>

          <div className="metric-row" style={{ marginBottom: '8px' }}>
            <span style={{ opacity: 0.7 }}>Temperature:</span>
            <span
              style={{
                float: 'right',
                color: parseFloat(telemetry.temperature) > 40 ? '#ff6b6b' : '#51cf66'
              }}
            >
              {telemetry.temperature}
            </span>
          </div>

          <div className="metric-row" style={{ marginBottom: '8px' }}>
            <span style={{ opacity: 0.7 }}>Pressure:</span>
            <span style={{ float: 'right' }}>{telemetry.pressure}</span>
          </div>

          <div className="metric-row" style={{ marginBottom: '8px' }}>
            <span style={{ opacity: 0.7 }}>Runtime:</span>
            <span style={{ float: 'right' }}>{telemetry.runtime}</span>
          </div>

          <div className="metric-row" style={{ marginBottom: '8px' }}>
            <span style={{ opacity: 0.7 }}>Maintenance:</span>
            <span
              style={{
                float: 'right',
                color: telemetry.maintenance === 'Due' ? '#ffd43b' : '#51cf66'
              }}
            >
              {telemetry.maintenance}
            </span>
          </div>

          <div
            className="status-badge"
            style={{
              marginTop: '12px',
              padding: '6px 12px',
              borderRadius: '4px',
              textAlign: 'center',
              backgroundColor:
                telemetry.status === 'Warning' ? '#fa5252' : '#51cf66',
              fontWeight: 'bold'
            }}
          >
            {telemetry.status}
          </div>
        </div>
      )}

      {/* Documents Panel */}
      {documents.length > 0 && (
        <div
          className="documents-panel"
          style={{
            position: 'absolute',
            bottom: '20px',
            left: '20px',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            color: 'white',
            padding: '15px',
            borderRadius: '8px',
            maxWidth: '300px'
          }}
        >
          <h3 style={{ margin: '0 0 10px 0' }}>Technical Documents</h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {documents.map((docId, index) => (
              <li
                key={index}
                style={{
                  padding: '8px 0',
                  borderBottom:
                    index < documents.length - 1
                      ? '1px solid rgba(255, 255, 255, 0.1)'
                      : 'none'
                }}
              >
                <a
                  href={`/documents/${docId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    color: '#74c0fc',
                    textDecoration: 'none'
                  }}
                >
                  📄 {docId}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Instructions */}
      {!selectedAsset && !loading && (
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: 'rgba(0, 0, 0, 0.6)',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '4px',
            fontSize: '14px'
          }}
        >
          Click on an asset to view details
        </div>
      )}
    </div>
  );
}

// Example usage in parent component
export function App() {
  const models = [
    {
      id: 'kuka_robot',
      path: '/models/kuka_robot.glb',
      position: new THREE.Vector3(-5, 0, 0),
      scale: 1.0,
      name: 'Kuka KR 210 Robot',
      type: 'robot',
      placeholder: true
    },
    {
      id: 'industrial_machine',
      path: '/models/industrial_machine.glb',
      position: new THREE.Vector3(5, 0, 0),
      scale: 0.8,
      name: 'CNC Machine',
      type: 'machine',
      placeholder: true
    }
  ];

  const documentMapping = {
    kuka_robot: ['DOC_ROBOT_MANUAL', 'DOC_SAFETY_GUIDE', 'DOC_MAINTENANCE'],
    industrial_machine: ['DOC_MACHINE_SPEC', 'DOC_OPERATION_MANUAL']
  };

  return (
    <div className="app">
      <header>
        <h1>Digital Twin - Manufacturing Floor</h1>
      </header>

      <main>
        <DigitalTwinComponent
          models={models}
          documentMapping={documentMapping}
        />
      </main>
    </div>
  );
}

export default DigitalTwinComponent;
