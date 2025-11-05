/**
 * Main App Component
 * Handles keyboard controls and game loop
 */

import { useEffect } from 'react';
import { Scene } from './components/Scene';
import { UI } from './components/UI';
import { MobileControls } from './components/MobileControls';
import { useGameStore } from './store/gameStore';
import './App.css';

function App() {
  const { setControl } = useGameStore();

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key.toLowerCase()) {
        case 'w':
        case 'arrowup':
          setControl('forward', true);
          break;
        case 's':
        case 'arrowdown':
          setControl('backward', true);
          break;
        case 'a':
        case 'arrowleft':
          setControl('left', true);
          break;
        case 'd':
        case 'arrowright':
          setControl('right', true);
          break;
        case ' ':
          e.preventDefault();
          setControl('brake', true);
          break;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      switch (e.key.toLowerCase()) {
        case 'w':
        case 'arrowup':
          setControl('forward', false);
          break;
        case 's':
        case 'arrowdown':
          setControl('backward', false);
          break;
        case 'a':
        case 'arrowleft':
          setControl('left', false);
          break;
        case 'd':
        case 'arrowright':
          setControl('right', false);
          break;
        case ' ':
          setControl('brake', false);
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [setControl]);

  return (
    <div className="app">
      <Scene />
      <UI />
      <MobileControls />
    </div>
  );
}

export default App;
