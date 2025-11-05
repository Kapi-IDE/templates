/**
 * Race Track Component
 * Ground plane, barriers, checkpoints, and track decorations
 */

import { usePlane, useBox } from '@react-three/cannon';
import { useRef } from 'react';
import * as THREE from 'three';

export function Track() {
  return (
    <group>
      <Ground />
      <TrackBoundaries />
      <Checkpoints />
      <StartFinishLine />
      <TrackDecorations />
    </group>
  );
}

// Ground plane with physics
function Ground() {
  const [ref] = usePlane(
    () => ({
      type: 'Static',
      rotation: [-Math.PI / 2, 0, 0],
      material: {
        friction: 0.8,
        restitution: 0.1,
      },
    }),
    useRef<THREE.Mesh>(null)
  );

  return (
    <mesh ref={ref} receiveShadow>
      <planeGeometry args={[200, 200]} />
      <meshStandardMaterial
        color="#2d3436"
        roughness={0.9}
        metalness={0.1}
      />
    </mesh>
  );
}

// Track barriers (invisible collision walls)
function TrackBoundaries() {
  const barriers: Array<{
    position: [number, number, number];
    args: [number, number, number];
    rotation?: [number, number, number];
  }> = [
    // Outer walls
    { position: [0, 2.5, 50], args: [100, 5, 1] },
    { position: [0, 2.5, -50], args: [100, 5, 1] },
    { position: [50, 2.5, 0], args: [1, 5, 100], rotation: [0, Math.PI / 2, 0] },
    { position: [-50, 2.5, 0], args: [1, 5, 100], rotation: [0, Math.PI / 2, 0] },
  ];

  return (
    <>
      {barriers.map((barrier, index) => (
        <Barrier key={index} {...barrier} />
      ))}
    </>
  );
}

function Barrier({
  position,
  args,
  rotation = [0, 0, 0],
}: {
  position: [number, number, number];
  args: [number, number, number];
  rotation?: [number, number, number];
}) {
  const [ref] = useBox(
    () => ({
      type: 'Static',
      position,
      rotation,
      args,
    }),
    useRef<THREE.Mesh>(null)
  );

  return (
    <mesh ref={ref} castShadow receiveShadow>
      <boxGeometry args={args} />
      <meshStandardMaterial
        color="#e74c3c"
        transparent
        opacity={0.3}
        wireframe
      />
    </mesh>
  );
}

// Checkpoints (visual markers)
function Checkpoints() {
  const checkpointPositions: [number, number, number][] = [
    [0, 0.1, 20],
    [20, 0.1, 20],
    [20, 0.1, -20],
    [-20, 0.1, -20],
  ];

  return (
    <>
      {checkpointPositions.map((position, index) => (
        <mesh key={index} position={position} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[3, 4, 32]} />
          <meshStandardMaterial
            color="#f1c40f"
            emissive="#f1c40f"
            emissiveIntensity={0.5}
            transparent
            opacity={0.6}
            side={THREE.DoubleSide}
          />
        </mesh>
      ))}
    </>
  );
}

// Start/Finish line
function StartFinishLine() {
  return (
    <group position={[0, 0.1, 0]}>
      {/* Checkered pattern */}
      {Array.from({ length: 10 }).map((_, i) => (
        <mesh
          key={i}
          position={[(i - 4.5) * 1.5, 0, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[1.4, 5]} />
          <meshStandardMaterial
            color={i % 2 === 0 ? '#ffffff' : '#000000'}
            roughness={0.8}
          />
        </mesh>
      ))}

      {/* Finish line arch */}
      <mesh position={[0, 3, 0]}>
        <boxGeometry args={[15, 0.5, 0.5]} />
        <meshStandardMaterial color="#f1c40f" />
      </mesh>
      <mesh position={[-7, 1.5, 0]}>
        <boxGeometry args={[0.5, 3, 0.5]} />
        <meshStandardMaterial color="#f1c40f" />
      </mesh>
      <mesh position={[7, 1.5, 0]}>
        <boxGeometry args={[0.5, 3, 0.5]} />
        <meshStandardMaterial color="#f1c40f" />
      </mesh>
    </group>
  );
}

// Track decorations (trees, buildings, etc.)
function TrackDecorations() {
  // Simple trees around the track
  const treePositions: [number, number, number][] = [
    [-40, 0, -40],
    [-30, 0, -40],
    [30, 0, -40],
    [40, 0, -40],
    [-40, 0, 40],
    [40, 0, 40],
  ];

  return (
    <>
      {treePositions.map((position, index) => (
        <group key={index} position={position}>
          {/* Trunk */}
          <mesh position={[0, 2, 0]} castShadow>
            <cylinderGeometry args={[0.5, 0.7, 4, 8]} />
            <meshStandardMaterial color="#8B4513" />
          </mesh>

          {/* Foliage */}
          <mesh position={[0, 5, 0]} castShadow>
            <coneGeometry args={[2.5, 4, 8]} />
            <meshStandardMaterial color="#2d5016" />
          </mesh>
        </group>
      ))}
    </>
  );
}
