/**
 * Game UI Overlay
 * Score, controls, game over screen, leaderboard
 */

import { useEffect, useState } from 'react';
import { useGameStore } from '../store/gameStore';
import './UI.css';

export function UI() {
  const {
    score,
    highScore,
    gameOver,
    isPaused,
    startGame,
    resetGame,
    pauseGame,
  } = useGameStore();

  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [leaderboard, setLeaderboard] = useState<Array<{ name: string; score: number }>>([]);

  // Load leaderboard from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('leaderboard');
    if (saved) {
      setLeaderboard(JSON.parse(saved));
    }
  }, []);

  // Save score to leaderboard
  function saveScore(name: string) {
    const newEntry = { name, score };
    const newLeaderboard = [...leaderboard, newEntry]
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    localStorage.setItem('leaderboard', JSON.stringify(newLeaderboard));
    setLeaderboard(newLeaderboard);
    setShowLeaderboard(true);
  }

  return (
    <div className="ui-overlay">
      {/* Header */}
      <div className="game-header">
        <div className="game-title">
          <h1>3D Puzzle</h1>
          <p className="subtitle">Tetris × 2048</p>
        </div>

        <div className="score-panel">
          <div className="score-box">
            <div className="label">Score</div>
            <div className="value">{score}</div>
          </div>
          <div className="score-box best">
            <div className="label">Best</div>
            <div className="value">{highScore}</div>
          </div>
        </div>
      </div>

      {/* Controls Help */}
      {!gameOver && (
        <div className="controls-hint">
          <div className="key-hint">
            <kbd>←</kbd> <kbd>→</kbd> Move
          </div>
          <div className="key-hint">
            <kbd>↓</kbd> Drop
          </div>
          <div className="key-hint">
            <kbd>Space</kbd> Pause
          </div>
        </div>
      )}

      {/* Game Over Screen */}
      {gameOver && (
        <div className="modal-overlay">
          <div className="modal game-over">
            <h2>Game Over</h2>
            <div className="final-score">
              <div className="label">Final Score</div>
              <div className="value">{score}</div>
            </div>

            {score > 0 && (
              <div className="save-score">
                <input
                  type="text"
                  placeholder="Enter your name"
                  maxLength={20}
                  onKeyDown={e => {
                    if (e.key === 'Enter' && e.currentTarget.value.trim()) {
                      saveScore(e.currentTarget.value.trim());
                    }
                  }}
                />
                <button
                  onClick={e => {
                    const input = e.currentTarget.previousSibling as HTMLInputElement;
                    if (input.value.trim()) {
                      saveScore(input.value.trim());
                    }
                  }}
                >
                  Save Score
                </button>
              </div>
            )}

            <div className="modal-actions">
              <button className="btn-primary" onClick={resetGame}>
                Play Again
              </button>
              <button
                className="btn-secondary"
                onClick={() => setShowLeaderboard(true)}
              >
                Leaderboard
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Pause Screen */}
      {isPaused && !gameOver && (
        <div className="modal-overlay">
          <div className="modal pause-screen">
            <h2>Paused</h2>
            <button className="btn-primary" onClick={pauseGame}>
              Resume
            </button>
            <button className="btn-secondary" onClick={resetGame}>
              Restart
            </button>
          </div>
        </div>
      )}

      {/* Leaderboard */}
      {showLeaderboard && (
        <div className="modal-overlay">
          <div className="modal leaderboard">
            <h2>🏆 Leaderboard</h2>
            <div className="leaderboard-list">
              {leaderboard.length === 0 ? (
                <p className="empty-state">No scores yet!</p>
              ) : (
                leaderboard.map((entry, index) => (
                  <div key={index} className="leaderboard-entry">
                    <div className="rank">#{index + 1}</div>
                    <div className="name">{entry.name}</div>
                    <div className="score">{entry.score}</div>
                  </div>
                ))
              )}
            </div>
            <button
              className="btn-secondary"
              onClick={() => setShowLeaderboard(false)}
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Start Screen */}
      {!gameOver && score === 0 && !isPaused && (
        <div className="start-screen">
          <button className="btn-primary btn-large" onClick={startGame}>
            Start Game
          </button>
          <button
            className="btn-secondary"
            onClick={() => setShowLeaderboard(true)}
          >
            View Leaderboard
          </button>
        </div>
      )}
    </div>
  );
}
