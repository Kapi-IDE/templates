/**
 * Mobile Touch Controls
 * Virtual joystick for steering and throttle buttons
 */

import { useRef, useState, TouchEvent } from 'react';
import { useGameStore } from '../store/gameStore';
import './MobileControls.css';

export function MobileControls() {
  const { setTouchSteering, setTouchThrottle, setTouchBrake } = useGameStore();

  const [steeringActive, setSteeringActive] = useState(false);
  const [steeringPos, setSteeringPos] = useState({ x: 0, y: 0 });

  const joystickRef = useRef<HTMLDivElement>(null);

  // Steering joystick
  function handleSteeringStart(e: TouchEvent<HTMLDivElement>) {
    setSteeringActive(true);
    updateSteering(e);
  }

  function handleSteeringMove(e: TouchEvent<HTMLDivElement>) {
    if (!steeringActive) return;
    updateSteering(e);
  }

  function handleSteeringEnd() {
    setSteeringActive(false);
    setSteeringPos({ x: 0, y: 0 });
    setTouchSteering(0);
  }

  function updateSteering(e: TouchEvent<HTMLDivElement>) {
    if (!joystickRef.current) return;

    const touch = e.touches[0];
    const rect = joystickRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const deltaX = touch.clientX - centerX;
    const deltaY = touch.clientY - centerY;

    const maxDistance = rect.width / 2;
    const distance = Math.min(
      Math.sqrt(deltaX * deltaX + deltaY * deltaY),
      maxDistance
    );
    const angle = Math.atan2(deltaY, deltaX);

    const x = Math.cos(angle) * distance;
    const y = Math.sin(angle) * distance;

    setSteeringPos({ x, y });

    // Normalize steering (-1 to 1)
    const steering = x / maxDistance;
    setTouchSteering(steering);
  }

  return (
    <div className="mobile-controls">
      {/* Steering Joystick (left side) */}
      <div
        ref={joystickRef}
        className="joystick-container"
        onTouchStart={handleSteeringStart}
        onTouchMove={handleSteeringMove}
        onTouchEnd={handleSteeringEnd}
      >
        <div className="joystick-base">
          <div
            className="joystick-stick"
            style={{
              transform: `translate(${steeringPos.x}px, ${steeringPos.y}px)`,
            }}
          />
        </div>
        <div className="joystick-label">Steering</div>
      </div>

      {/* Throttle & Brake (right side) */}
      <div className="button-controls">
        {/* Throttle */}
        <button
          className="control-btn throttle-btn"
          onTouchStart={() => setTouchThrottle(1)}
          onTouchEnd={() => setTouchThrottle(0)}
        >
          <div className="btn-icon">↑</div>
          <div className="btn-label">Gas</div>
        </button>

        {/* Brake */}
        <button
          className="control-btn brake-btn"
          onTouchStart={() => setTouchBrake(true)}
          onTouchEnd={() => setTouchBrake(false)}
        >
          <div className="btn-icon">■</div>
          <div className="btn-label">Brake</div>
        </button>
      </div>
    </div>
  );
}
