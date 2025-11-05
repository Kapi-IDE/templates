# 🎨 3D Visualization Components Library

**Enterprise-Grade Three.js UI Components for Knowledge Management & Industrial Applications**

A collection of production-ready, reusable 3D visualization components built with Three.js. These components can be used standalone or integrated with any web application.

---

## 📦 Component Collection

### 1. **Digital Twin** (`digital-twin/`)
Interactive 3D asset visualization for industrial and manufacturing applications.

**Features:**
- CAD model loading (GLB/GLTF format)
- Interactive asset selection with raycasting
- Real-time telemetry display
- Document-to-asset mapping
- Animation system support
- Smooth camera transitions (TWEEN.js)
- Placeholder generation on model load failure

**Use Cases:**
- Manufacturing asset management
- Industrial equipment monitoring
- Maintenance visualization
- Product lifecycle management (PLM)
- Engineering documentation

**Tech Stack:** Three.js + GLTFLoader + OrbitControls + TWEEN.js

---

### 2. **Knowledge Seismograph** (`knowledge-seismograph/`)
Ripple-based visualization showing query relevance across document clusters.

**Features:**
- Document clustering visualization
- Real-time query ripple effects
- Relevance-based ripple intensity
- Interactive document selection
- Cluster boundary visualization
- Customizable ripple settings (speed, decay, lifetime)
- Auto-scroll camera to view all clusters

**Use Cases:**
- Knowledge base exploration
- Document relevance visualization
- Search result visualization
- Cross-document intelligence
- Research knowledge gaps

**Tech Stack:** Three.js + OrbitControls + Lodash

---

### 3. **Knowledge Galaxy** (`knowledge-galaxy/`)
3D cluster visualization for exploring knowledge bases with gap analysis.

**Features:**
- Multi-domain support (aerospace, automotive, custom)
- Cluster-based knowledge organization
- Knowledge gap identification
- Inter-cluster relationship mapping
- Bloom post-processing effects
- Domain-specific data models
- Question-based gap analysis

**Use Cases:**
- Engineering knowledge management
- PLM system visualization
- Knowledge gap analysis
- Cross-departmental knowledge mapping
- Research & development tracking

**Tech Stack:** Three.js + OrbitControls + EffectComposer + UnrealBloomPass

---

### 4. **Space Animation** (`space-animation/`)
Stunning animated space visualization with nucleus, particles, and celestial bodies.

**Features:**
- Procedural nucleus with Perlin noise displacement
- Multi-phase particle animations (expansion, contraction, centering)
- Moving star effects
- Planet and comet visualizations
- Configurable animation timeline
- Auto-rotating camera controls
- Performance-optimized rendering (FPS limiting)

**Use Cases:**
- Landing page backgrounds
- Data visualization intros
- Branded animations
- Loading screens
- Educational content
- Creative portfolio displays

**Tech Stack:** Three.js + OrbitControls + Simplex Noise

---

## 🚀 Quick Start

### Installation

```bash
# Install Three.js and dependencies
npm install three @tweenjs/tween.js lodash simplex-noise
```

### Basic Usage

#### Digital Twin Example

```javascript
import { DigitalTwin } from './components/ui/3d-visualizations/digital-twin/DigitalTwin.js';

const container = document.getElementById('digital-twin-container');

const digitalTwin = new DigitalTwin(container, {
  backgroundColor: 0x111122,
  enableTelemetry: true,
  enableDocumentMapping: true,
  onModelSelect: (modelId, model) => {
    console.log('Selected model:', modelId);
  },
  onTelemetryUpdate: (modelId, telemetry) => {
    console.log('Telemetry:', telemetry);
  }
});

// Load 3D models
digitalTwin.loadModel({
  id: 'industrial_machine',
  path: '/models/machine.glb',
  position: new THREE.Vector3(0, 0, 0),
  scale: 1.0,
  placeholder: true
});

// Set document mapping
digitalTwin.setDocumentMapping({
  'industrial_machine': ['DOC123', 'DOC456', 'DOC789']
});
```

#### Knowledge Seismograph Example

```javascript
import KnowledgeSeismograph from './components/ui/3d-visualizations/knowledge-seismograph/KnowledgeSeismograph.js';

const container = document.getElementById('seismograph-container');
const seismograph = new KnowledgeSeismograph(container);

// Load documents
const documents = [
  { id: 'doc1', title: 'CAD Drawing', type: 'CAD', metadata: { department: 'Engineering' } },
  { id: 'doc2', title: 'Test Procedure', type: 'TEST', metadata: { department: 'Quality' } },
  // ... more documents
];

seismograph.loadDocuments(documents);

// Execute query
seismograph.executeQuery("engine design specifications");

// Adjust relevance threshold
seismograph.setRelevanceThreshold(0.5);
```

#### Knowledge Galaxy Example

```javascript
import { initGalaxy } from './components/ui/3d-visualizations/knowledge-galaxy/KnowledgeGalaxy.js';

const container = document.getElementById('galaxy-container');

// Initialize with domain-specific data
initGalaxy(container, {
  domain: 'aerospace', // or 'automotive'
  onClusterClick: (clusterId, clusterData) => {
    console.log('Cluster clicked:', clusterData);
  },
  onGapClick: (gapId, gapData) => {
    console.log('Knowledge gap:', gapData);
  }
});
```

#### Space Animation Example

```javascript
import { Effect } from './components/ui/3d-visualizations/space-animation/SpaceAnimation.js';

// Initialize animation
const effect = new Effect();
await effect.init();

// Animation runs automatically with predefined timeline
```

---

## 🎨 Customization

### Digital Twin Configuration

```javascript
const options = {
  // Scene settings
  backgroundColor: 0x111122,

  // Camera position
  cameraPosition: { x: 0, y: 15, z: 30 },

  // Lighting
  lightingIntensity: {
    ambient: 0.4,
    directional: 1
  },

  // Features
  enableAnimations: true,
  enableTelemetry: true,
  enableDocumentMapping: true,

  // Callbacks
  onModelSelect: (modelId, model) => {},
  onModelDeselect: (modelId) => {},
  onTelemetryUpdate: (modelId, telemetry) => {},
  onTelemetryClear: () => {},
  onDocumentsLoad: (modelId, documents) => {}
};
```

### Knowledge Seismograph Settings

```javascript
const settings = {
  clusterSpacing: 300,        // Distance between clusters
  documentRadius: 5,          // Size of document nodes
  rippleSpeed: 0.8,           // Ripple expansion speed
  rippleDecay: 0.95,          // Ripple fade rate
  relevanceThreshold: 0.3,    // Minimum relevance to show ripple
  maxRippleSize: 200,         // Maximum ripple radius
  rippleLifetime: 5           // Ripple duration (seconds)
};

seismograph.setRippleSettings(settings);
```

### Knowledge Galaxy Colors

```javascript
// Domain-specific color schemes
const colors = {
  engineering: 0x2c699a,
  manufacturing: 0x048abf,
  research: 0x0c6291,
  operations: 0x07a0c3
};
```

### Space Animation Timeline

```javascript
// Customize animation phases (milliseconds from start)
const timeline = {
  nucleusAnimation: 6000,      // Nucleus blob effect starts
  movingStars: 15000,          // Stars fly toward center
  expansion: 9000,             // Particle expansion
  contraction: 20000,          // Particle contraction
  centering: 25000,            // Gather at center
  pointContraction: 25000      // Outer stars contract
};
```

---

## 📐 Component Architecture

### Digital Twin Architecture

```
DigitalTwin (Class)
├── Scene Management
│   ├── setupScene()
│   ├── setupCamera()
│   ├── setupRenderer()
│   └── setupLighting()
├── Model Management
│   ├── loadModel()
│   ├── createPlaceholder()
│   └── animations{}
├── Interaction
│   ├── onClick()
│   ├── selectModel()
│   ├── deselectModel()
│   └── raycaster
├── Visual Effects
│   ├── highlightModel()
│   ├── removeHighlight()
│   └── focusOnModel() (TWEEN)
├── Data Integration
│   ├── updateTelemetryPanel()
│   ├── loadAssociatedDocuments()
│   └── assetDocumentMapping{}
└── Animation Loop
    └── animate()
```

### Knowledge Seismograph Architecture

```
KnowledgeSeismograph (Class)
├── Visualization Setup
│   ├── init()
│   ├── renderer, scene, camera
│   └── controls (OrbitControls)
├── Data Processing
│   ├── loadDocuments()
│   ├── clusterDocuments()
│   └── createDocumentNodes()
├── Query System
│   ├── executeQuery()
│   ├── simulateRelevanceRipples()
│   └── createRipple()
├── Ripple Management
│   ├── updateRipples()
│   └── ripples[]
└── Interaction
    ├── onMouseClick()
    └── raycaster
```

### Knowledge Galaxy Data Model

```
Knowledge Cluster {
  id: number
  name: string
  domain: string (engineering, manufacturing, research, operations)
  size: number (cluster importance)
  documents: number (doc count)
  updated: date
  subClusters: number[]
  position: {x, y, z}
  keyDocuments: Document[]
}

Knowledge Gap {
  id: number
  significance: string (high, medium, low)
  connectedClusters: number[]
  identified: date
  position: {x, y, z}
  questions: Question[]
}

Question {
  id: number
  text: string
  importance: string (high, medium, low)
  impact: string (description)
}
```

---

## 🔧 Integration Patterns

### With React

```jsx
import { useEffect, useRef } from 'react';
import { DigitalTwin } from './components/ui/3d-visualizations/digital-twin/DigitalTwin.js';

function DigitalTwinComponent() {
  const containerRef = useRef(null);
  const twinRef = useRef(null);

  useEffect(() => {
    if (containerRef.current && !twinRef.current) {
      twinRef.current = new DigitalTwin(containerRef.current, {
        onModelSelect: (modelId) => {
          console.log('Selected:', modelId);
        }
      });
    }

    return () => {
      if (twinRef.current) {
        twinRef.current.dispose();
      }
    };
  }, []);

  return <div ref={containerRef} style={{ width: '100%', height: '600px' }} />;
}
```

### With Vue

```vue
<template>
  <div ref="container" class="digital-twin-container"></div>
</template>

<script>
import { DigitalTwin } from './components/ui/3d-visualizations/digital-twin/DigitalTwin.js';

export default {
  mounted() {
    this.twin = new DigitalTwin(this.$refs.container, {
      onModelSelect: this.handleModelSelect
    });
  },

  beforeUnmount() {
    if (this.twin) {
      this.twin.dispose();
    }
  },

  methods: {
    handleModelSelect(modelId) {
      console.log('Selected:', modelId);
    }
  }
}
</script>

<style scoped>
.digital-twin-container {
  width: 100%;
  height: 600px;
}
</style>
```

### With Vanilla JavaScript

```html
<!DOCTYPE html>
<html>
<head>
  <title>Digital Twin Demo</title>
  <style>
    #twin-container { width: 100%; height: 600px; }
  </style>
</head>
<body>
  <div id="twin-container"></div>

  <script type="module">
    import { DigitalTwin } from './components/ui/3d-visualizations/digital-twin/DigitalTwin.js';

    const container = document.getElementById('twin-container');
    const twin = new DigitalTwin(container);

    twin.loadModel({
      id: 'machine',
      path: '/models/machine.glb'
    });
  </script>
</body>
</html>
```

---

## 🎯 Use Case Examples

### Manufacturing Dashboard

Combine Digital Twin + Telemetry display for real-time asset monitoring:

```javascript
const twin = new DigitalTwin(container, {
  onTelemetryUpdate: (modelId, telemetry) => {
    // Update dashboard panels
    document.getElementById('temperature').textContent = telemetry.temperature;
    document.getElementById('pressure').textContent = telemetry.pressure;
    document.getElementById('runtime').textContent = telemetry.runtime;
    document.getElementById('status').textContent = telemetry.status;
  },
  onDocumentsLoad: (modelId, documents) => {
    // Load associated technical documents
    const docList = documents.map(docId =>
      `<li><a href="/docs/${docId}">${docId}</a></li>`
    ).join('');
    document.getElementById('doc-list').innerHTML = docList;
  }
});
```

### Knowledge Management Portal

Combine Knowledge Galaxy + Seismograph for comprehensive knowledge exploration:

```javascript
// Galaxy for high-level overview
const galaxy = initGalaxy(galaxyContainer, {
  onClusterClick: (clusterId, clusterData) => {
    // Load cluster documents into seismograph
    const documents = clusterData.keyDocuments;
    seismograph.loadDocuments(documents);
  }
});

// Seismograph for detailed exploration
const seismograph = new KnowledgeSeismograph(seismographContainer);
```

### Animated Landing Page

Use Space Animation for engaging visual background:

```javascript
// Full-screen background
const effect = new Effect();
await effect.init();

// Overlay content on top
document.querySelector('.hero-content').style.position = 'relative';
document.querySelector('.hero-content').style.zIndex = '10';
```

---

## 🛠️ Development

### File Structure

```
components/ui/3d-visualizations/
├── README.md (this file)
├── digital-twin/
│   ├── DigitalTwin.js
│   ├── README.md
│   └── examples/
├── knowledge-seismograph/
│   ├── KnowledgeSeismograph.js
│   ├── README.md
│   └── examples/
├── knowledge-galaxy/
│   ├── KnowledgeGalaxy.js
│   ├── README.md
│   └── examples/
└── space-animation/
    ├── SpaceAnimation.js
    ├── README.md
    └── examples/
```

### Dependencies

```json
{
  "dependencies": {
    "three": "^0.160.0",
    "@tweenjs/tween.js": "^21.0.0",
    "lodash": "^4.17.21",
    "simplex-noise": "^4.0.1"
  }
}
```

### Build Configuration (Vite Example)

```javascript
// vite.config.js
export default {
  resolve: {
    alias: {
      'three/addons': 'three/examples/jsm'
    }
  }
}
```

---

## 📊 Performance Considerations

### Digital Twin
- **FPS Target:** 60 FPS
- **Model Complexity:** Limit to 100k vertices per model
- **Shadow Maps:** 2048x2048 resolution (adjustable)
- **Memory:** ~50-100 MB per loaded model

**Optimization Tips:**
- Use LOD (Level of Detail) for distant objects
- Implement object culling
- Compress GLB files
- Lazy load models on demand

### Knowledge Seismograph
- **FPS Target:** 60 FPS
- **Document Limit:** Up to 1000 documents
- **Ripple Limit:** Auto-cleanup after lifetime expires
- **Memory:** ~10-20 MB for 1000 documents

**Optimization Tips:**
- Use instanced meshes for documents
- Limit simultaneous ripple count
- Throttle ripple creation

### Knowledge Galaxy
- **FPS Target:** 30-60 FPS
- **Cluster Limit:** Up to 50 clusters
- **Bloom Effect:** Medium quality (adjustable)
- **Memory:** ~30-50 MB

**Optimization Tips:**
- Reduce bloom resolution for better performance
- Use simpler geometries for clusters
- Limit particle count

### Space Animation
- **FPS Target:** 60 FPS (with FPS limiter)
- **Particle Count:** Configurable (default: 800)
- **Noise Calculations:** Optimized with pre-computed values
- **Memory:** ~20-30 MB

**Optimization Tips:**
- Adjust particle counts based on device
- Use lower geometry detail for nucleus
- Disable unnecessary animation phases

---

## 🔐 Security Considerations

- All components are **frontend-only**
- No hardcoded credentials or API keys
- Model loading should validate file types (GLB/GLTF only)
- Implement CORS properly for model loading
- Sanitize any user-provided URLs before loading

---

## 📝 License

MIT License - Free to use in commercial and personal projects.

---

## 🤝 Contributing

These components are extracted from the **Brahmasumm** knowledge management platform and refined for reusability.

**Enhancement Ideas:**
- VR/AR support
- More animation presets
- Additional data visualization modes
- Performance monitoring dashboard
- Mobile optimization
- Accessibility improvements (keyboard navigation, screen readers)

---

## 📚 Additional Resources

### Learning Three.js
- [Three.js Documentation](https://threejs.org/docs/)
- [Three.js Examples](https://threejs.org/examples/)
- [Three.js Journey Course](https://threejs-journey.com/)

### CAD Model Resources
- [Sketchfab](https://sketchfab.com/) - 3D model marketplace
- [TurboSquid](https://www.turbosquid.com/) - Professional models
- [Free3D](https://free3d.com/) - Free models

### Visualization Techniques
- [Data Visualization Catalog](https://datavizcatalogue.com/)
- [Observable](https://observablehq.com/) - Interactive visualizations
- [D3.js Gallery](https://d3-graph-gallery.com/) - 2D data viz

---

**Built with ❤️ for modern knowledge management and industrial visualization**
