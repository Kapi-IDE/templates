# Turbo Racer 3D

**Game #21** - Physics-based 3D racing game with React Three Fiber + Cannon.js

Build a complete racing game in 30 minutes with realistic physics, multiple tracks, and mobile support.

## ✨ Features

### Core Gameplay
- **Realistic Physics**: Powered by Cannon.js physics engine
- **3D Graphics**: React Three Fiber (Three.js for React)
- **5 Race Tracks**: City, Desert, Mountain, Coastal, Night Circuit
- **4 Game Modes**: Time Trial, Race, Drift Challenge, Elimination
- **Power-Ups**: Speed Boost, Shield, Jump, Slow Opponents
- **Checkpoints & Laps**: Complete 3-lap races with checkpoint validation
- **Collision Detection**: Realistic car-to-car and car-to-barrier physics
- **Drift System**: Earn points for controlled drifts

### Controls
- **Desktop**: Arrow keys or WASD + Space for brake/drift
- **Mobile**: Touch controls with virtual joystick
- **Gamepad**: Full Xbox/PlayStation controller support

### Visual Effects
- **Particle System**: Tire smoke, sparks, dust trails
- **Dynamic Camera**: Follow cam, chase cam, first-person views
- **Weather Effects**: Rain, fog, day/night cycle
- **Post-Processing**: Bloom, motion blur, depth of field
- **Car Customization**: 10+ colors, spoilers, decals

### Technical Features
- **60 FPS Target**: Optimized physics and rendering
- **Responsive**: Works on desktop, tablet, mobile
- **Progressive Loading**: Assets load on-demand
- **Local Storage**: Save best times and settings
- **Replay System**: Watch your best races
- **Performance Scaling**: Auto-adjust graphics based on device

## 🚀 Quick Start (30 minutes)

### Prerequisites
- Node.js 18+
- Modern browser with WebGL 2.0 support
- **NO API keys or backend required!**

### Setup

```bash
# 1. Clone/copy this directory
cd racing-game

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

Visit http://localhost:3000 and start racing!

### Build for Production

```bash
# Build optimized bundle
npm run build

# Test production build locally
npm run start

# Deploy to Vercel (FREE)
vercel

# Or deploy to Netlify
netlify deploy
```

## 🎮 How to Play

### Desktop Controls

```
┌─────────────────────────────────────────────┐
│  W / ↑        : Accelerate                  │
│  S / ↓        : Brake / Reverse             │
│  A / ←        : Steer Left                  │
│  D / →        : Steer Right                 │
│  SPACE        : Drift / Handbrake           │
│  SHIFT        : Nitro Boost                 │
│  C            : Change Camera               │
│  R            : Reset Car                   │
│  ESC          : Pause Menu                  │
└─────────────────────────────────────────────┘
```

### Mobile Controls

```
┌─────────────────────────────────────────────┐
│  🕹️ Left Joystick  : Steer Left/Right      │
│  🔼 Right Buttons  : Accelerate/Brake       │
│  💨 Boost Button   : Nitro Boost            │
│  🎯 Drift Button   : Handbrake/Drift        │
└─────────────────────────────────────────────┘
```

### Gameplay Tips

1. **Drifting**: Hold SPACE while turning to drift around corners
   - Longer drifts = More points
   - Perfect drifts = Nitro boost refill

2. **Power-Ups**: Drive through colored zones to collect
   - 🔵 Speed Boost (5 seconds)
   - 🟢 Shield (protect from collisions)
   - 🟡 Jump (launch over obstacles)
   - 🔴 Slow Opponents (in Race mode)

3. **Checkpoints**: Must pass through all checkpoints in order
   - Missing checkpoint = Time penalty
   - Lap doesn't count if checkpoints missed

4. **Best Lines**: Study track layouts for optimal racing lines
   - Brake before corners, not during
   - Accelerate out of corners
   - Use drift for tight turns

## 🏁 Game Modes

### 1. Time Trial

**Objective**: Complete 3 laps in fastest time

```
Solo racing against the clock
- No opponents
- Ghost car of your best time
- Power-ups disabled
- Pure driving skill
```

**Leaderboard**: Local best times per track

### 2. Race

**Objective**: Finish first against 7 AI opponents

```
- 8 total racers
- 3 laps
- Power-ups enabled
- Aggressive AI
- Points for finishing position
```

**Difficulty Levels**:
- Easy: AI makes mistakes, slower reactions
- Medium: Competitive AI, occasional mistakes
- Hard: Expert AI, rare mistakes
- Expert: Perfect AI, uses optimal lines

### 3. Drift Challenge

**Objective**: Score maximum drift points

```
- 5-minute time limit
- Points for controlled drifts
- Combo multiplier (chain drifts)
- Bonus zones (2x points)
- Penalties for wall hits
```

**Scoring**:
- Short drift (1-2 sec): 100 points
- Medium drift (2-4 sec): 300 points
- Long drift (4+ sec): 600 points
- Perfect drift (no corrections): 2x multiplier

### 4. Elimination

**Objective**: Don't be last!

```
- Every 30 seconds, last place is eliminated
- Start with 8 racers, end with 1
- Intense pressure racing
- Power-ups enabled
- Sudden death rounds
```

## 🏎️ Tracks

### 1. Sunset City

**Difficulty**: ⭐⭐☆☆☆ (Easy)

```
- Urban street circuit
- Wide corners
- Gentle elevation changes
- Perfect for beginners
- Best time: 1:42.5
```

**Highlights**: Skyscrapers, neon lights, traffic

### 2. Desert Storm

**Difficulty**: ⭐⭐⭐☆☆ (Medium)

```
- Off-road sand dunes
- Sharp elevation changes
- Loose surface (more sliding)
- Sandstorm weather effect
- Best time: 2:03.8
```

**Highlights**: Canyon jumps, oasis checkpoint

### 3. Mountain Pass

**Difficulty**: ⭐⭐⭐⭐☆ (Hard)

```
- Hairpin turns
- Steep elevation changes
- Narrow track (guard rails)
- Challenging for drifting
- Best time: 2:15.3
```

**Highlights**: Scenic overlooks, tunnels

### 4. Coastal Highway

**Difficulty**: ⭐⭐⭐☆☆ (Medium)

```
- Ocean views
- High-speed straights
- Beach sections
- Dynamic time of day
- Best time: 1:55.7
```

**Highlights**: Pier jump, lighthouse turn

### 5. Night Circuit

**Difficulty**: ⭐⭐⭐⭐⭐ (Expert)

```
- Formula-style race track
- Technical corners
- High-speed chicanes
- Nighttime lighting
- Best time: 1:38.2
```

**Highlights**: Pit lane shortcut, bridge section

## 🎨 Graphics Settings

### Performance Presets

**Low** (Mobile/Low-end):
- 30 FPS target
- Simple shadows
- Low particle count
- Reduced draw distance
- No post-processing

**Medium** (Default):
- 60 FPS target
- Dynamic shadows
- Medium particles
- Standard draw distance
- Basic bloom

**High** (Recommended):
- 60 FPS target
- High-quality shadows
- Full particles
- Extended draw distance
- Full post-processing

**Ultra** (High-end PC):
- 120 FPS target
- Ray-traced shadows
- Maximum particles
- Unlimited draw distance
- Advanced effects

### Custom Settings

```typescript
// Adjust individual settings
const graphics = {
  shadowQuality: 'high',      // low, medium, high, ultra
  particles: true,            // particle effects
  postProcessing: true,       // bloom, motion blur
  antialiasing: true,         // smoother edges
  drawDistance: 1000,         // meters
  reflections: true,          // car reflections
  weatherEffects: true,       // rain, fog, etc.
};
```

## 🏗️ Architecture

```
racing-game/
├── src/
│   ├── components/
│   │   ├── Game.tsx                # Main game component
│   │   ├── Car.tsx                 # Player car with physics
│   │   ├── AIcar.tsx               # AI opponent
│   │   ├── Track.tsx               # Track geometry
│   │   ├── Checkpoint.tsx          # Lap validation
│   │   ├── PowerUp.tsx             # Collectible power-ups
│   │   ├── Camera.tsx              # Dynamic camera
│   │   ├── ParticleSystem.tsx      # Visual effects
│   │   ├── UI/
│   │   │   ├── HUD.tsx             # Speedometer, lap time, position
│   │   │   ├── Menu.tsx            # Main menu
│   │   │   ├── PauseMenu.tsx       # In-game menu
│   │   │   ├── Leaderboard.tsx     # Best times
│   │   │   └── MobileControls.tsx  # Touch controls
│   │   └── Effects/
│   │       ├── TireSmoke.tsx       # Drift smoke
│   │       ├── Sparks.tsx          # Collision sparks
│   │       └── MotionBlur.tsx      # Speed effect
│   ├── hooks/
│   │   ├── usePhysics.ts           # Cannon.js physics
│   │   ├── useControls.ts          # Input handling
│   │   ├── useAI.ts                # AI logic
│   │   └── useGameState.ts         # Game state management
│   ├── lib/
│   │   ├── physics.ts              # Physics configuration
│   │   ├── tracks.ts               # Track definitions
│   │   ├── cars.ts                 # Car specifications
│   │   └── audio.ts                # Sound effects
│   ├── assets/
│   │   ├── models/                 # 3D car models (.glb)
│   │   ├── textures/               # Track textures
│   │   ├── sounds/                 # Engine, drift, collision
│   │   └── music/                  # Background music
│   └── app/
│       └── page.tsx                # Next.js entry point
└── public/
    └── assets/                     # Static assets
```

## 🎯 Component Reuse

This blueprint is **100% self-contained** - no external KAPI components needed!

**Custom Components Built**:
- ✅ React Three Fiber game loop
- ✅ Cannon.js physics integration
- ✅ Mobile touch controls
- ✅ AI opponent logic
- ✅ Particle system
- ✅ HUD and menus

**External Libraries Used**:
- `@react-three/fiber` - React renderer for Three.js
- `@react-three/drei` - Useful Three.js helpers
- `@react-three/cannon` - Physics for React
- `zustand` - State management
- `three` - 3D graphics library

**Token Savings**: ~40% by using established game libraries

## 💰 Pricing

### Development: FREE
- ✅ All libraries are free and open-source
- ✅ No API keys required
- ✅ No backend needed
- ✅ Runs completely client-side

### Hosting: FREE
- Vercel: FREE for static sites
- Netlify: FREE for static sites
- GitHub Pages: FREE
- Cloudflare Pages: FREE

**Total Monthly Cost**: $0

## 🚀 Deployment

### Vercel (Recommended)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Production
vercel --prod
```

**Result**: `https://your-game.vercel.app`

### Netlify

```bash
# 1. Install Netlify CLI
npm i -g netlify-cli

# 2. Build
npm run build

# 3. Deploy
netlify deploy --prod
```

### GitHub Pages

```bash
# 1. Build
npm run build

# 2. Add to package.json:
"homepage": "https://yourusername.github.io/racing-game"

# 3. Deploy
npm run deploy  # (requires gh-pages package)
```

## 🎮 Advanced Features

### Custom Car Models

Replace default car with your own 3D model:

```typescript
// 1. Export car from Blender as .glb
// 2. Add to /public/assets/models/my-car.glb
// 3. Update Car component:

import { useGLTF } from '@react-three/drei';

function CustomCar() {
  const { scene } = useGLTF('/assets/models/my-car.glb');
  return <primitive object={scene} />;
}
```

### Add New Tracks

Create custom race tracks:

```typescript
// lib/tracks.ts
export const customTrack = {
  id: 'custom',
  name: 'My Track',
  difficulty: 3,
  laps: 3,
  checkpoints: [
    { position: [0, 0, 100], radius: 20 },
    { position: [50, 0, 150], radius: 20 },
    // ... more checkpoints
  ],
  startPosition: [0, 2, 0],
  weather: 'clear',
  timeOfDay: 'day',
};
```

### Multiplayer (Future)

Framework ready for multiplayer:

```typescript
// Add WebSocket connection
import { io } from 'socket.io-client';

const socket = io(process.env.NEXT_PUBLIC_MULTIPLAYER_SERVER);

// Sync car positions
socket.on('car-update', (data) => {
  updateOpponentCar(data.id, data.position, data.rotation);
});
```

## 🐛 Troubleshooting

### "Low FPS / Laggy gameplay"

**Solution**: Lower graphics settings

```typescript
// Set to Low preset
setGraphicsPreset('low');

// Or disable specific features
setSettings({
  particles: false,
  shadows: false,
  postProcessing: false
});
```

### "Physics behaving strangely"

**Solution**: Check physics step rate

```typescript
// Increase physics substeps for more accuracy
useFrame((state, delta) => {
  const maxSubSteps = 10;
  world.step(1 / 60, delta, maxSubSteps);
});
```

### "Car flips over easily"

**Solution**: Adjust center of mass

```typescript
// Lower center of gravity
const carBody = new CANNON.Body({
  mass: 1200,
  position: new CANNON.Vec3(0, 0.5, 0), // Lower Y value
  shape: carShape,
});
```

### "Mobile controls not responsive"

**Solution**: Adjust touch sensitivity

```typescript
const TOUCH_SENSITIVITY = {
  steering: 2.0,  // Increase for more responsive steering
  acceleration: 1.5,
};
```

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build**:

1. ✅ **Specification**: Complete 3D racing game with physics
2. ✅ **Architecture**: React Three Fiber + Cannon.js integration
3. ✅ **Implementation**: Modular components, reusable hooks
4. ✅ **Quality Gates**: Performance targets, mobile testing

**Learning Path**:
- Three.js fundamentals
- Physics engine integration
- Game loop optimization
- Touch control implementation
- Performance profiling

## 📚 Resources

**React Three Fiber**:
- [Documentation](https://docs.pmnd.rs/react-three-fiber)
- [Examples](https://codesandbox.io/examples/package/@react-three/fiber)

**Cannon.js Physics**:
- [Documentation](https://pmndrs.github.io/cannon-es/)
- [React Integration](https://github.com/pmndrs/use-cannon)

**Three.js**:
- [Documentation](https://threejs.org/docs/)
- [Examples](https://threejs.org/examples/)

**Game Development**:
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [WebGL Fundamentals](https://webglfundamentals.org/)

## 📄 License

MIT - Free for commercial and personal use

---

**Built with KAPI** - Stop vibe coding. Start engineering.

**Play now**: https://turbo-racer-demo.vercel.app (demo link)
