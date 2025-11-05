import { FastifyPluginCallback, FastifyRequest } from 'fastify';
import fastifyPlugin from 'fastify-plugin';
import jwt from 'jsonwebtoken';

export type JWTOptions = {
  secret: string;
};

export type AuthenticatedUser = {
  [key: string]: unknown;
};

const JWTVerifierPlugin: FastifyPluginCallback<JWTOptions> = (app, options, done) => {
  app.decorateRequest('user', null);

  app.addHook('onRequest', async (request, reply) => {
    const result = verifyToken(request, options.secret);
    if (!result.success) {
      reply.status(401).send();
      return;
    }

    request.user = result.user;
  });

  done();
};

type VerificationResult =
  | { success: false }
  | { success: true; user: AuthenticatedUser };

function verifyToken(request: FastifyRequest, secret: string): VerificationResult {
  const header = getAuthorizationHeader(request);
  if (!header) return { success: false };

  const parts = header.split(' ');
  if (parts.length > 2) return { success: false };
  const token = parts.length === 2 ? parts[1] : parts[0];

  try {
    const decoded = jwt.verify(token, secret);
    if (typeof decoded !== 'object' || decoded === null) {
      return { success: false };
    }

    const payload = (decoded as jwt.JwtPayload).data ?? decoded;
    if (typeof payload !== 'object' || payload === null) {
      return { success: false };
    }

    return { success: true, user: payload as AuthenticatedUser };
  } catch (error) {
    return { success: false };
  }
}

function getAuthorizationHeader(request: FastifyRequest): string | undefined {
  const header = request.headers['authorization'] ?? (request.headers as any)['Authorization'];
  if (Array.isArray(header)) {
    return header[0];
  }
  return header;
}

declare module 'fastify' {
  interface FastifyRequest {
    user: AuthenticatedUser | null;
  }
}

export const JWTVerifier = fastifyPlugin(JWTVerifierPlugin, {
  name: 'jwt-verifier',
});
