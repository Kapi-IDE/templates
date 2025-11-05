// Basic JWT Usage - Simple token generation and verification

import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET || 'your-secret-key';

// 1. Generate a token
function createToken(userId: string) {
  const token = jwt.sign(
    { userId, email: 'user@example.com' },
    SECRET,
    { expiresIn: '1h' }
  );
  return token;
}

// 2. Verify a token
function verifyToken(token: string) {
  try {
    const decoded = jwt.verify(token, SECRET);
    console.log('Valid token:', decoded);
    return decoded;
  } catch (error) {
    console.error('Invalid token:', error.message);
    return null;
  }
}

// 3. Decode without verification (for debugging)
function inspectToken(token: string) {
  const decoded = jwt.decode(token);
  console.log('Token contents:', decoded);
  return decoded;
}

// Example usage
const userId = '12345';
const token = createToken(userId);
console.log('Generated token:', token);

const verified = verifyToken(token);
if (verified) {
  console.log('Token is valid!');
}

// Inspect token structure
inspectToken(token);

export { createToken, verifyToken, inspectToken };