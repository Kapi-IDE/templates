/**
 * Game State Management with Zustand
 * Manages grid, score, game status, and block positions
 */

import { create } from 'zustand';

export interface Block {
  id: string;
  value: number; // 2, 4, 8, 16, 32, etc.
  position: [number, number]; // [x, y] grid coordinates
  color: string;
  merging?: boolean; // Animation flag
}

interface GameState {
  // Game data
  grid: (Block | null)[][];
  score: number;
  highScore: number;
  gameOver: boolean;
  isPaused: boolean;

  // Current falling block
  fallingBlock: Block | null;
  fallSpeed: number; // Blocks per second

  // Actions
  startGame: () => void;
  resetGame: () => void;
  pauseGame: () => void;
  moveBlock: (direction: 'left' | 'right') => void;
  rotateBlock: () => void; // For future Tetris mode
  dropBlock: () => void;
  tick: () => void; // Game loop update
  mergeBlocks: () => void;
}

// Grid dimensions
export const GRID_WIDTH = 6;
export const GRID_HEIGHT = 12;

// Value to color mapping (2048 style)
const VALUE_COLORS: Record<number, string> = {
  2: '#eee4da',
  4: '#ede0c8',
  8: '#f2b179',
  16: '#f59563',
  32: '#f67c5f',
  64: '#f65e3b',
  128: '#edcf72',
  256: '#edcc61',
  512: '#edc850',
  1024: '#edc53f',
  2048: '#edc22e',
};

function createEmptyGrid(): (Block | null)[][] {
  return Array(GRID_HEIGHT)
    .fill(null)
    .map(() => Array(GRID_WIDTH).fill(null));
}

function generateRandomValue(): number {
  return Math.random() < 0.9 ? 2 : 4;
}

function createBlock(x: number, y: number): Block {
  const value = generateRandomValue();
  return {
    id: Math.random().toString(36).substring(7),
    value,
    position: [x, y],
    color: VALUE_COLORS[value] || '#3c3a32',
  };
}

export const useGameStore = create<GameState>((set, get) => ({
  grid: createEmptyGrid(),
  score: 0,
  highScore: parseInt(localStorage.getItem('highScore') || '0'),
  gameOver: false,
  isPaused: false,
  fallingBlock: null,
  fallSpeed: 1,

  startGame: () => {
    const newBlock = createBlock(Math.floor(GRID_WIDTH / 2), 0);
    set({
      grid: createEmptyGrid(),
      score: 0,
      gameOver: false,
      isPaused: false,
      fallingBlock: newBlock,
    });
  },

  resetGame: () => {
    get().startGame();
  },

  pauseGame: () => {
    set(state => ({ isPaused: !state.isPaused }));
  },

  moveBlock: (direction: 'left' | 'right') => {
    const { fallingBlock, grid } = get();
    if (!fallingBlock || get().isPaused) return;

    const [x, y] = fallingBlock.position;
    const newX = direction === 'left' ? x - 1 : x + 1;

    // Check boundaries
    if (newX < 0 || newX >= GRID_WIDTH) return;

    // Check collision with existing blocks
    if (grid[y] && grid[y][newX]) return;

    set({
      fallingBlock: {
        ...fallingBlock,
        position: [newX, y],
      },
    });
  },

  rotateBlock: () => {
    // Future: Add rotation for Tetris shapes
    console.log('Rotation not implemented yet');
  },

  dropBlock: () => {
    const { fallingBlock } = get();
    if (!fallingBlock || get().isPaused) return;

    // Drop block to the bottom
    let y = fallingBlock.position[1];
    const x = fallingBlock.position[0];
    const grid = get().grid;

    while (y < GRID_HEIGHT - 1 && !grid[y + 1][x]) {
      y++;
    }

    set({
      fallingBlock: {
        ...fallingBlock,
        position: [x, y],
      },
    });

    // Immediately place the block
    setTimeout(() => get().tick(), 100);
  },

  tick: () => {
    const { fallingBlock, grid, isPaused } = get();
    if (!fallingBlock || isPaused) return;

    const [x, y] = fallingBlock.position;
    const newY = y + 1;

    // Check if block reached bottom or landed on another block
    if (newY >= GRID_HEIGHT || (grid[newY] && grid[newY][x])) {
      // Place block in grid
      const newGrid = grid.map(row => [...row]);
      newGrid[y][x] = { ...fallingBlock };

      set({ grid: newGrid, fallingBlock: null });

      // Merge blocks and spawn new block
      setTimeout(() => {
        get().mergeBlocks();

        // Check game over
        const topRow = get().grid[0];
        if (topRow.some(cell => cell !== null)) {
          const highScore = Math.max(get().score, get().highScore);
          localStorage.setItem('highScore', highScore.toString());
          set({ gameOver: true, highScore });
          return;
        }

        // Spawn new block
        const newBlock = createBlock(Math.floor(GRID_WIDTH / 2), 0);
        set({ fallingBlock: newBlock });
      }, 200);
    } else {
      // Continue falling
      set({
        fallingBlock: {
          ...fallingBlock,
          position: [x, newY],
        },
      });
    }
  },

  mergeBlocks: () => {
    const { grid, score } = get();
    let newGrid = grid.map(row => [...row]);
    let newScore = score;
    let merged = false;

    // Check for vertical merges (2048 style)
    for (let y = GRID_HEIGHT - 2; y >= 0; y--) {
      for (let x = 0; x < GRID_WIDTH; x++) {
        const current = newGrid[y][x];
        const below = newGrid[y + 1][x];

        if (current && below && current.value === below.value) {
          // Merge blocks
          const newValue = current.value * 2;
          newGrid[y + 1][x] = {
            ...current,
            value: newValue,
            color: VALUE_COLORS[newValue] || '#3c3a32',
            merging: true,
          };
          newGrid[y][x] = null;
          newScore += newValue;
          merged = true;
        }
      }
    }

    // Apply gravity (blocks fall down)
    if (merged) {
      for (let x = 0; x < GRID_WIDTH; x++) {
        const column = [];
        for (let y = 0; y < GRID_HEIGHT; y++) {
          if (newGrid[y][x]) {
            column.push(newGrid[y][x]);
          }
        }

        // Fill column from bottom
        for (let y = 0; y < GRID_HEIGHT; y++) {
          newGrid[y][x] = null;
        }

        for (let i = 0; i < column.length; i++) {
          newGrid[GRID_HEIGHT - column.length + i][x] = column[i];
        }
      }
    }

    set({ grid: newGrid, score: newScore });
  },
}));
