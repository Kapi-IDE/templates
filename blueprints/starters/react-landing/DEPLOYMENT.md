# Deployment Guide

## Prerequisites
- Node.js 18+
- npm or pnpm

## Local Build
```bash
npm install
npm run build
npm start
```

## Vercel
```bash
npm install
npx vercel deploy
```

## Netlify
1. Build command: `npm run build`
2. Publish directory: `.next`
3. Enable Next.js runtime

## Environment Variables
None required. Update email/phone links in `ContactSection.tsx` before launch.
