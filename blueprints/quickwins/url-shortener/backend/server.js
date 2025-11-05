/**
 * URL Shortener Express Server
 *
 * Features:
 * - Create short URLs with custom slugs
 * - Fast Redis-cached redirects
 * - Click tracking and analytics
 * - QR code generation
 * - URL expiration
 * - Rate limiting
 */

const express = require('express');
const { PrismaClient } = require('@prisma/client');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { customAlphabet } = require('nanoid');
const QRCode = require('qrcode');
const { UrlCache, ClickCounter, RateLimiter } = require('./redis-client');

// Initialize
const app = express();
const prisma = new PrismaClient();
const urlCache = new UrlCache();
const clickCounter = new ClickCounter();
const rateLimiter = new RateLimiter();

// Short code generator (URL-safe characters)
const generateShortCode = customAlphabet(
  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
  7 // 7 characters = 62^7 = 3.5 trillion combinations
);

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan('combined'));

// Get client IP helper
function getClientIp(req) {
  return (
    req.headers['x-forwarded-for']?.split(',')[0] ||
    req.headers['x-real-ip'] ||
    req.socket.remoteAddress
  );
}

// ============================================================================
// ROUTES
// ============================================================================

/**
 * Health check
 * GET /health
 */
app.get('/health', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    const redisHealthy = await urlCache.exists('health_check_test');

    res.json({
      status: 'healthy',
      database: 'connected',
      redis: redisHealthy ? 'connected' : 'degraded',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
    });
  }
});

/**
 * Create short URL
 * POST /api/shorten
 *
 * Body: {
 *   url: "https://example.com/very/long/url",
 *   customSlug?: "my-link",
 *   expiresInDays?: 30
 * }
 */
app.post('/api/shorten', async (req, res) => {
  try {
    const { url, customSlug, expiresInDays } = req.body;
    const clientIp = getClientIp(req);

    // Validate URL
    if (!url || !url.match(/^https?:\/\/.+/)) {
      return res.status(400).json({ error: 'Invalid URL' });
    }

    // Rate limiting
    const rateLimit = await rateLimiter.checkLimit(clientIp);
    if (!rateLimit.allowed) {
      return res.status(429).json({
        error: 'Rate limit exceeded',
        resetAt: rateLimit.resetAt,
      });
    }

    // Generate or validate custom slug
    let shortCode;
    if (customSlug) {
      // Validate custom slug (alphanumeric, hyphens, underscores only)
      if (!/^[a-zA-Z0-9_-]+$/.test(customSlug)) {
        return res.status(400).json({
          error: 'Custom slug must contain only letters, numbers, hyphens, and underscores',
        });
      }

      // Check if custom slug is available
      const existing = await prisma.url.findUnique({
        where: { shortCode: customSlug },
      });

      if (existing) {
        return res.status(409).json({
          error: 'Custom slug already taken',
        });
      }

      shortCode = customSlug;
    } else {
      // Generate unique short code
      shortCode = generateShortCode();

      // Ensure uniqueness (very unlikely to collide)
      while (await prisma.url.findUnique({ where: { shortCode } })) {
        shortCode = generateShortCode();
      }
    }

    // Calculate expiration
    let expiresAt = null;
    if (expiresInDays && expiresInDays > 0) {
      expiresAt = new Date();
      expiresAt.setDate(expiresAt.getDate() + expiresInDays);
    }

    // Create URL record
    const urlRecord = await prisma.url.create({
      data: {
        originalUrl: url,
        shortCode,
        customSlug: !!customSlug,
        expiresAt,
        createdBy: clientIp,
      },
    });

    // Cache in Redis for fast redirects
    const cacheTtl = expiresInDays
      ? Math.min(expiresInDays * 86400, 86400)
      : 3600;
    await urlCache.cacheUrl(shortCode, url, cacheTtl);

    // Build short URL
    const baseUrl = process.env.BASE_URL || `http://localhost:${process.env.PORT || 3000}`;
    const shortUrl = `${baseUrl}/${shortCode}`;

    res.status(201).json({
      shortUrl,
      shortCode,
      originalUrl: url,
      expiresAt: expiresAt?.toISOString() || null,
      createdAt: urlRecord.createdAt.toISOString(),
    });
  } catch (error) {
    console.error('Error creating short URL:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * Get URL statistics
 * GET /api/stats/:shortCode
 */
app.get('/api/stats/:shortCode', async (req, res) => {
  try {
    const { shortCode } = req.params;

    const urlRecord = await prisma.url.findUnique({
      where: { shortCode },
      include: {
        analytics: {
          orderBy: { createdAt: 'desc' },
          take: 100,
        },
      },
    });

    if (!urlRecord) {
      return res.status(404).json({ error: 'Short URL not found' });
    }

    // Get Redis click count (may be ahead of DB)
    const redisClicks = await clickCounter.getClicks(shortCode);

    // Aggregate analytics
    const analyticsData = urlRecord.analytics;
    const browserStats = {};
    const countryStats = {};
    const referrerStats = {};

    analyticsData.forEach((entry) => {
      if (entry.browser) {
        browserStats[entry.browser] = (browserStats[entry.browser] || 0) + 1;
      }
      if (entry.country) {
        countryStats[entry.country] = (countryStats[entry.country] || 0) + 1;
      }
      if (entry.referrer) {
        const domain = entry.referrer.match(/https?:\/\/([^\/]+)/)?.[1] || 'direct';
        referrerStats[domain] = (referrerStats[domain] || 0) + 1;
      }
    });

    res.json({
      shortCode,
      originalUrl: urlRecord.originalUrl,
      clicks: Math.max(urlRecord.clicks, redisClicks),
      createdAt: urlRecord.createdAt,
      expiresAt: urlRecord.expiresAt,
      isActive: urlRecord.isActive,
      analytics: {
        total: analyticsData.length,
        browsers: browserStats,
        countries: countryStats,
        referrers: referrerStats,
      },
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * Generate QR code
 * GET /api/qr/:shortCode
 */
app.get('/api/qr/:shortCode', async (req, res) => {
  try {
    const { shortCode } = req.params;

    const urlRecord = await prisma.url.findUnique({
      where: { shortCode },
    });

    if (!urlRecord || !urlRecord.isActive) {
      return res.status(404).json({ error: 'Short URL not found' });
    }

    // Build short URL
    const baseUrl = process.env.BASE_URL || `http://localhost:${process.env.PORT || 3000}`;
    const shortUrl = `${baseUrl}/${shortCode}`;

    // Generate QR code
    const qrDataUrl = await QRCode.toDataURL(shortUrl, {
      width: 300,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF',
      },
    });

    res.json({
      shortCode,
      shortUrl,
      qrCode: qrDataUrl,
    });
  } catch (error) {
    console.error('Error generating QR code:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * Redirect short URL
 * GET /:shortCode
 */
app.get('/:shortCode', async (req, res) => {
  try {
    const { shortCode } = req.params;
    const clientIp = getClientIp(req);

    // Try cache first
    let originalUrl = await urlCache.getUrl(shortCode);

    if (!originalUrl) {
      // Cache miss - fetch from database
      const urlRecord = await prisma.url.findUnique({
        where: { shortCode },
      });

      if (!urlRecord || !urlRecord.isActive) {
        return res.status(404).send('Short URL not found or expired');
      }

      // Check expiration
      if (urlRecord.expiresAt && new Date() > urlRecord.expiresAt) {
        await prisma.url.update({
          where: { id: urlRecord.id },
          data: { isActive: false },
        });
        return res.status(410).send('Short URL has expired');
      }

      originalUrl = urlRecord.originalUrl;

      // Re-cache
      await urlCache.cacheUrl(shortCode, originalUrl);
    }

    // Track click asynchronously (don't block redirect)
    const userAgent = req.headers['user-agent'] || '';
    const referrer = req.headers['referer'] || req.headers['referrer'] || null;

    // Increment Redis counter immediately
    clickCounter.incrementClicks(shortCode).catch((err) => {
      console.error('Error incrementing click counter:', err);
    });

    // Store detailed analytics in background
    setImmediate(async () => {
      try {
        // Parse user agent
        const browser = userAgent.match(/(Chrome|Firefox|Safari|Edge|Opera)/i)?.[1] || 'Unknown';
        const os = userAgent.match(/(Windows|Mac|Linux|Android|iOS)/i)?.[1] || 'Unknown';
        const device = userAgent.match(/Mobile/i) ? 'Mobile' : 'Desktop';

        await prisma.analytics.create({
          data: {
            urlId: (await prisma.url.findUnique({ where: { shortCode } })).id,
            userAgent,
            browser,
            os,
            device,
            ipAddress: clientIp,
            referrer,
          },
        });

        // Update database click count periodically
        await prisma.url.update({
          where: { shortCode },
          data: { clicks: { increment: 1 } },
        });
      } catch (err) {
        console.error('Error storing analytics:', err);
      }
    });

    // Redirect
    res.redirect(301, originalUrl);
  } catch (error) {
    console.error('Error redirecting:', error);
    res.status(500).send('Internal server error');
  }
});

// ============================================================================
// SERVER
// ============================================================================

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 URL Shortener running on port ${PORT}`);
  console.log(`📊 Base URL: ${process.env.BASE_URL || `http://localhost:${PORT}`}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully');
  await prisma.$disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT received, shutting down gracefully');
  await prisma.$disconnect();
  process.exit(0);
});

module.exports = app;
