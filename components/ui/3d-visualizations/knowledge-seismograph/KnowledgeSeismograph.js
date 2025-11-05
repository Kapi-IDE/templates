// Knowledge Seismograph - Interactive Document Visualization
// This implementation visualizes document clusters with interactive ripple effects
// showing query relevance and concept relationships

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import _ from 'lodash';

class KnowledgeSeismograph {
  constructor(container) {
    // Core properties
    this.container = container;
    this.documents = [];
    this.clusters = [];
    this.ripples = [];
    this.activeQueries = [];
    this.clock = new THREE.Clock();
    
    // Visualization settings
    this.settings = {
      clusterSpacing: 300,
      documentRadius: 5,
      rippleSpeed: 0.8,
      rippleDecay: 0.95,
      relevanceThreshold: 0.3,
      maxRippleSize: 200,
      rippleLifetime: 5 // seconds
    };
    
    // Color schemes
    this.colors = {
      background: 0x121218,
      documents: 0x3a7ca5,
      clusters: [0x2c699a, 0x0c6291, 0x048abf, 0x07a0c3],
      ripples: [0x0cc0df, 0x0cdfdd, 0xff9500, 0xff2d00],
      highlights: 0xf7e016
    };
    
    this.init();
  }
  
  init() {
    // Setup renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.setClearColor(this.colors.background, 1);
    this.container.appendChild(this.renderer.domElement);
    
    // Setup scene
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(this.colors.background, 0.0015);
    
    // Setup camera
    this.camera = new THREE.PerspectiveCamera(
      60, 
      this.container.clientWidth / this.container.clientHeight, 
      1, 
      4000
    );
    this.camera.position.set(0, 300, 600);
    
    // Setup controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.screenSpacePanning = false;
    
    // Setup lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(0, 200, 100);
    this.scene.add(directionalLight);
    
    // Setup raycaster for interaction
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    
    // Add ground plane for reference
    const groundGeometry = new THREE.PlaneGeometry(2000, 2000, 20, 20);
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: this.colors.background,
      roughness: 0.8,
      metalness: 0.2,
      wireframe: true,
      transparent: true,
      opacity: 0.2
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -50;
    this.scene.add(ground);
    
    // Group for document objects
    this.documentsGroup = new THREE.Group();
    this.scene.add(this.documentsGroup);
    
    // Group for ripple effects
    this.ripplesGroup = new THREE.Group();
    this.scene.add(this.ripplesGroup);
    
    // Setup event listeners
    window.addEventListener('resize', this.onWindowResize.bind(this), false);
    this.renderer.domElement.addEventListener('mousemove', this.onMouseMove.bind(this), false);
    this.renderer.domElement.addEventListener('click', this.onMouseClick.bind(this), false);
    
    // Start animation loop
    this.animate();
  }
  
  // Load and process document data
  loadDocuments(documents) {
    this.documents = documents;
    this.clearVisualization();
    
    if (documents.length === 0) {
      console.warn('No documents provided to visualize');
      return;
    }
    
    // Group documents into clusters (simplified - normally would use embedding similarity)
    this.clusters = this.clusterDocuments(documents);
    
    // Create visual elements
    this.createDocumentNodes();
    this.createClusterBoundaries();
    
    // Position camera to see all documents
    this.resetCameraView();
  }
  
  clusterDocuments(documents) {
    // This is a simplified clustering algorithm
    // In a real implementation, this would use the actual embedding vectors
    
    // For demo, we'll create 3-5 random clusters
    const clusterCount = Math.floor(Math.random() * 3) + 3;
    
    // Assign each document to a random cluster
    const clusters = _.range(clusterCount).map(i => ({
      id: `cluster-${i}`,
      name: `Cluster ${i+1}`,
      color: this.colors.clusters[i % this.colors.clusters.length],
      documents: [],
      position: new THREE.Vector3(
        (Math.random() - 0.5) * this.settings.clusterSpacing * 2,
        0,
        (Math.random() - 0.5) * this.settings.clusterSpacing * 2
      ),
      radius: 100 + Math.random() * 100
    }));
    
    // Assign documents to clusters
    documents.forEach(doc => {
      const clusterIndex = Math.floor(Math.random() * clusterCount);
      clusters[clusterIndex].documents.push(doc);
    });
    
    return clusters;
  }
  
  createDocumentNodes() {
    // Create instanced mesh for better performance with many documents
    const docGeometry = new THREE.SphereGeometry(this.settings.documentRadius, 8, 8);
    const docMaterial = new THREE.MeshStandardMaterial({
      color: this.colors.documents,
      roughness: 0.7,
      metalness: 0.2
    });
    
    // Process each cluster
    this.clusters.forEach(cluster => {
      // Create a container for document instances in this cluster
      const instancedMesh = new THREE.InstancedMesh(
        docGeometry, 
        docMaterial.clone(), 
        cluster.documents.length
      );
      instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
      instancedMesh.material.color.set(cluster.color);
      
      // Set position for each document within cluster
      const dummy = new THREE.Object3D();
      cluster.documents.forEach((doc, index) => {
        // Assign a position within the cluster (spiral pattern)
        const angle = index * 0.6;
        const radius = Math.sqrt(index) * 8;
        const x = cluster.position.x + radius * Math.cos(angle);
        const z = cluster.position.z + radius * Math.sin(angle);
        
        // Store position in document data for later reference
        doc.position = new THREE.Vector3(x, 0, z);
        doc.clusterIndex = this.clusters.indexOf(cluster);
        
        // Set the matrix for this instance
        dummy.position.set(x, 0, z);
        dummy.updateMatrix();
        instancedMesh.setMatrixAt(index, dummy.matrix);
      });
      
      instancedMesh.instanceMatrix.needsUpdate = true;
      this.documentsGroup.add(instancedMesh);
    });
  }
  
  createClusterBoundaries() {
    this.clusters.forEach(cluster => {
      const geometry = new THREE.CircleGeometry(cluster.radius, 32);
      const material = new THREE.MeshBasicMaterial({
        color: cluster.color,
        transparent: true,
        opacity: 0.1,
        side: THREE.DoubleSide
      });
      
      const circle = new THREE.Mesh(geometry, material);
      circle.rotation.x = -Math.PI / 2;
      circle.position.copy(cluster.position);
      circle.position.y = -5;
      this.documentsGroup.add(circle);
      
      // Add text label for cluster name
      const label = this.createTextLabel(cluster.name, cluster.position, cluster.color);
      this.documentsGroup.add(label);
    });
  }
  
  createTextLabel(text, position, color) {
    // This is a placeholder - in Three.js you'd typically use a sprite with canvas text
    // or use a library like troika-three-text for better text rendering
    const sprite = new THREE.Sprite(
      new THREE.SpriteMaterial({
        color: color
      })
    );
    sprite.position.set(position.x, 20, position.z);
    sprite.scale.set(40, 20, 1);
    
    return sprite;
  }
  
  resetCameraView() {
    // Find the bounds of all clusters
    let minX = Infinity, maxX = -Infinity;
    let minZ = Infinity, maxZ = -Infinity;
    
    this.clusters.forEach(cluster => {
      const x = cluster.position.x;
      const z = cluster.position.z;
      const r = cluster.radius;
      
      minX = Math.min(minX, x - r);
      maxX = Math.max(maxX, x + r);
      minZ = Math.min(minZ, z - r);
      maxZ = Math.max(maxZ, z + r);
    });
    
    // Position camera to see all clusters
    const centerX = (minX + maxX) / 2;
    const centerZ = (minZ + maxZ) / 2;
    const width = maxX - minX;
    const height = maxZ - minZ;
    const maxDim = Math.max(width, height);
    
    this.camera.position.set(centerX, maxDim * 0.8, centerZ + maxDim * 1.2);
    this.camera.lookAt(centerX, 0, centerZ);
    this.controls.target.set(centerX, 0, centerZ);
    this.controls.update();
  }
  
  // Execute a query and create a ripple effect from the most relevant document
  executeQuery(queryText) {
    if (!queryText || !this.documents.length) return;
    
    // Create a new query object
    const queryId = Date.now().toString();
    const queryColor = this.colors.ripples[this.activeQueries.length % this.colors.ripples.length];
    
    const query = {
      id: queryId,
      text: queryText,
      color: queryColor,
      timestamp: Date.now()
    };
    
    // Find the most relevant document (in a real implementation, this would use embeddings)
    const relevantDocIndex = Math.floor(Math.random() * this.documents.length);
    const relevantDoc = this.documents[relevantDocIndex];
    
    // Create a ripple effect from the most relevant document
    this.createRipple(relevantDoc.position, queryColor, 1.0);
    
    // Add this query to active queries
    this.activeQueries.push(query);
    
    // Simulate finding other relevant documents with delayed ripples
    this.simulateRelevanceRipples(query);
    
    return query;
  }
  
  simulateRelevanceRipples(query) {
    // Simulate finding other relevant documents over time
    const relevanceCount = 2 + Math.floor(Math.random() * 5);
    
    for (let i = 0; i < relevanceCount; i++) {
      // Add some delay between ripples
      setTimeout(() => {
        // Select a random document (in real implementation, would be based on relevance)
        const randomDocIndex = Math.floor(Math.random() * this.documents.length);
        const doc = this.documents[randomDocIndex];
        
        // Randomize relevance score (0.3 - 0.9)
        const relevance = 0.3 + Math.random() * 0.6;
        
        // Only show ripples for documents above the relevance threshold
        if (relevance > this.settings.relevanceThreshold) {
          this.createRipple(doc.position, query.color, relevance);
        }
      }, 300 + i * 700); // Stagger the ripples
    }
  }
  
  createRipple(position, color, strength) {
    // Create a ripple effect geometry
    const rippleGeometry = new THREE.RingGeometry(1, 3, 32);
    const rippleMaterial = new THREE.MeshBasicMaterial({
      color: color,
      transparent: true,
      opacity: strength * 0.7,
      side: THREE.DoubleSide
    });
    
    const ripple = new THREE.Mesh(rippleGeometry, rippleMaterial);
    ripple.rotation.x = -Math.PI / 2;
    ripple.position.copy(position);
    ripple.position.y = 2;
    
    // Add ripple metadata
    ripple.userData = {
      startTime: this.clock.getElapsedTime(),
      lifetime: this.settings.rippleLifetime * (0.5 + strength * 0.5),
      strength: strength,
      baseColor: color,
      maxSize: this.settings.maxRippleSize * strength
    };
    
    this.ripplesGroup.add(ripple);
    this.ripples.push(ripple);
    
    return ripple;
  }
  
  updateRipples() {
    const currentTime = this.clock.getElapsedTime();
    const expiredRipples = [];
    
    // Update each ripple
    this.ripples.forEach(ripple => {
      const elapsed = currentTime - ripple.userData.startTime;
      const lifetime = ripple.userData.lifetime;
      
      // Check if ripple has expired
      if (elapsed > lifetime) {
        expiredRipples.push(ripple);
        return;
      }
      
      // Calculate current ripple size
      const progress = elapsed / lifetime;
      const size = ripple.userData.maxSize * Math.sin(progress * Math.PI);
      
      // Update ripple appearance
      ripple.scale.set(size, size, 1);
      
      // Fade out gradually
      const fadeStart = 0.7;
      let opacity = ripple.userData.strength * 0.7;
      
      if (progress > fadeStart) {
        opacity *= 1 - ((progress - fadeStart) / (1 - fadeStart));
      }
      
      ripple.material.opacity = opacity;
    });
    
    // Remove expired ripples
    expiredRipples.forEach(ripple => {
      this.ripplesGroup.remove(ripple);
      const index = this.ripples.indexOf(ripple);
      if (index > -1) {
        this.ripples.splice(index, 1);
      }
    });
  }
  
  clearQueries() {
    // Remove all active queries
    this.activeQueries = [];
    
    // Remove all ripples
    this.ripples.forEach(ripple => {
      this.ripplesGroup.remove(ripple);
    });
    
    this.ripples = [];
  }
  
  clearVisualization() {
    // Remove all document objects
    while (this.documentsGroup.children.length > 0) {
      const child = this.documentsGroup.children[0];
      this.documentsGroup.remove(child);
    }
    
    // Remove all ripples
    while (this.ripplesGroup.children.length > 0) {
      const child = this.ripplesGroup.children[0];
      this.ripplesGroup.remove(child);
    }
    
    this.ripples = [];
  }
  
  // Animation and rendering
  animate() {
    requestAnimationFrame(this.animate.bind(this));
    
    // Update controls
    this.controls.update();
    
    // Update ripples
    this.updateRipples();
    
    // Render the scene
    this.renderer.render(this.scene, this.camera);
  }
  
  // Event handlers
  onWindowResize() {
    this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
  }
  
  onMouseMove(event) {
    // Calculate mouse position in normalized device coordinates
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  }
  
  onMouseClick(event) {
    // Perform raycasting to detect clicked objects
    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.documentsGroup.children, true);
    
    if (intersects.length > 0) {
      // In a real implementation, this would show document details
      console.log('Document clicked:', intersects[0]);
      
      // Create a highlight ripple
      const position = intersects[0].point;
      this.createRipple(position, this.colors.highlights, 0.7);
    }
  }
  
  // Public API methods
  setRelevanceThreshold(threshold) {
    this.settings.relevanceThreshold = threshold;
  }
  
  setRippleSettings(settings) {
    this.settings = { ...this.settings, ...settings };
  }
}

export default KnowledgeSeismograph;