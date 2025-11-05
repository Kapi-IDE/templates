# Express Service Skeleton

Production-quality Express bootstrap extracted from the Practica clean architecture blueprint and simplified to remove custom dependencies. Use it when you need a hardened HTTP layer with logging, security middleware, graceful startup/shutdown, and a sample router.

## What's Included

- `startWebServer`/`stopWebServer` lifecycle helpers for tests and CLI entrypoints
- Security and observability middleware (`helmet`, `cors`, `pino-http`)
- Request ID injection + structured logging
- Centralised error handler that emits JSON responses
- Example REST routes that delegate into a thin domain adapter
- Environment-driven configuration with sane defaults

The code mirrors the patterns used across the Practica blueprint so you can plug it directly into new Node.js quick wins without re-writing plumbing.

## Usage

```ts
import { startWebServer, stopWebServer } from './src/server';

async function main() {
  const address = await startWebServer();
  console.log(`Service started on ${address.port}`);
}

main();
```

During tests:

```ts
beforeAll(async () => {
  address = await startWebServer();
});

afterAll(async () => {
  await stopWebServer();
});
```

## Dependencies

Install the minimal runtime packages:

```bash
npm install express helmet cors pino pino-http pino-pretty http-errors nanoid dotenv
```

For TypeScript projects also install the types:

```bash
npm install -D typescript ts-node @types/express @types/node @types/cors @types/helmet
```

## Customisation

- Update `src/config.ts` to wire in your configuration provider
- Extend the router in `src/routes.ts`
- Replace `domain/order-service.ts` shim with real use cases

## Related Components

- `backend/web-servers/fastify-service` – Fastify flavour with the same conventions
- `backend/node-llm-framework` – Pair with Express to expose AI endpoints
