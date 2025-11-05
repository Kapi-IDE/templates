/**
 * Digital Twin - Interactive 3D Asset Visualization Component
 *
 * A production-ready Three.js component for visualizing industrial assets with:
 * - CAD model loading (GLB/GLTF format)
 * - Interactive asset selection with raycasting
 * - Real-time telemetry display
 * - Document-to-asset mapping
 * - Animation system
 * - Camera controls with smooth transitions
 *
 * @version 1.0.0
 * @author KAPI Components
 * @license MIT
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import TWEEN from '@tweenjs/tween.js';

export class DigitalTwin {
  constructor(container, options = {}) {
    // Configuration
    this.container = container;
    this.options = {
      backgroundColor: 0x111122,
      enableAnimations: true,
      enableTelemetry: true,
      enableDocumentMapping: true,
      cameraPosition: { x: 0, y: 15, z: 30 },
      lightingIntensity: { ambient: 0.4, directional: 1 },
      ...options
    };

    // State
    this.models = {};
    this.selectedModel = null;
    this.animations = {};
    this.assetDocumentMapping = {};
    this.telemetryData = {};

    // Three.js core objects
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();

    // Initialize
    this.init();
  }

  /**
   * Initialize the Digital Twin scene
   */
  init() {
    this.setupScene();
    this.setupCamera();
    this.setupRenderer();
    this.setupLighting();
    this.setupControls();
    this.setupEventListeners();
    this.animate();
  }

  /**
   * Setup Three.js scene
   */
  setupScene() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.options.backgroundColor);
    this.scene.fog = new THREE.Fog(this.options.backgroundColor, 50, 200);
  }

  /**
   * Setup camera
   */
  setupCamera() {
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
    this.camera.position.set(
      this.options.cameraPosition.x,
      this.options.cameraPosition.y,
      this.options.cameraPosition.z
    );
  }

  /**
   * Setup WebGL renderer
   */
  setupRenderer() {
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true
    });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.appendChild(this.renderer.domElement);
  }

  /**
   * Setup scene lighting
   */
  setupLighting() {
    // Ambient light
    const ambientLight = new THREE.AmbientLight(
      0xffffff,
      this.options.lightingIntensity.ambient
    );
    this.scene.add(ambientLight);

    // Directional light (main)
    const directionalLight = new THREE.DirectionalLight(
      0xffffff,
      this.options.lightingIntensity.directional
    );
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    this.scene.add(directionalLight);

    // Additional fill lights
    const fillLight1 = new THREE.DirectionalLight(0x4466ff, 0.3);
    fillLight1.position.set(-10, 10, -10);
    this.scene.add(fillLight1);

    const fillLight2 = new THREE.DirectionalLight(0xff6644, 0.2);
    fillLight2.position.set(5, -5, 10);
    this.scene.add(fillLight2);
  }

  /**
   * Setup orbit controls
   */
  setupControls() {
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 10;
    this.controls.maxDistance = 100;
    this.controls.maxPolarAngle = Math.PI / 2;
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Click detection for asset selection
    this.renderer.domElement.addEventListener('click', this.onClick.bind(this));

    // Window resize handling
    window.addEventListener('resize', this.onWindowResize.bind(this));

    // Mouse move for hover effects
    this.renderer.domElement.addEventListener('mousemove', this.onMouseMove.bind(this));
  }

  /**
   * Load a 3D model (GLB/GLTF)
   * @param {Object} config - Model configuration
   * @returns {Promise} - Resolves when model is loaded
   */
  loadModel(config) {
    return new Promise((resolve, reject) => {
      const loader = new GLTFLoader();

      loader.load(
        config.path,
        (gltf) => {
          const model = gltf.scene;

          // Set position
          if (config.position) {
            model.position.copy(config.position);
          }

          // Set scale
          if (config.scale) {
            model.scale.set(config.scale, config.scale, config.scale);
          }

          // Store model metadata
          model.userData.modelId = config.id;
          model.userData.name = config.name || config.id;
          model.userData.type = config.type || 'asset';

          // Enable shadows
          model.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
              child.userData.modelId = config.id;
            }
          });

          // Store animation mixer if model has animations
          if (gltf.animations && gltf.animations.length > 0) {
            const mixer = new THREE.AnimationMixer(model);
            this.animations[config.id] = {
              mixer: mixer,
              actions: gltf.animations.map(clip => mixer.clipAction(clip))
            };
          }

          // Add to scene
          this.scene.add(model);
          this.models[config.id] = model;

          // Create placeholder if specified
          if (config.placeholder) {
            this.createPlaceholder(config);
          }

          resolve(model);
        },
        (xhr) => {
          const progress = (xhr.loaded / xhr.total) * 100;
          if (config.onProgress) {
            config.onProgress(progress);
          }
        },
        (error) => {
          console.error(`Error loading model ${config.id}:`, error);

          // Create placeholder on error
          if (config.placeholder !== false) {
            this.createPlaceholder(config);
          }

          reject(error);
        }
      );
    });
  }

  /**
   * Create a placeholder geometry when model fails to load
   * @param {Object} config - Model configuration
   */
  createPlaceholder(config) {
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const material = new THREE.MeshStandardMaterial({
      color: 0x888888,
      wireframe: true
    });
    const placeholder = new THREE.Mesh(geometry, material);

    if (config.position) {
      placeholder.position.copy(config.position);
    }

    placeholder.userData.modelId = config.id;
    placeholder.userData.isPlaceholder = true;

    this.scene.add(placeholder);
    this.models[config.id] = placeholder;
  }

  /**
   * Handle mouse click for asset selection
   * @param {Event} event - Click event
   */
  onClick(event) {
    this.updateMousePosition(event);

    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.scene.children, true);

    if (intersects.length > 0) {
      const clickedObject = intersects[0].object;
      const modelId = clickedObject.userData.modelId;

      if (modelId && this.models[modelId]) {
        this.selectModel(this.models[modelId]);
      }
    } else {
      this.deselectModel();
    }
  }

  /**
   * Handle mouse move for hover effects
   * @param {Event} event - Mouse move event
   */
  onMouseMove(event) {
    this.updateMousePosition(event);

    // Optional: Add hover highlighting here
  }

  /**
   * Update mouse position in normalized device coordinates
   * @param {Event} event - Mouse event
   */
  updateMousePosition(event) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  }

  /**
   * Select a model and display its information
   * @param {THREE.Object3D} model - Selected model
   */
  selectModel(model) {
    // Deselect previous model
    if (this.selectedModel) {
      this.deselectModel();
    }

    this.selectedModel = model;
    const modelId = model.userData.modelId;

    // Visual feedback - Add outline or highlight
    this.highlightModel(model);

    // Animate camera to focus on model
    this.focusOnModel(model);

    // Update telemetry panel
    if (this.options.enableTelemetry) {
      this.updateTelemetryPanel(modelId);
    }

    // Load associated documents
    if (this.options.enableDocumentMapping) {
      this.loadAssociatedDocuments(modelId);
    }

    // Play animation if available
    if (this.options.enableAnimations && this.animations[modelId]) {
      this.playAnimation(modelId);
    }

    // Trigger callback
    if (this.options.onModelSelect) {
      this.options.onModelSelect(modelId, model);
    }
  }

  /**
   * Deselect the currently selected model
   */
  deselectModel() {
    if (!this.selectedModel) return;

    const modelId = this.selectedModel.userData.modelId;

    // Remove visual highlight
    this.removeHighlight(this.selectedModel);

    // Stop animation
    if (this.animations[modelId]) {
      this.stopAnimation(modelId);
    }

    // Clear telemetry
    if (this.options.enableTelemetry) {
      this.clearTelemetryPanel();
    }

    this.selectedModel = null;

    // Trigger callback
    if (this.options.onModelDeselect) {
      this.options.onModelDeselect(modelId);
    }
  }

  /**
   * Highlight selected model
   * @param {THREE.Object3D} model - Model to highlight
   */
  highlightModel(model) {
    model.traverse((child) => {
      if (child.isMesh) {
        child.userData.originalEmissive = child.material.emissive?.clone();
        if (child.material.emissive) {
          child.material.emissive.setHex(0x3366ff);
          child.material.emissiveIntensity = 0.3;
        }
      }
    });
  }

  /**
   * Remove highlight from model
   * @param {THREE.Object3D} model - Model to remove highlight from
   */
  removeHighlight(model) {
    model.traverse((child) => {
      if (child.isMesh && child.userData.originalEmissive) {
        child.material.emissive.copy(child.userData.originalEmissive);
        child.material.emissiveIntensity = 0;
      }
    });
  }

  /**
   * Focus camera on selected model with smooth animation
   * @param {THREE.Object3D} model - Model to focus on
   */
  focusOnModel(model) {
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const distance = maxDim * 2.5;

    const targetPosition = {
      x: center.x + distance * 0.5,
      y: center.y + distance * 0.3,
      z: center.z + distance * 0.8
    };

    // Smooth camera transition using TWEEN
    new TWEEN.Tween(this.camera.position)
      .to(targetPosition, 1000)
      .easing(TWEEN.Easing.Cubic.InOut)
      .start();

    new TWEEN.Tween(this.controls.target)
      .to(center, 1000)
      .easing(TWEEN.Easing.Cubic.InOut)
      .onUpdate(() => this.controls.update())
      .start();
  }

  /**
   * Update telemetry panel with real-time data
   * @param {string} modelId - Model identifier
   */
  updateTelemetryPanel(modelId) {
    const telemetry = this.generateTelemetry(modelId);

    if (this.options.onTelemetryUpdate) {
      this.options.onTelemetryUpdate(modelId, telemetry);
    }
  }

  /**
   * Generate simulated telemetry data
   * @param {string} modelId - Model identifier
   * @returns {Object} Telemetry data
   */
  generateTelemetry(modelId) {
    return {
      temperature: (Math.random() * 50 + 20).toFixed(1) + '°C',
      pressure: (Math.random() * 10 + 1).toFixed(2) + ' MPa',
      runtime: Math.floor(Math.random() * 10000) + ' hrs',
      maintenance: Math.random() > 0.7 ? 'Due' : 'OK',
      status: Math.random() > 0.9 ? 'Warning' : 'Operational',
      lastUpdate: new Date().toISOString()
    };
  }

  /**
   * Clear telemetry panel
   */
  clearTelemetryPanel() {
    if (this.options.onTelemetryClear) {
      this.options.onTelemetryClear();
    }
  }

  /**
   * Load documents associated with an asset
   * @param {string} modelId - Model identifier
   */
  loadAssociatedDocuments(modelId) {
    const documents = this.assetDocumentMapping[modelId] || [];

    if (this.options.onDocumentsLoad) {
      this.options.onDocumentsLoad(modelId, documents);
    }
  }

  /**
   * Set document mapping for assets
   * @param {Object} mapping - Asset ID to document IDs mapping
   */
  setDocumentMapping(mapping) {
    this.assetDocumentMapping = mapping;
  }

  /**
   * Play animation for a model
   * @param {string} modelId - Model identifier
   */
  playAnimation(modelId) {
    const animation = this.animations[modelId];
    if (animation && animation.actions.length > 0) {
      animation.actions[0].reset().play();
    }
  }

  /**
   * Stop animation for a model
   * @param {string} modelId - Model identifier
   */
  stopAnimation(modelId) {
    const animation = this.animations[modelId];
    if (animation && animation.actions.length > 0) {
      animation.actions[0].stop();
    }
  }

  /**
   * Handle window resize
   */
  onWindowResize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  /**
   * Animation loop
   */
  animate() {
    requestAnimationFrame(this.animate.bind(this));

    // Update controls
    this.controls.update();

    // Update TWEEN animations
    TWEEN.update();

    // Update model animations
    const delta = 0.016; // ~60fps
    Object.values(this.animations).forEach(animation => {
      if (animation.mixer) {
        animation.mixer.update(delta);
      }
    });

    // Render scene
    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Clean up resources
   */
  dispose() {
    // Remove event listeners
    this.renderer.domElement.removeEventListener('click', this.onClick);
    this.renderer.domElement.removeEventListener('mousemove', this.onMouseMove);
    window.removeEventListener('resize', this.onWindowResize);

    // Dispose geometries and materials
    this.scene.traverse((object) => {
      if (object.geometry) object.geometry.dispose();
      if (object.material) {
        if (Array.isArray(object.material)) {
          object.material.forEach(material => material.dispose());
        } else {
          object.material.dispose();
        }
      }
    });

    // Dispose renderer
    this.renderer.dispose();

    // Remove DOM element
    this.container.removeChild(this.renderer.domElement);
  }
}

export default DigitalTwin;
