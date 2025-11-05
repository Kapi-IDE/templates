/**
 * Main App Component
 * Handles keyboard input and game loop
 */

import { useEffect, useRef } from 'react';
import { Scene } from './components/Scene';
import { UI } from './components/UI';
import { useGameStore } from './store/gameStore';
import './App.css';

function App() {
  const { moveBlock, dropBlock, pauseGame, tick, isPaused, gameOver, fallingBlock } =
    useGameStore();

  const gameLoopRef = useRef<number>();

  // Keyboard controls
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (gameOver) return;

      switch (e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          moveBlock('left');
          break;
        case 'ArrowRight':
          e.preventDefault();
          moveBlock('right');
          break;
        case 'ArrowDown':
          e.preventDefault();
          dropBlock();
          break;
        case ' ':
          e.preventDefault();
          pauseGame();
          break;
      }
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [moveBlock, dropBlock, pauseGame, gameOver]);

  // Game loop
  useEffect(() => {
    if (isPaused || gameOver || !fallingBlock) {
      if (gameLoopRef.current) {
        cancelAnimationFrame(gameLoopRef.current);
      }
      return;
    }

    let lastTickTime = Date.now();
    const tickInterval = 1000; // 1 second per tick

    function loop() {
      const now = Date.now();
      if (now - lastTickTime >= tickInterval) {
        tick();
        lastTickTime = now;
      }
      gameLoopRef.current = requestAnimationFrame(loop);
    }

    gameLoopRef.current = requestAnimationFrame(loop);

    return () => {
      if (gameLoopRef.current) {
        cancelAnimationFrame(gameLoopRef.current);
      }
    };
  }, [tick, isPaused, gameOver, fallingBlock]);

  return (
    <div className="app">
      <Scene />
      <UI />
    </div>
  );
}

export default App;
