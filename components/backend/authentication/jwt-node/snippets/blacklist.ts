// Token Blacklisting - Logout and invalidation patterns

import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET || 'your-secret';

// In-memory blacklist (use Redis in production)
const blacklist = new Set<string>();

// For production: Use Redis with TTL
/*
import { Redis } from 'ioredis';
const redis = new Redis();

async function blacklistToken(token: string) {
  const decoded = jwt.decode(token) as any;
  const ttl = decoded.exp - Math.floor(Date.now() / 1000);
  await redis.setex(`blacklist:${token}`, ttl, '1');
}

async function isBlacklisted(token: string): Promise<boolean> {
  const result = await redis.get(`blacklist:${token}`);
  return result === '1';
}
*/

// 1. Blacklist a token (logout)
function blacklistToken(token: string): void {
  blacklist.add(token);

  // Auto-cleanup after expiry
  const decoded = jwt.decode(token) as any;
  if (decoded?.exp) {
    const ttlMs = decoded.exp * 1000 - Date.now();
    if (ttlMs > 0) {
      setTimeout(() => {
        blacklist.delete(token);
        console.log('Token removed from blacklist after expiry');
      }, ttlMs);
    }
  }
}

// 2. Check if token is blacklisted
function isBlacklisted(token: string): boolean {
  return blacklist.has(token);
}

// 3. Verify token with blacklist check
function verifyToken(token: string) {
  // Check blacklist first
  if (isBlacklisted(token)) {
    console.log('Token is blacklisted');
    return null;
  }

  try {
    const decoded = jwt.verify(token, SECRET);
    return decoded;
  } catch (error) {
    console.error('Invalid token:', error.message);
    return null;
  }
}

// 4. Logout and blacklist token
function logout(token: string): void {
  blacklistToken(token);
  console.log('User logged out, token blacklisted');
}

// 5. Blacklist all tokens for a user (force logout all sessions)
const userTokens = new Map<string, Set<string>>(); // userId -> tokens

function registerToken(userId: string, token: string): void {
  if (!userTokens.has(userId)) {
    userTokens.set(userId, new Set());
  }
  userTokens.get(userId)!.add(token);
}

function logoutAllSessions(userId: string): void {
  const tokens = userTokens.get(userId);
  if (tokens) {
    tokens.forEach((token) => blacklistToken(token));
    userTokens.delete(userId);
    console.log(`All sessions logged out for user ${userId}`);
  }
}

// 6. Middleware pattern
function authMiddleware(token: string | undefined): boolean {
  if (!token) {
    console.log('No token provided');
    return false;
  }

  if (isBlacklisted(token)) {
    console.log('Token is blacklisted (user logged out)');
    return false;
  }

  const decoded = verifyToken(token);
  if (!decoded) {
    console.log('Invalid or expired token');
    return false;
  }

  console.log('Token is valid:', decoded);
  return true;
}

// Example usage
const userId = '12345';

// Generate token
const token = jwt.sign({ userId }, SECRET, { expiresIn: '1h' });
console.log('Generated token');

// Register token for user
registerToken(userId, token);

// Verify token
console.log('Token valid:', authMiddleware(token));

// Logout
logout(token);

// Try to use token after logout
console.log('Token valid after logout:', authMiddleware(token)); // false

// Example: logout all sessions
const token2 = jwt.sign({ userId }, SECRET, { expiresIn: '1h' });
const token3 = jwt.sign({ userId }, SECRET, { expiresIn: '1h' });
registerToken(userId, token2);
registerToken(userId, token3);

logoutAllSessions(userId);

export {
  blacklistToken,
  isBlacklisted,
  verifyToken,
  logout,
  logoutAllSessions,
  registerToken,
  authMiddleware,
};