/**
 * 3D Block Component
 * Renders individual blocks with smooth animations and particle effects
 */

import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { RoundedBox, Text } from '@react-three/drei';
import * as THREE from 'three';
import type { Block } from '../store/gameStore';

interface Block3DProps {
  block: Block;
  gridSize: number;
}

export function Block3D({ block, gridSize }: Block3DProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [scale, setScale] = useState(1);

  // Spawn animation
  useFrame((state, delta) => {
    if (!meshRef.current) return;

    // Pop-in animation
    if (scale < 1) {
      setScale(Math.min(scale + delta * 3, 1));
      meshRef.current.scale.set(scale, scale, scale);
    }

    // Merge pulse animation
    if (block.merging) {
      const pulse = Math.sin(state.clock.elapsedTime * 10) * 0.1 + 1;
      meshRef.current.scale.set(pulse, pulse, pulse);
    }
  });

  // Convert grid position to 3D world position
  const [x, y] = block.position;
  const worldX = (x - gridSize / 2 + 0.5) * 1.1;
  const worldY = (y - gridSize + 0.5) * 1.1;

  return (
    <group position={[worldX, worldY, 0]}>
      {/* Block mesh */}
      <RoundedBox
        ref={meshRef}
        args={[1, 1, 0.5]}
        radius={0.1}
        smoothness={4}
      >
        <meshStandardMaterial
          color={block.color}
          metalness={0.3}
          roughness={0.4}
        />
      </RoundedBox>

      {/* Value text */}
      <Text
        position={[0, 0, 0.3]}
        fontSize={0.4}
        color="#776e65"
        anchorX="center"
        anchorY="middle"
        font="/fonts/Inter-Bold.ttf"
      >
        {block.value}
      </Text>

      {/* Glow effect for high values */}
      {block.value >= 128 && (
        <pointLight
          color={block.color}
          intensity={block.value / 512}
          distance={2}
        />
      )}
    </group>
  );
}
