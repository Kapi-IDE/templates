/**
 * 3D Game Grid Component
 * Renders the playing field and all blocks
 */

import { Block3D } from './Block3D';
import { ParticleField } from './ParticleField';
import { useGameStore, GRID_WIDTH, GRID_HEIGHT } from '../store/gameStore';

export function GameGrid() {
  const { grid, fallingBlock } = useGameStore();

  return (
    <group>
      {/* Background grid lines */}
      <gridHelper
        args={[GRID_HEIGHT * 1.1, GRID_HEIGHT, '#444', '#222']}
        rotation={[Math.PI / 2, 0, 0]}
        position={[0, 0, -0.3]}
      />

      {/* Border frame */}
      <lineSegments>
        <edgesGeometry
          attach="geometry"
          args={[
            new THREE.BoxGeometry(
              GRID_WIDTH * 1.1,
              GRID_HEIGHT * 1.1,
              0.1
            ),
          ]}
        />
        <lineBasicMaterial attach="material" color="#666" linewidth={2} />
      </lineSegments>

      {/* Render all grid blocks */}
      {grid.map((row, y) =>
        row.map((block, x) =>
          block ? (
            <Block3D
              key={block.id}
              block={block}
              gridSize={GRID_WIDTH}
            />
          ) : null
        )
      )}

      {/* Render falling block */}
      {fallingBlock && (
        <Block3D
          key={fallingBlock.id}
          block={fallingBlock}
          gridSize={GRID_WIDTH}
        />
      )}

      {/* Ambient particle field */}
      <ParticleField count={100} />
    </group>
  );
}
