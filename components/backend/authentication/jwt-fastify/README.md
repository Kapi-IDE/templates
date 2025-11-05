# Fastify JWT Plugin

Fastify plugin that validates bearer tokens and decorates `request.user`, extracted from the Practica blueprint.

## Install

```bash
npm install jsonwebtoken fastify-plugin
```

## Usage

```ts
import fastify from 'fastify';
import { JWTVerifier } from './src/jwt-plugin';

const app = fastify();
await app.register(JWTVerifier, { secret: process.env.JWT_SECRET! });
```

The plugin rejects unauthenticated requests with 401 and exposes the decoded payload as `request.user`.

