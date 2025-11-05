/**
 * Game UI Overlay
 * HUD, race timer, lap counter, controls hint
 */

import { useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { useGameStore } from '../store/gameStore';
import './UI.css';

export function UI() {
  const {
    gameStarted,
    raceTime,
    lapTime,
    bestLapTime,
    currentLap,
    totalLaps,
    startRace,
    resetRace,
    updateRaceTime,
  } = useGameStore();

  // Game loop - update race time
  useEffect(() => {
    if (!gameStarted) return;

    const interval = setInterval(() => {
      updateRaceTime(0.016); // ~60 FPS
    }, 16);

    return () => clearInterval(interval);
  }, [gameStarted, updateRaceTime]);

  function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 1000);
    return `${mins}:${secs.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`;
  }

  return (
    <div className="race-ui">
      {/* HUD */}
      {gameStarted && (
        <div className="hud">
          {/* Race Timer */}
          <div className="hud-panel time-panel">
            <div className="label">Race Time</div>
            <div className="value">{formatTime(raceTime)}</div>
          </div>

          {/* Lap Info */}
          <div className="hud-panel lap-panel">
            <div className="label">Lap</div>
            <div className="value">
              {currentLap}/{totalLaps}
            </div>
          </div>

          {/* Lap Time */}
          <div className="hud-panel lap-time-panel">
            <div className="label">Lap Time</div>
            <div className="value">{formatTime(lapTime)}</div>
          </div>

          {/* Best Lap */}
          {bestLapTime !== Infinity && (
            <div className="hud-panel best-lap-panel">
              <div className="label">Best Lap</div>
              <div className="value">{formatTime(bestLapTime)}</div>
            </div>
          )}

          {/* Speed (placeholder) */}
          <div className="hud-panel speed-panel">
            <div className="speedometer">
              <div className="speed-value">0</div>
              <div className="speed-unit">MPH</div>
            </div>
          </div>
        </div>
      )}

      {/* Controls Hint */}
      {!gameStarted && (
        <div className="controls-hint">
          <h3>Controls</h3>
          <div className="control-row">
            <kbd>W</kbd> or <kbd>↑</kbd> - Accelerate
          </div>
          <div className="control-row">
            <kbd>S</kbd> or <kbd>↓</kbd> - Reverse
          </div>
          <div className="control-row">
            <kbd>A</kbd> / <kbd>D</kbd> or <kbd>←</kbd> / <kbd>→</kbd> - Steer
          </div>
          <div className="control-row">
            <kbd>Space</kbd> - Brake
          </div>
        </div>
      )}

      {/* Start Screen */}
      {!gameStarted && (
        <div className="start-screen">
          <h1 className="game-title">🏁 Racing Legends</h1>
          <p className="game-subtitle">Physics-Based 3D Racing</p>

          <button className="btn-primary btn-large" onClick={startRace}>
            Start Race
          </button>

          <div className="race-info">
            <div className="info-item">
              <span className="info-label">Laps:</span>
              <span className="info-value">{totalLaps}</span>
            </div>
            {bestLapTime !== Infinity && (
              <div className="info-item">
                <span className="info-label">Best Lap:</span>
                <span className="info-value">{formatTime(bestLapTime)}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Race Complete */}
      {!gameStarted && raceTime > 0 && (
        <div className="modal-overlay">
          <div className="modal race-complete">
            <h2>🏆 Race Complete!</h2>

            <div className="race-stats">
              <div className="stat">
                <div className="stat-label">Total Time</div>
                <div className="stat-value">{formatTime(raceTime)}</div>
              </div>
              {bestLapTime !== Infinity && (
                <div className="stat">
                  <div className="stat-label">Best Lap</div>
                  <div className="stat-value">{formatTime(bestLapTime)}</div>
                </div>
              )}
            </div>

            <div className="modal-actions">
              <button className="btn-primary" onClick={resetRace}>
                Race Again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Watermark */}
      <div className="watermark">Built with KAPI</div>
    </div>
  );
}
