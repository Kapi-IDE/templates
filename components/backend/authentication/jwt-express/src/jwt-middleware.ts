import { RequestHandler } from 'express';
import jwt, { JwtPayload, VerifyErrors } from 'jsonwebtoken';

export type JWTOptions = {
  secret: string;
};

export interface AuthenticatedRequestPayload extends JwtPayload {
  data?: unknown;
}

export interface RequestUser {
  [key: string]: unknown;
}

declare module 'express-serve-static-core' {
  interface Request {
    user?: RequestUser;
  }
}

export function jwtVerifierMiddleware(options: JWTOptions): RequestHandler {
  return function verifyToken(req, res, next) {
    const authHeader = (req.headers['authorization'] ?? req.headers['Authorization']) as string | undefined;

    if (!authHeader) {
      res.sendStatus(401);
      return;
    }

    const parts = authHeader.split(' ');
    if (parts.length > 2) {
      res.sendStatus(401);
      return;
    }

    const token = parts.length === 2 ? parts[1] : parts[0];

    jwt.verify(token, options.secret, (err: VerifyErrors | null, decoded: AuthenticatedRequestPayload | undefined) => {
      if (err || !decoded) {
        res.sendStatus(401);
        return;
      }

      // Practica convention stores data in payload.data
      req.user = (decoded.data as RequestUser) ?? decoded;
      next();
    });
  };
}
