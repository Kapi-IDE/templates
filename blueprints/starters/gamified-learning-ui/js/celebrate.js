/*
More designs from: https://confetti.js.org/more.html
*/
const defaults = {
  spread: 360,
  ticks: 100,
  gravity: 0,
  decay: 0.94,
  startVelocity: 30,
};

function shoot() {
  confetti({
      ...defaults,
      particleCount: 30,
      scalar: 1.2,
      shapes: ["circle", "square"],
      colors: ["#a864fd", "#29cdff", "#78ff44", "#ff718d", "#fdff6a"],
  });

  confetti({
      ...defaults,
      particleCount: 20,
      scalar: 2,
      shapes: ["emoji"],
      shapeOptions: {
          emoji: {
              value: ["🧠", "🌈"],
          },
      },
  });
}

setTimeout(shoot, 1500); // 1-second delay
setTimeout(shoot, 1600); // 1.1-second delay
setTimeout(shoot, 1700); // 1.2-second delay
