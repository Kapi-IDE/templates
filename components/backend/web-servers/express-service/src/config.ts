import dotenv from 'dotenv';

dotenv.config();

export type ServiceConfig = {
  port: number;
  jwtSecret: string;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
};

export function loadConfig(): ServiceConfig {
  return {
    port: Number(process.env.PORT || 3000),
    jwtSecret: process.env.JWT_SECRET || 'dev-secret-change-me',
    logLevel: (process.env.LOG_LEVEL as ServiceConfig['logLevel']) || 'info',
  };
}
