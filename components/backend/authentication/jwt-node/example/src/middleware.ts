import { Request, Response, NextFunction } from 'express';
import { verifyToken, extractTokenFromHeader, DecodedToken } from './auth';

// Extend Express Request type to include user
declare global {
  namespace Express {
    interface Request {
      user?: DecodedToken;
    }
  }
}

/**
 * Authentication middleware - verifies JWT and attaches user to request
 * Usage: app.get('/protected', authMiddleware, handler)
 */
export function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  try {
    // Extract token from Authorization header
    const token = extractTokenFromHeader(req.headers.authorization);

    if (!token) {
      res.status(401).json({
        error: 'Authentication required',
        message: 'No token provided',
      });
      return;
    }

    // Verify token
    const decoded = verifyToken(token);

    if (!decoded) {
      res.status(401).json({
        error: 'Authentication failed',
        message: 'Invalid or expired token',
      });
      return;
    }

    // Attach user to request
    req.user = decoded;

    next();
  } catch (error) {
    res.status(500).json({
      error: 'Authentication error',
      message: 'An error occurred during authentication',
    });
  }
}

/**
 * Optional authentication middleware - attaches user if token is valid, but doesn't require it
 * Usage: app.get('/public-or-protected', optionalAuthMiddleware, handler)
 */
export function optionalAuthMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  try {
    const token = extractTokenFromHeader(req.headers.authorization);

    if (token) {
      const decoded = verifyToken(token);
      if (decoded) {
        req.user = decoded;
      }
    }

    next();
  } catch {
    // Silently fail for optional auth
    next();
  }
}

/**
 * Role-based authorization middleware factory
 * Usage: app.delete('/admin', authMiddleware, requireRole('admin'), handler)
 */
export function requireRole(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({
        error: 'Authentication required',
        message: 'User not authenticated',
      });
      return;
    }

    const userRole = req.user.role;

    if (!userRole || !allowedRoles.includes(userRole)) {
      res.status(403).json({
        error: 'Forbidden',
        message: `Access denied. Required role: ${allowedRoles.join(' or ')}`,
      });
      return;
    }

    next();
  };
}

/**
 * Permission-based authorization middleware factory
 * Usage: app.post('/posts', authMiddleware, requirePermission('posts:create'), handler)
 */
export function requirePermission(...permissions: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({
        error: 'Authentication required',
        message: 'User not authenticated',
      });
      return;
    }

    const userPermissions = req.user.permissions as string[] | undefined;

    if (!userPermissions) {
      res.status(403).json({
        error: 'Forbidden',
        message: 'User has no permissions',
      });
      return;
    }

    const hasPermission = permissions.some((permission) =>
      userPermissions.includes(permission)
    );

    if (!hasPermission) {
      res.status(403).json({
        error: 'Forbidden',
        message: `Missing required permission: ${permissions.join(' or ')}`,
      });
      return;
    }

    next();
  };
}

/**
 * Resource ownership middleware - checks if user owns a resource
 * Usage: app.put('/posts/:id', authMiddleware, requireOwnership('Post'), handler)
 */
export function requireOwnership(resourceName: string) {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    if (!req.user) {
      res.status(401).json({
        error: 'Authentication required',
        message: 'User not authenticated',
      });
      return;
    }

    // This is a simplified example
    // In production, fetch the resource and check ownership
    const resourceId = req.params.id;
    const userId = req.user.userId;

    // Example: const resource = await db.post.findUnique({ where: { id: resourceId } });
    // if (resource.userId !== userId && req.user.role !== 'admin') { ... }

    // For this example, we just pass through
    // Implement your actual ownership check here
    console.log(`Checking ownership of ${resourceName} ${resourceId} for user ${userId}`);

    next();
  };
}

/**
 * Rate limiting middleware (simple implementation)
 * Usage: app.post('/login', rateLimitMiddleware(5, 60), handler)
 * @param maxRequests - Maximum requests allowed
 * @param windowSeconds - Time window in seconds
 */
export function rateLimitMiddleware(maxRequests: number, windowSeconds: number) {
  const requestCounts = new Map<string, { count: number; resetAt: number }>();

  return (req: Request, res: Response, next: NextFunction): void => {
    const identifier = req.ip || req.socket.remoteAddress || 'unknown';
    const now = Date.now();

    const userLimit = requestCounts.get(identifier);

    if (!userLimit || now > userLimit.resetAt) {
      // Reset window
      requestCounts.set(identifier, {
        count: 1,
        resetAt: now + windowSeconds * 1000,
      });
      next();
      return;
    }

    if (userLimit.count >= maxRequests) {
      res.status(429).json({
        error: 'Too many requests',
        message: `Rate limit exceeded. Try again in ${Math.ceil(
          (userLimit.resetAt - now) / 1000
        )} seconds`,
      });
      return;
    }

    userLimit.count++;
    next();
  };
}

/**
 * API key middleware - validates API key from header
 * Usage: app.get('/api/data', apiKeyMiddleware, handler)
 */
export function apiKeyMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const apiKey = req.headers['x-api-key'] as string;

  if (!apiKey) {
    res.status(401).json({
      error: 'API key required',
      message: 'Missing x-api-key header',
    });
    return;
  }

  // In production, verify against database
  const validApiKeys = process.env.VALID_API_KEYS?.split(',') || [];

  if (!validApiKeys.includes(apiKey)) {
    res.status(401).json({
      error: 'Invalid API key',
      message: 'The provided API key is invalid',
    });
    return;
  }

  next();
}