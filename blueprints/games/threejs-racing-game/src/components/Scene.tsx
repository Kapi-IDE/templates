/**
 * Main 3D Scene
 * Sets up physics world, camera, lighting, and renders game objects
 */

import { Canvas } from '@react-three/fiber';
import { Sky, Environment } from '@react-three/drei';
import { Physics } from '@react-three/cannon';
import { Vehicle } from './Vehicle';
import { Track } from './Track';

export function Scene() {
  return (
    <Canvas
      shadows
      camera={{ position: [0, 5, -10], fov: 75 }}
      gl={{ antialias: true }}
    >
      {/* Sky */}
      <Sky
        distance={450000}
        sunPosition={[100, 20, 100]}
        inclination={0.6}
        azimuth={0.25}
      />

      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight
        position={[50, 50, 50]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-left={-50}
        shadow-camera-right={50}
        shadow-camera-top={50}
        shadow-camera-bottom={-50}
      />
      <hemisphereLight
        skyColor="#87CEEB"
        groundColor="#2d3436"
        intensity={0.3}
      />

      {/* Environment reflections */}
      <Environment preset="sunset" />

      {/* Physics world */}
      <Physics
        gravity={[0, -30, 0]}
        defaultContactMaterial={{
          friction: 0.9,
          restitution: 0.1,
        }}
      >
        {/* Track */}
        <Track />

        {/* Player vehicle */}
        <Vehicle
          position={[0, 2, 0]}
          rotation={[0, 0, 0]}
          playerId="player1"
          isPlayer={true}
        />

        {/* TODO: Add multiplayer vehicles here */}
      </Physics>
    </Canvas>
  );
}
