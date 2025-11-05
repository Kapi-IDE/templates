import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';
import { nanoid } from 'nanoid';
import { registerRoutes } from './routes';

let app: FastifyInstance | null = null;

export async function createServer() {
  const server = Fastify({ logger: true });

  await server.register(cors);
  await server.register(helmet);
  await server.register(swagger, {
    openapi: {
      info: {
        title: 'Fastify Service',
        version: '1.0.0',
      },
    },
  });
  await server.register(swaggerUi, { routePrefix: '/docs' });

  server.addHook('onRequest', async (request) => {
    request.id ??= nanoid();
  });

  await registerRoutes(server);

  return server;
}

export async function startServer(port = Number(process.env.PORT || 3000)) {
  if (!app) {
    app = await createServer();
    await app.listen({ port, host: '0.0.0.0' });
  }
  return app.server.address();
}

export async function stopServer() {
  if (!app) return;
  await app.close();
  app = null;
}
