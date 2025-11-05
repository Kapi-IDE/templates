import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

// Environment configuration
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-me-in-production';
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'your-refresh-secret-change-me';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '15m';
const JWT_REFRESH_EXPIRES_IN = process.env.JWT_REFRESH_EXPIRES_IN || '7d';
const BCRYPT_ROUNDS = parseInt(process.env.BCRYPT_ROUNDS || '10');

// In-memory token blacklist (use Redis in production)
const tokenBlacklist = new Set<string>();

// Types
export interface TokenPayload {
  userId: string;
  email?: string;
  role?: string;
  [key: string]: any;
}

export interface DecodedToken extends TokenPayload {
  iat: number;
  exp: number;
}

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

/**
 * Generate access and refresh tokens for a user
 * @param userId - User ID to encode in token
 * @param additionalPayload - Additional data to include in token
 * @returns Object with accessToken and refreshToken
 */
export function generateTokens(
  userId: string,
  additionalPayload: Omit<TokenPayload, 'userId'> = {}
): TokenPair {
  const payload: TokenPayload = {
    userId,
    ...additionalPayload,
  };

  const accessToken = jwt.sign(payload, JWT_SECRET, {
    expiresIn: JWT_EXPIRES_IN,
    algorithm: 'HS256',
  });

  const refreshToken = jwt.sign(payload, JWT_REFRESH_SECRET, {
    expiresIn: JWT_REFRESH_EXPIRES_IN,
    algorithm: 'HS256',
  });

  return { accessToken, refreshToken };
}

/**
 * Verify and decode an access token
 * @param token - JWT access token
 * @returns Decoded token payload or null if invalid
 */
export function verifyToken(token: string): DecodedToken | null {
  try {
    // Check if token is blacklisted
    if (tokenBlacklist.has(token)) {
      return null;
    }

    const decoded = jwt.verify(token, JWT_SECRET, {
      algorithms: ['HS256'],
    }) as DecodedToken;

    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      console.warn('Token expired:', error.message);
    } else if (error instanceof jwt.JsonWebTokenError) {
      console.warn('Invalid token:', error.message);
    }
    return null;
  }
}

/**
 * Verify and decode a refresh token
 * @param token - JWT refresh token
 * @returns Decoded token payload or null if invalid
 */
export function verifyRefreshToken(token: string): DecodedToken | null {
  try {
    // Check if token is blacklisted
    if (tokenBlacklist.has(token)) {
      return null;
    }

    const decoded = jwt.verify(token, JWT_REFRESH_SECRET, {
      algorithms: ['HS256'],
    }) as DecodedToken;

    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      console.warn('Refresh token expired:', error.message);
    } else if (error instanceof jwt.JsonWebTokenError) {
      console.warn('Invalid refresh token:', error.message);
    }
    return null;
  }
}

/**
 * Hash a password using bcrypt
 * @param password - Plain text password
 * @returns Hashed password
 */
export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, BCRYPT_ROUNDS);
}

/**
 * Compare a password with a hash
 * @param password - Plain text password
 * @param hash - Hashed password
 * @returns True if password matches hash
 */
export async function comparePassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

/**
 * Add a token to the blacklist (for logout)
 * @param token - Token to blacklist
 */
export function blacklistToken(token: string): void {
  tokenBlacklist.add(token);

  // Auto-cleanup after token expiry
  // In production, use Redis with TTL
  const decoded = jwt.decode(token) as DecodedToken;
  if (decoded?.exp) {
    const expiryMs = decoded.exp * 1000 - Date.now();
    if (expiryMs > 0) {
      setTimeout(() => {
        tokenBlacklist.delete(token);
      }, expiryMs);
    }
  }
}

/**
 * Check if a token is blacklisted
 * @param token - Token to check
 * @returns True if token is blacklisted
 */
export function isTokenBlacklisted(token: string): boolean {
  return tokenBlacklist.has(token);
}

/**
 * Extract token from Authorization header
 * @param authHeader - Authorization header value
 * @returns Token or null
 */
export function extractTokenFromHeader(authHeader?: string): string | null {
  if (!authHeader) {
    return null;
  }

  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return null;
  }

  return parts[1];
}

/**
 * Generate a random token (for password reset, email verification, etc.)
 * @param length - Token length (default 32)
 * @returns Random token string
 */
export function generateRandomToken(length: number = 32): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let token = '';
  for (let i = 0; i < length; i++) {
    token += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return token;
}

/**
 * Decode a token without verifying (use for inspecting expired tokens)
 * @param token - JWT token
 * @returns Decoded payload or null
 */
export function decodeToken(token: string): DecodedToken | null {
  try {
    return jwt.decode(token) as DecodedToken;
  } catch {
    return null;
  }
}

// Export configuration for testing
export const config = {
  JWT_SECRET,
  JWT_REFRESH_SECRET,
  JWT_EXPIRES_IN,
  JWT_REFRESH_EXPIRES_IN,
  BCRYPT_ROUNDS,
};