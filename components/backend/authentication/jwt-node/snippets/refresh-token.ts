// Refresh Token Flow - Access token + Refresh token pattern

import jwt from 'jsonwebtoken';

const ACCESS_SECRET = process.env.JWT_SECRET || 'access-secret';
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'refresh-secret';

interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

// 1. Generate both tokens on login
function generateTokenPair(userId: string): TokenPair {
  const accessToken = jwt.sign(
    { userId, type: 'access' },
    ACCESS_SECRET,
    { expiresIn: '15m' } // Short-lived
  );

  const refreshToken = jwt.sign(
    { userId, type: 'refresh' },
    REFRESH_SECRET,
    { expiresIn: '7d' } // Long-lived
  );

  return { accessToken, refreshToken };
}

// 2. Verify access token
function verifyAccessToken(token: string) {
  try {
    return jwt.verify(token, ACCESS_SECRET);
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      console.log('Access token expired - use refresh token');
    }
    return null;
  }
}

// 3. Verify refresh token and generate new access token
function refreshAccessToken(refreshToken: string): string | null {
  try {
    const decoded = jwt.verify(refreshToken, REFRESH_SECRET) as any;

    // Generate new access token
    const newAccessToken = jwt.sign(
      { userId: decoded.userId, type: 'access' },
      ACCESS_SECRET,
      { expiresIn: '15m' }
    );

    return newAccessToken;
  } catch (error) {
    console.error('Invalid refresh token:', error.message);
    return null;
  }
}

// 4. Complete authentication flow
async function authenticateRequest(
  accessToken: string,
  refreshToken?: string
): Promise<{ valid: boolean; newAccessToken?: string; userId?: string }> {
  // Try access token first
  const decoded = verifyAccessToken(accessToken);

  if (decoded) {
    return { valid: true, userId: (decoded as any).userId };
  }

  // Access token expired, try refresh
  if (refreshToken) {
    const newAccessToken = refreshAccessToken(refreshToken);

    if (newAccessToken) {
      const newDecoded = verifyAccessToken(newAccessToken) as any;
      return {
        valid: true,
        newAccessToken,
        userId: newDecoded.userId,
      };
    }
  }

  return { valid: false };
}

// Example usage
const userId = '12345';

// Login - generate both tokens
const tokens = generateTokenPair(userId);
console.log('Login tokens:', tokens);

// After 15 minutes, access token expires
setTimeout(() => {
  console.log('\n--- 15 minutes later ---');

  // Try to authenticate with expired access token
  const result = authenticateRequest(tokens.accessToken, tokens.refreshToken);
  result.then((auth) => {
    if (auth.valid && auth.newAccessToken) {
      console.log('Access token refreshed!');
      console.log('New access token:', auth.newAccessToken);
    }
  });
}, 100); // Simulated delay

export { generateTokenPair, verifyAccessToken, refreshAccessToken, authenticateRequest };