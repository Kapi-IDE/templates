# Express JWT Middleware

Production-ready JWT verification middleware extracted from the Practica blueprint. It parses plain or `Bearer` tokens, validates them with `jsonwebtoken`, attaches the decoded payload to `req.user`, and returns 401 on invalid/missing tokens.

## Install

```bash
npm install jsonwebtoken
npm install -D @types/jsonwebtoken  # if using TypeScript
```

## Usage

```ts
import express from 'express';
import { jwtVerifierMiddleware } from './src/jwt-middleware';

const app = express();
app.use(jwtVerifierMiddleware({ secret: process.env.JWT_SECRET! }));
```

Downstream handlers can access `req.user`.

