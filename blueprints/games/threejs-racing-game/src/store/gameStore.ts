/**
 * Game State Management with Zustand
 * Controls, game state, multiplayer data
 */

import { create } from 'zustand';

export interface Controls {
  forward: boolean;
  backward: boolean;
  left: boolean;
  right: boolean;
  brake: boolean;
}

export interface Player {
  id: string;
  name: string;
  position: [number, number, number];
  rotation: [number, number, number];
  velocity: [number, number, number];
  color: string;
}

interface GameState {
  // Controls
  controls: Controls;
  setControl: (key: keyof Controls, value: boolean) => void;

  // Touch controls (mobile)
  touchControls: {
    steering: number; // -1 to 1
    throttle: number; // 0 to 1
    brake: boolean;
  };
  setTouchSteering: (value: number) => void;
  setTouchThrottle: (value: number) => void;
  setTouchBrake: (value: boolean) => void;

  // Game state
  gameStarted: boolean;
  raceTime: number;
  lapTime: number;
  bestLapTime: number;
  currentLap: number;
  totalLaps: number;
  checkpoints: boolean[];

  // Actions
  startRace: () => void;
  resetRace: () => void;
  updateRaceTime: (delta: number) => void;
  completeCheckpoint: (index: number) => void;
  completeLap: () => void;

  // Multiplayer
  players: Map<string, Player>;
  localPlayerId: string;
  addPlayer: (player: Player) => void;
  removePlayer: (playerId: string) => void;
  updatePlayer: (playerId: string, data: Partial<Player>) => void;
}

export const useGameStore = create<GameState>((set, get) => ({
  // Controls
  controls: {
    forward: false,
    backward: false,
    left: false,
    right: false,
    brake: false,
  },

  setControl: (key, value) => {
    set(state => ({
      controls: { ...state.controls, [key]: value },
    }));
  },

  // Touch controls
  touchControls: {
    steering: 0,
    throttle: 0,
    brake: false,
  },

  setTouchSteering: steering =>
    set(state => ({
      touchControls: { ...state.touchControls, steering },
    })),

  setTouchThrottle: throttle =>
    set(state => ({
      touchControls: { ...state.touchControls, throttle },
    })),

  setTouchBrake: brake =>
    set(state => ({
      touchControls: { ...state.touchControls, brake },
    })),

  // Game state
  gameStarted: false,
  raceTime: 0,
  lapTime: 0,
  bestLapTime: Infinity,
  currentLap: 0,
  totalLaps: 3,
  checkpoints: [false, false, false, false],

  startRace: () => {
    set({
      gameStarted: true,
      raceTime: 0,
      lapTime: 0,
      currentLap: 1,
      checkpoints: [false, false, false, false],
    });
  },

  resetRace: () => {
    set({
      gameStarted: false,
      raceTime: 0,
      lapTime: 0,
      currentLap: 0,
      checkpoints: [false, false, false, false],
    });
  },

  updateRaceTime: delta => {
    if (!get().gameStarted) return;

    set(state => ({
      raceTime: state.raceTime + delta,
      lapTime: state.lapTime + delta,
    }));
  },

  completeCheckpoint: index => {
    set(state => {
      const newCheckpoints = [...state.checkpoints];
      newCheckpoints[index] = true;
      return { checkpoints: newCheckpoints };
    });
  },

  completeLap: () => {
    const { lapTime, bestLapTime, currentLap, totalLaps, checkpoints } = get();

    // Check if all checkpoints were hit
    const allCheckpointsComplete = checkpoints.every(c => c);
    if (!allCheckpointsComplete) return;

    // Update best lap time
    const newBestLap = Math.min(lapTime, bestLapTime);

    // Check if race is complete
    if (currentLap >= totalLaps) {
      set({
        gameStarted: false,
        bestLapTime: newBestLap,
      });

      // Save to localStorage
      const savedBestLap = localStorage.getItem('bestLapTime');
      if (!savedBestLap || newBestLap < parseFloat(savedBestLap)) {
        localStorage.setItem('bestLapTime', newBestLap.toString());
      }
    } else {
      set({
        currentLap: currentLap + 1,
        lapTime: 0,
        bestLapTime: newBestLap,
        checkpoints: [false, false, false, false],
      });
    }
  },

  // Multiplayer
  players: new Map(),
  localPlayerId: Math.random().toString(36).substring(7),

  addPlayer: player => {
    set(state => {
      const newPlayers = new Map(state.players);
      newPlayers.set(player.id, player);
      return { players: newPlayers };
    });
  },

  removePlayer: playerId => {
    set(state => {
      const newPlayers = new Map(state.players);
      newPlayers.delete(playerId);
      return { players: newPlayers };
    });
  },

  updatePlayer: (playerId, data) => {
    set(state => {
      const newPlayers = new Map(state.players);
      const player = newPlayers.get(playerId);
      if (player) {
        newPlayers.set(playerId, { ...player, ...data });
      }
      return { players: newPlayers };
    });
  },
}));
