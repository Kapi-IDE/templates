import { Router, Request, Response } from 'express';
import {
  generateTokens,
  hashPassword,
  comparePassword,
  verifyRefreshToken,
  blacklistToken,
  extractTokenFromHeader,
} from './auth';
import { authMiddleware, rateLimitMiddleware } from './middleware';

const router = Router();

// In-memory user storage (use database in production)
interface User {
  id: string;
  email: string;
  passwordHash: string;
  role: string;
}

const users: User[] = [];

/**
 * POST /api/auth/register
 * Register a new user
 */
router.post(
  '/register',
  rateLimitMiddleware(5, 60), // 5 requests per minute
  async (req: Request, res: Response) => {
    try {
      const { email, password, role = 'user' } = req.body;

      // Validation
      if (!email || !password) {
        res.status(400).json({
          error: 'Validation error',
          message: 'Email and password are required',
        });
        return;
      }

      if (password.length < 8) {
        res.status(400).json({
          error: 'Validation error',
          message: 'Password must be at least 8 characters',
        });
        return;
      }

      // Check if user exists
      const existingUser = users.find((u) => u.email === email);
      if (existingUser) {
        res.status(409).json({
          error: 'User exists',
          message: 'A user with this email already exists',
        });
        return;
      }

      // Hash password
      const passwordHash = await hashPassword(password);

      // Create user
      const user: User = {
        id: Date.now().toString(),
        email,
        passwordHash,
        role,
      };

      users.push(user);

      // Generate tokens
      const tokens = generateTokens(user.id, {
        email: user.email,
        role: user.role,
      });

      res.status(201).json({
        message: 'User registered successfully',
        user: {
          id: user.id,
          email: user.email,
          role: user.role,
        },
        ...tokens,
      });
    } catch (error) {
      console.error('Registration error:', error);
      res.status(500).json({
        error: 'Registration failed',
        message: 'An error occurred during registration',
      });
    }
  }
);

/**
 * POST /api/auth/login
 * Login and get access/refresh tokens
 */
router.post(
  '/login',
  rateLimitMiddleware(10, 60), // 10 requests per minute
  async (req: Request, res: Response) => {
    try {
      const { email, password } = req.body;

      // Validation
      if (!email || !password) {
        res.status(400).json({
          error: 'Validation error',
          message: 'Email and password are required',
        });
        return;
      }

      // Find user
      const user = users.find((u) => u.email === email);
      if (!user) {
        res.status(401).json({
          error: 'Authentication failed',
          message: 'Invalid email or password',
        });
        return;
      }

      // Verify password
      const isValidPassword = await comparePassword(password, user.passwordHash);
      if (!isValidPassword) {
        res.status(401).json({
          error: 'Authentication failed',
          message: 'Invalid email or password',
        });
        return;
      }

      // Generate tokens
      const tokens = generateTokens(user.id, {
        email: user.email,
        role: user.role,
      });

      res.json({
        message: 'Login successful',
        user: {
          id: user.id,
          email: user.email,
          role: user.role,
        },
        ...tokens,
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({
        error: 'Login failed',
        message: 'An error occurred during login',
      });
    }
  }
);

/**
 * POST /api/auth/refresh
 * Refresh access token using refresh token
 */
router.post('/refresh', async (req: Request, res: Response) => {
  try {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      res.status(400).json({
        error: 'Validation error',
        message: 'Refresh token is required',
      });
      return;
    }

    // Verify refresh token
    const decoded = verifyRefreshToken(refreshToken);
    if (!decoded) {
      res.status(401).json({
        error: 'Authentication failed',
        message: 'Invalid or expired refresh token',
      });
      return;
    }

    // Generate new tokens
    const tokens = generateTokens(decoded.userId, {
      email: decoded.email,
      role: decoded.role,
    });

    res.json({
      message: 'Token refreshed successfully',
      ...tokens,
    });
  } catch (error) {
    console.error('Refresh error:', error);
    res.status(500).json({
      error: 'Refresh failed',
      message: 'An error occurred while refreshing token',
    });
  }
});

/**
 * POST /api/auth/logout
 * Logout and blacklist token
 */
router.post('/logout', authMiddleware, (req: Request, res: Response) => {
  try {
    const token = extractTokenFromHeader(req.headers.authorization);

    if (token) {
      blacklistToken(token);
    }

    res.json({
      message: 'Logged out successfully',
    });
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({
      error: 'Logout failed',
      message: 'An error occurred during logout',
    });
  }
});

/**
 * GET /api/auth/me
 * Get current user profile (protected route)
 */
router.get('/me', authMiddleware, (req: Request, res: Response) => {
  try {
    const user = users.find((u) => u.id === req.user?.userId);

    if (!user) {
      res.status(404).json({
        error: 'User not found',
        message: 'User no longer exists',
      });
      return;
    }

    res.json({
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
      },
    });
  } catch (error) {
    console.error('Profile error:', error);
    res.status(500).json({
      error: 'Profile fetch failed',
      message: 'An error occurred while fetching profile',
    });
  }
});

/**
 * PUT /api/auth/password
 * Change password (protected route)
 */
router.put('/password', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
      res.status(400).json({
        error: 'Validation error',
        message: 'Current and new password are required',
      });
      return;
    }

    if (newPassword.length < 8) {
      res.status(400).json({
        error: 'Validation error',
        message: 'New password must be at least 8 characters',
      });
      return;
    }

    const user = users.find((u) => u.id === req.user?.userId);
    if (!user) {
      res.status(404).json({
        error: 'User not found',
        message: 'User no longer exists',
      });
      return;
    }

    // Verify current password
    const isValid = await comparePassword(currentPassword, user.passwordHash);
    if (!isValid) {
      res.status(401).json({
        error: 'Authentication failed',
        message: 'Current password is incorrect',
      });
      return;
    }

    // Update password
    user.passwordHash = await hashPassword(newPassword);

    res.json({
      message: 'Password changed successfully',
    });
  } catch (error) {
    console.error('Password change error:', error);
    res.status(500).json({
      error: 'Password change failed',
      message: 'An error occurred while changing password',
    });
  }
});

export default router;