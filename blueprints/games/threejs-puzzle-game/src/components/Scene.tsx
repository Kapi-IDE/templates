/**
 * Main 3D Scene Component
 * Sets up camera, lighting, and controls
 */

import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing';
import { GameGrid } from './GameGrid';

export function Scene() {
  return (
    <Canvas
      shadows
      gl={{ antialias: true }}
      style={{ background: '#0a0a0a' }}
    >
      {/* Camera */}
      <PerspectiveCamera
        makeDefault
        position={[0, 0, 15]}
        fov={50}
      />

      {/* Lighting */}
      <ambientLight intensity={0.3} />
      <directionalLight
        position={[5, 10, 5]}
        intensity={0.8}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <pointLight position={[-5, 5, 5]} intensity={0.5} color="#4a90e2" />
      <pointLight position={[5, -5, -5]} intensity={0.5} color="#e24a90" />

      {/* Game grid */}
      <GameGrid />

      {/* Camera controls (limited for gameplay) */}
      <OrbitControls
        enableZoom={false}
        enablePan={false}
        minPolarAngle={Math.PI / 3}
        maxPolarAngle={Math.PI / 2}
        minAzimuthAngle={-Math.PI / 6}
        maxAzimuthAngle={Math.PI / 6}
      />

      {/* Environment map for reflections */}
      <Environment preset="night" />

      {/* Post-processing effects */}
      <EffectComposer>
        <Bloom
          intensity={0.3}
          luminanceThreshold={0.9}
          luminanceSmoothing={0.9}
        />
        <Vignette
          offset={0.3}
          darkness={0.5}
        />
      </EffectComposer>
    </Canvas>
  );
}
