# Braine React Theme Starter

Production-ready Next.js starter that recreates the Braine digital agency HTML template with React components, the original styling, and a modern App Router structure.

## Features
- All theme sections ported to TypeScript components (header, hero, services, case studies, testimonials, contact, footer)
- Original CSS/JS assets bundled under `public/`
- Swiper-based carousel instead of jQuery plugins
- Metadata.json and deployment docs so you can ship quickly

## Getting Started
```bash
npm install
npm run dev
```

Open `http://localhost:3000` to view the landing page.

## Deployment
- Vercel: `npm run build && npx vercel deploy`
- Netlify: build command `npm run build`, publish `.next`
- Docker: standard Next.js runtime image

## Customisation
Edit copy and imagery in `src/components/*`, or gradually migrate styles into Tailwind classes if you prefer utility-first styling.
