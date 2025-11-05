# Fastify Service Skeleton

Hardened Fastify bootstrap modelled after the Practica blueprint. It wires logging, Swagger, request context, security plugins, and graceful lifecycle helpers so you can stand up an API in minutes.

## Features

- `createServer`/`startServer`/`stopServer` lifecycle utilities
- Pino logging + per-request context via `asyncLocalStorage`
- `@fastify/swagger` + `@fastify/swagger-ui` with sensible defaults
- Health check and sample CRUD routes
- JWT-protected endpoints (middleware placeholder) and CORS/helmet equivalents

## Dependencies

```bash
npm install fastify @fastify/cors @fastify/helmet @fastify/swagger @fastify/swagger-ui pino nanoid http-errors
```

Optional extras:

```bash
npm install -D typescript ts-node @types/node
```

## Usage

```ts
import { startServer, stopServer } from './src/server';

(async () => {
  const address = await startServer();
  console.log(`Fastify listening on`, address.port);
})();
```

## Related Components

- `backend/web-servers/express-service`
- `backend/node-llm-framework`

