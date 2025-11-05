import pino from 'pino';
import { loadConfig } from './config';

const config = loadConfig();

export const logger = pino({
  level: config.logLevel,
  transport:
    process.env.NODE_ENV !== 'production'
      ? {
          target: 'pino-pretty',
          options: { colorize: true, translateTime: true },
        }
      : undefined,
});
