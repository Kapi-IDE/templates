import { Server } from 'http';
import { AddressInfo } from 'net';
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import pinoHttp from 'pino-http';
import { nanoid } from 'nanoid';
import { loadConfig } from './config';
import { logger } from './logger';
import { registerRoutes } from './routes';

let connection: Server | null = null;

export async function startWebServer(): Promise<AddressInfo> {
  if (connection) {
    return connection.address() as AddressInfo;
  }

  const config = loadConfig();
  const app = express();

  app.use(assignRequestId);
  app.use(pinoHttp({ logger }));
  app.use(helmet());
  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  registerRoutes(app);
  app.get('/health', (_req, res) => res.json({ status: 'ok' }));
  app.use(errorHandler);

  await new Promise<void>((resolve) => {
    connection = app.listen(config.port, () => {
      const address = connection?.address() as AddressInfo;
      logger.info({ address }, 'Express service is listening');
      resolve();
    });
  });

  return connection.address() as AddressInfo;
}

export async function stopWebServer() {
  if (!connection) return;
  await new Promise<void>((resolve) => connection?.close(() => resolve()));
  connection = null;
}

function assignRequestId(
  req: express.Request,
  _res: express.Response,
  next: express.NextFunction
) {
  (req as express.Request & { id?: string }).id = nanoid();
  next();
}

function errorHandler(
  error: unknown,
  _req: express.Request,
  res: express.Response,
  _next: express.NextFunction
) {
  logger.error({ err: error }, 'Request failed');
  const status =
    (error as any)?.statusCode ||
    (error as any)?.status ||
    500;
  res.status(status).json({ message: 'Unexpected error' });
}
