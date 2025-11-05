/**
 * Vehicle Component with Cannon.js Physics
 * Realistic car physics with suspension, friction, and controls
 */

import { useRef, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { useBox, useRaycastVehicle } from '@react-three/cannon';
import { Vector3 } from 'three';
import * as THREE from 'three';
import { useGameStore } from '../store/gameStore';

interface VehicleProps {
  position: [number, number, number];
  rotation?: [number, number, number];
  playerId?: string;
  isPlayer?: boolean;
}

// Vehicle configuration
const CHASSIS_CONFIG = {
  mass: 150,
  position: [0, 1, 0] as [number, number, number],
  args: [1.5, 0.6, 3] as [number, number, number], // width, height, length
};

const WHEEL_CONFIG = {
  radius: 0.4,
  mass: 15,
  width: 0.3,
};

const VEHICLE_CONFIG = {
  maxForce: 500,
  maxBrakeForce: 50,
  steeringClamp: 0.5,
  maxSpeed: 30,
};

export function Vehicle({ position, rotation = [0, 0, 0], playerId = 'player1', isPlayer = true }: VehicleProps) {
  const { controls } = useGameStore();

  // Chassis (car body)
  const [chassisBody, chassisApi] = useBox(
    () => ({
      mass: CHASSIS_CONFIG.mass,
      position,
      rotation,
      args: CHASSIS_CONFIG.args,
      linearDamping: 0.3,
      angularDamping: 0.3,
    }),
    useRef<THREE.Mesh>(null)
  );

  // Wheels
  const wheelPositions: [number, number, number][] = [
    [-0.6, 0, 1.0],  // Front left
    [0.6, 0, 1.0],   // Front right
    [-0.6, 0, -1.0], // Rear left
    [0.6, 0, -1.0],  // Rear right
  ];

  const wheels = wheelPositions.map(() =>
    useBox(
      () => ({
        mass: WHEEL_CONFIG.mass,
        type: 'Kinematic',
        collisionFilterGroup: 0,
        args: [WHEEL_CONFIG.width, WHEEL_CONFIG.radius * 2, WHEEL_CONFIG.radius * 2],
      }),
      useRef<THREE.Mesh>(null)
    )
  );

  // Vehicle physics
  const [vehicle, vehicleApi] = useRaycastVehicle(
    () => ({
      chassisBody,
      wheels: wheels.map(w => w[0]),
      wheelInfos: wheelPositions.map((position, index) => ({
        radius: WHEEL_CONFIG.radius,
        directionLocal: [0, -1, 0],
        axleLocal: [1, 0, 0],
        suspensionStiffness: 30,
        suspensionRestLength: 0.3,
        maxSuspensionForce: 100000,
        maxSuspensionTravel: 0.3,
        dampingRelaxation: 10,
        dampingCompression: 4.4,
        frictionSlip: 2,
        rollInfluence: 0.01,
        useCustomSlidingRotationalSpeed: true,
        customSlidingRotationalSpeed: -30,
        isFrontWheel: index < 2,
        chassisConnectionPointLocal: position,
      })),
      indexForwardAxis: 2,
      indexRightAxis: 0,
      indexUpAxis: 1,
    }),
    useRef(null)
  );

  // Control vehicle based on input
  useFrame(() => {
    if (!isPlayer || !vehicleApi) return;

    const { forward, backward, left, right, brake } = controls;

    // Engine force (acceleration)
    const force = forward ? -VEHICLE_CONFIG.maxForce : backward ? VEHICLE_CONFIG.maxForce : 0;

    // Braking
    const brakeForce = brake ? VEHICLE_CONFIG.maxBrakeForce : 0;

    // Steering
    const steer = left ? VEHICLE_CONFIG.steeringClamp : right ? -VEHICLE_CONFIG.steeringClamp : 0;

    // Apply to front wheels (steering)
    vehicleApi.applyEngineForce(force, 2);
    vehicleApi.applyEngineForce(force, 3);

    vehicleApi.setSteeringValue(steer, 0);
    vehicleApi.setSteeringValue(steer, 1);

    // Apply brakes to all wheels
    for (let i = 0; i < 4; i++) {
      vehicleApi.setBrake(brakeForce, i);
    }
  });

  // Update camera position to follow vehicle
  useFrame(({ camera }) => {
    if (!isPlayer || !chassisBody.current) return;

    const chassisPosition = new Vector3();
    chassisBody.current.getWorldPosition(chassisPosition);

    const chassisRotation = new THREE.Euler();
    chassisBody.current.getWorldQuaternion(new THREE.Quaternion()).normalize();

    // Camera offset behind and above car
    const cameraOffset = new Vector3(0, 3, -8);
    const cameraRotation = new THREE.Quaternion();
    chassisBody.current.getWorldQuaternion(cameraRotation);

    cameraOffset.applyQuaternion(cameraRotation);
    const targetPosition = chassisPosition.clone().add(cameraOffset);

    // Smooth camera follow
    camera.position.lerp(targetPosition, 0.1);
    camera.lookAt(chassisPosition);
  });

  return (
    <group ref={vehicle}>
      {/* Chassis (car body) */}
      <mesh ref={chassisBody} castShadow>
        <boxGeometry args={CHASSIS_CONFIG.args} />
        <meshStandardMaterial
          color={isPlayer ? '#e63946' : '#1d3557'}
          metalness={0.8}
          roughness={0.2}
        />

        {/* Windshield */}
        <mesh position={[0, 0.4, 0.5]} rotation={[0.3, 0, 0]} castShadow>
          <boxGeometry args={[1.3, 0.4, 1.2]} />
          <meshStandardMaterial
            color="#88ccee"
            transparent
            opacity={0.6}
            metalness={0.9}
            roughness={0.1}
          />
        </mesh>
      </mesh>

      {/* Wheels */}
      {wheels.map(([wheelRef], index) => (
        <mesh key={index} ref={wheelRef} castShadow>
          <cylinderGeometry args={[WHEEL_CONFIG.radius, WHEEL_CONFIG.radius, WHEEL_CONFIG.width, 16]} />
          <meshStandardMaterial color="#1a1a1a" />
        </mesh>
      ))}

      {/* Headlights */}
      <spotLight
        position={[0.5, 0.3, 1.5]}
        angle={0.5}
        penumbra={0.5}
        intensity={20}
        distance={30}
        castShadow
      />
      <spotLight
        position={[-0.5, 0.3, 1.5]}
        angle={0.5}
        penumbra={0.5}
        intensity={20}
        distance={30}
        castShadow
      />
    </group>
  );
}
