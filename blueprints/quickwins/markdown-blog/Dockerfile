FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build static site
RUN npm run build

# Production image - serve with simple HTTP server
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/out ./out

# Install simple HTTP server
RUN npm install -g serve

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["serve", "-s", "out", "-l", "3000"]
