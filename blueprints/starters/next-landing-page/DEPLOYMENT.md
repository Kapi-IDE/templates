# Deployment Guide

## Prerequisites
- Node.js 18+
- npm or pnpm
- Optional: Vercel CLI for one-command deploy

## Local Build
```bash
npm install
npm run build
npm start
```
The app listens on port 3000.

## Vercel
```bash
npm install
npx vercel deploy
```
Use the defaults; Vercel detects Next.js automatically.

## Netlify
1. Create a new site from GitHub.
2. Set build command to `npm run build` and publish directory to `.next`.
3. Enable Next.js runtime in Netlify UI (automatic with latest Next).

## Environment Variables
None required for the starter. Replace `https://example.com/api/waitlist` in `CallToAction.tsx` and `WaitlistModal.tsx` with your form endpoint.
