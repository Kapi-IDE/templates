# 🏁 Racing Legends - 3D Physics Racing Game

**Realistic physics-based racing with React Three Fiber + Cannon.js**

Built with KAPI blueprints - Production-ready racing game in 30 minutes.

---

## 🎯 Features

- **Realistic Physics**: Cannon.js raycast vehicle with suspension
- **Mobile Controls**: Virtual joystick + throttle/brake buttons
- **Lap System**: 3 laps with checkpoints and timing
- **Camera Follow**: Smooth third-person camera
- **Multiplayer-Ready**: Zustand state architecture for networking
- **Beautiful 3D**: Sky, shadows, environment reflections

---

## 🚀 Quick Start

```bash
npm install
npm run dev
```

Visit **http://localhost:3000**

---

## 🎮 Controls

**Keyboard:**
- W/↑ - Accelerate
- S/↓ - Reverse
- A/D or ←/→ - Steer
- Space - Brake

**Mobile:**
- Left joystick - Steering
- Gas button - Accelerate
- Brake button - Brake

---

## 🏗️ Tech Stack

- React Three Fiber
- @react-three/cannon (Physics)
- @react-three/drei (Helpers)
- Zustand (State)
- TypeScript
- Vite

---

## 📁 Structure

```
src/
├── components/
│   ├── Vehicle.tsx         # Raycast vehicle with Cannon.js
│   ├── Track.tsx           # Ground, barriers, checkpoints
│   ├── Scene.tsx           # 3D scene setup
│   ├── UI.tsx              # HUD, timer, lap counter
│   └── MobileControls.tsx  # Touch controls
├── store/
│   └── gameStore.ts        # Zustand state (multiplayer-ready)
└── App.tsx                 # Keyboard controls & game loop
```

---

## 🎮 Vehicle Physics

- **Chassis**: 150kg mass with damping
- **Wheels**: 4 wheels with raycast suspension
- **Suspension**: Stiffness 30, travel 0.3
- **Steering**: ±0.5 rad clamp
- **Engine**: 500 max force
- **Friction**: 2.0 slip, 0.01 roll influence

---

## 🌐 Multiplayer Integration

The game is architected for multiplayer:

1. **State Management**: Zustand separates local/remote players
2. **Player Data**: Position, rotation, velocity synced
3. **WebSocket Ready**: Add socket.io or Colyseus
4. **Vehicle Instances**: Render remote players with same Vehicle component

**Example Integration:**
```typescript
// Add WebSocket client
const socket = io('ws://localhost:3001');

// Broadcast position
socket.emit('playerUpdate', { id, position, rotation });

// Receive remote players
socket.on('playersUpdate', (players) => {
  players.forEach(p => updatePlayer(p.id, p));
});
```

---

## 🔧 Customization

**Adjust Vehicle Speed:**
```typescript
// In Vehicle.tsx
const VEHICLE_CONFIG = {
  maxForce: 800, // Faster acceleration
  maxSpeed: 50,  // Higher top speed
};
```

**Change Track Size:**
```typescript
// In Track.tsx - Ground component
<planeGeometry args={[300, 300]} /> // Bigger track
```

**Add More Laps:**
```typescript
// In gameStore.ts
totalLaps: 5,
```

---

## 🚀 Deployment

```bash
npm run build
# Deploy dist/ to Vercel, Netlify, etc.
```

---

## 📄 License

MIT

---

**Built with KAPI** - Production-ready in 30 minutes
