# 🎮 3D Puzzle Game - Tetris × 2048 Hybrid

**Stunning 3D puzzle game combining Tetris mechanics with 2048 merging**

Built with KAPI blueprints - Production-ready Three.js game in 25 minutes.

---

## 🎯 What It Is

A revolutionary 3D puzzle game that merges the best of two classic games:
- **Tetris-style** falling blocks
- **2048-style** number merging
- **Stunning 3D graphics** with particle effects
- **Smooth animations** and post-processing
- **Leaderboard system** with localStorage

**Game Mechanics:**
- Blocks with values (2, 4, 8, 16...) fall from the top
- Move blocks left/right with arrow keys
- Blocks merge when matching values collide vertically
- Merged blocks double in value (just like 2048!)
- Game ends when blocks reach the top

---

## 🚀 Quick Start (3 Minutes)

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Visit **http://localhost:3000** and start playing!

---

## 🎮 How to Play

### Controls
- **← →** - Move block left/right
- **↓** - Drop block instantly
- **Space** - Pause game

### Objective
1. Match blocks with the same number
2. Blocks merge and double in value
3. Create higher value blocks (2048, 4096, etc.)
4. Survive as long as possible
5. Beat your high score!

### Strategy Tips
- Plan ahead - blocks fall automatically
- Create columns of matching numbers
- Use the drop key strategically
- Watch for merge opportunities
- Don't let blocks reach the top!

---

## 📊 Features

### Core Gameplay
- ✅ **Falling blocks** with Tetris-style gravity
- ✅ **2048 merging** - identical values combine
- ✅ **Smooth physics** - blocks fall and stack realistically
- ✅ **Auto-merge** - matching blocks combine automatically
- ✅ **Progressive difficulty** - blocks fall faster as you score

### 3D Graphics
- ✅ **React Three Fiber** - Modern Three.js with React
- ✅ **Rounded 3D blocks** - Smooth, polished visuals
- ✅ **Dynamic lighting** - Point lights, directional lights
- ✅ **Particle field** - 100+ floating ambient particles
- ✅ **Glow effects** - High-value blocks emit light
- ✅ **Post-processing** - Bloom and vignette effects

### UI & UX
- ✅ **Clean overlay** - Score, controls, game state
- ✅ **Modal system** - Game over, pause, leaderboard
- ✅ **Keyboard controls** - Responsive arrow key input
- ✅ **Leaderboard** - Top 10 scores with names
- ✅ **High score tracking** - Persistent localStorage

### Animations
- ✅ **Pop-in effect** - Blocks spawn with bounce
- ✅ **Merge pulse** - Blocks glow when merging
- ✅ **Particle motion** - Ambient particles float and bounce
- ✅ **Camera controls** - Limited orbit for better view

---

## 🏗️ Tech Stack

### Core
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool (fast HMR)

### 3D Graphics
- **Three.js**: 3D rendering library
- **React Three Fiber**: React renderer for Three.js
- **React Three Drei**: Useful helpers (RoundedBox, Text, etc.)
- **React Three Postprocessing**: Bloom, vignette effects

### State Management
- **Zustand**: Lightweight state management (< 1KB)
- **localStorage**: Persistent high scores and leaderboard

### Utilities
- **Leva**: Debug controls (optional)

---

## 📁 Project Structure

```
threejs-puzzle-game/
├── src/
│   ├── store/
│   │   └── gameStore.ts          # Zustand state management
│   ├── components/
│   │   ├── Scene.tsx              # Main 3D scene setup
│   │   ├── GameGrid.tsx           # Grid and block rendering
│   │   ├── Block3D.tsx            # Individual 3D block
│   │   ├── ParticleField.tsx      # Ambient particle effects
│   │   ├── UI.tsx                 # Game overlay and modals
│   │   └── UI.css                 # UI styles
│   ├── App.tsx                    # Main app with game loop
│   ├── App.css                    # Global styles
│   └── main.tsx                   # Entry point
├── index.html
├── vite.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

---

## 🎨 Game Architecture

### State Management (Zustand)

```typescript
interface GameState {
  grid: (Block | null)[][];      // 6×12 grid
  score: number;
  highScore: number;
  gameOver: boolean;
  isPaused: boolean;
  fallingBlock: Block | null;    // Currently falling block
  fallSpeed: number;

  // Actions
  startGame: () => void;
  moveBlock: (direction) => void;
  dropBlock: () => void;
  tick: () => void;              // Game loop update
  mergeBlocks: () => void;       // 2048-style merging
}
```

### Block Interface

```typescript
interface Block {
  id: string;
  value: number;                 // 2, 4, 8, 16, 32, etc.
  position: [number, number];    // [x, y] grid coords
  color: string;                 // 2048-style color mapping
  merging?: boolean;             // Animation flag
}
```

### Game Loop

1. **Tick** (every 1 second):
   - Move falling block down 1 grid space
   - Check collision with bottom or other blocks
   - If collision: place block in grid

2. **After Placement**:
   - Run merge algorithm (check vertical matches)
   - Apply gravity (blocks fall down)
   - Spawn new block at top
   - Check game over condition

3. **Merge Algorithm**:
   - Scan from bottom to top
   - If two adjacent blocks have same value: merge
   - Merged block = 2× value, new color
   - Award points equal to new value

---

## 🎮 3D Rendering Details

### Scene Setup

```typescript
<Canvas>
  <PerspectiveCamera position={[0, 0, 15]} fov={50} />
  <ambientLight intensity={0.3} />
  <directionalLight position={[5, 10, 5]} intensity={0.8} />
  <pointLight position={[-5, 5, 5]} color="#4a90e2" />

  <GameGrid />
  <OrbitControls enableZoom={false} />
  <Environment preset="night" />

  <EffectComposer>
    <Bloom />
    <Vignette />
  </EffectComposer>
</Canvas>
```

### Block Rendering

```typescript
<RoundedBox args={[1, 1, 0.5]} radius={0.1}>
  <meshStandardMaterial
    color={block.color}
    metalness={0.3}
    roughness={0.4}
  />
</RoundedBox>

<Text
  position={[0, 0, 0.3]}
  fontSize={0.4}
  color="#776e65"
>
  {block.value}
</Text>
```

### Particle System

- **100 particles** floating in 3D space
- **Random velocities** with boundary bouncing
- **Color gradient** (blue → purple → pink)
- **Additive blending** for glow effect
- **Slow rotation** of entire field

---

## 🎯 Customization

### Change Grid Size

Edit `src/store/gameStore.ts`:

```typescript
export const GRID_WIDTH = 8;   // Default: 6
export const GRID_HEIGHT = 16; // Default: 12
```

### Add New Block Values

```typescript
const VALUE_COLORS: Record<number, string> = {
  2: '#eee4da',
  4: '#ede0c8',
  // Add more...
  4096: '#ff0000',
  8192: '#00ff00',
};
```

### Adjust Fall Speed

```typescript
const tickInterval = 800; // Faster (default: 1000ms)
```

### Change Particle Count

```typescript
<ParticleField count={200} /> // More particles (default: 100)
```

### Custom Colors

Edit UI.css:

```css
.game-title h1 {
  background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output in `dist/` directory.

### Deploy to Vercel

```bash
npm i -g vercel
vercel
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
```

---

## 🎓 Educational Value

This project demonstrates:

### 1. **Modern 3D Web Development**
- React Three Fiber patterns
- Declarative 3D scene composition
- Component-based 3D graphics
- Performance optimization

### 2. **Game Development**
- Game loop implementation
- State management for games
- Collision detection
- Physics simulation
- Score tracking

### 3. **Advanced React Patterns**
- Custom hooks for game logic
- useFrame for animations
- useRef for Three.js meshes
- Effect management

### 4. **3D Graphics Concepts**
- Lighting (ambient, directional, point)
- Materials (metalness, roughness)
- Post-processing effects
- Particle systems
- Camera controls

### 5. **TypeScript Best Practices**
- Interface design
- Type-safe state management
- Generic components
- Proper typing for libraries

---

## 🐛 Troubleshooting

### WebGL Not Supported

**Error**: "WebGL not supported"

**Solution**: Use a modern browser (Chrome, Firefox, Edge, Safari)

### Performance Issues

**Solutions**:
1. Reduce particle count: `<ParticleField count={50} />`
2. Disable post-processing effects
3. Lower grid size
4. Close other browser tabs

### Blocks Not Merging

**Check**:
- Blocks must have exact same value
- Blocks must be vertically adjacent
- Merge happens after block is placed

### Leaderboard Not Saving

**Solution**: Check browser localStorage permissions

```javascript
// Test in console
localStorage.setItem('test', '1');
console.log(localStorage.getItem('test'));
```

---

## 🔮 Future Enhancements

### Gameplay
- [ ] **Tetris shapes**: L, T, S, Z pieces
- [ ] **Power-ups**: Bomb (clear column), Shuffle, Undo
- [ ] **Multiplayer**: Real-time competition
- [ ] **Time attack mode**: Score under time limit
- [ ] **Challenge mode**: Reach 2048 in X moves

### Graphics
- [ ] **Custom shaders**: GLSL effects
- [ ] **Explosion effects**: Particle burst on merge
- [ ] **Trail effects**: Block leaves trail
- [ ] **Background music**: Dynamic soundtrack
- [ ] **Sound effects**: Satisfying merge sounds

### Features
- [ ] **Daily challenges**: New puzzle each day
- [ ] **Achievements**: Unlock badges
- [ ] **Skins**: Different block themes
- [ ] **Mobile controls**: Touch/swipe support
- [ ] **Tutorial mode**: Interactive guide

---

## 📚 Learning Resources

**Three.js**:
- [Three.js Documentation](https://threejs.org/docs/)
- [Three.js Journey Course](https://threejs-journey.com/)

**React Three Fiber**:
- [R3F Documentation](https://docs.pmnd.rs/react-three-fiber/)
- [R3F Examples](https://docs.pmnd.rs/react-three-fiber/getting-started/examples)

**Game Development**:
- [Tetris Tutorial](https://www.freecodecamp.org/news/how-to-code-tetris/)
- [2048 Algorithm Explained](https://gabrielecirulli.github.io/2048/)

**Zustand**:
- [Zustand Guide](https://docs.pmnd.rs/zustand/)

---

## 📄 License

MIT - Free for personal and commercial use

---

## 🙏 Acknowledgments

- **Inspiration**: Tetris (1984), 2048 (Gabriele Cirulli)
- **Libraries**: Three.js, React Three Fiber, Zustand
- **Particle Patterns**: Based on react-particles-webgl
- **3D Patterns**: Inspired by baseten/react-three-2048
- **Built with**: KAPI Production Game Blueprints

---

**Built with KAPI** - From idea to production in 25 minutes

**Questions?** Check the source code comments for detailed explanations.
