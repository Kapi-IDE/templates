/**
 * Redis Client for URL Shortener
 * Adapted from Python Redis component for Node.js
 *
 * Features:
 * - URL caching for fast redirects
 * - Click rate limiting
 * - Analytics buffering
 */

const redis = require('redis');

/**
 * Get Redis URL from environment
 */
function getRedisUrl() {
  return process.env.REDIS_URL || 'redis://localhost:6379/0';
}

/**
 * Create Redis client with production settings
 */
function createRedisClient() {
  const client = redis.createClient({
    url: getRedisUrl(),
    socket: {
      reconnectStrategy: (retries) => {
        if (retries > 10) {
          return new Error('Max retries reached');
        }
        return Math.min(retries * 100, 3000);
      },
      connectTimeout: 5000,
      keepAlive: 30000,
    },
  });

  client.on('error', (err) => {
    console.error('Redis Client Error:', err);
  });

  client.on('connect', () => {
    console.log('Redis client connected');
  });

  return client;
}

// Global Redis client
let redisClient = null;

/**
 * Get or create Redis client singleton
 */
async function getRedisClient() {
  if (!redisClient) {
    redisClient = createRedisClient();
    await redisClient.connect();
  }
  return redisClient;
}

/**
 * Check Redis health
 */
async function redisHealthCheck() {
  try {
    const client = await getRedisClient();
    const result = await client.ping();
    return result === 'PONG';
  } catch (error) {
    return false;
  }
}

/**
 * URL Cache for fast redirects
 */
class UrlCache {
  constructor(client = null, keyPrefix = 'url:') {
    this.client = client;
    this.keyPrefix = keyPrefix;
    this.defaultTtl = 3600; // 1 hour
  }

  async _getClient() {
    if (!this.client) {
      this.client = await getRedisClient();
    }
    return this.client;
  }

  _getKey(shortCode) {
    return `${this.keyPrefix}${shortCode}`;
  }

  /**
   * Cache URL mapping
   * @param {string} shortCode - Short code
   * @param {string} originalUrl - Original URL
   * @param {number} ttl - Time to live in seconds
   */
  async cacheUrl(shortCode, originalUrl, ttl = null) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);
    const expiry = ttl || this.defaultTtl;

    await client.setEx(key, expiry, originalUrl);
    return true;
  }

  /**
   * Get cached URL
   * @param {string} shortCode - Short code
   * @returns {string|null} Original URL or null
   */
  async getUrl(shortCode) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);

    try {
      const url = await client.get(key);
      return url;
    } catch (error) {
      console.error('Redis get error:', error);
      return null;
    }
  }

  /**
   * Delete cached URL
   * @param {string} shortCode - Short code
   */
  async deleteUrl(shortCode) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);

    const result = await client.del(key);
    return result > 0;
  }

  /**
   * Check if URL is cached
   * @param {string} shortCode - Short code
   */
  async exists(shortCode) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);

    const result = await client.exists(key);
    return result > 0;
  }
}

/**
 * Click Counter with atomic increments
 */
class ClickCounter {
  constructor(client = null, keyPrefix = 'clicks:') {
    this.client = client;
    this.keyPrefix = keyPrefix;
  }

  async _getClient() {
    if (!this.client) {
      this.client = await getRedisClient();
    }
    return this.client;
  }

  _getKey(shortCode) {
    return `${this.keyPrefix}${shortCode}`;
  }

  /**
   * Increment click count atomically
   * @param {string} shortCode - Short code
   * @returns {number} New click count
   */
  async incrementClicks(shortCode) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);

    const newCount = await client.incr(key);

    // Set expiration on first increment
    if (newCount === 1) {
      await client.expire(key, 86400 * 30); // 30 days
    }

    return newCount;
  }

  /**
   * Get click count
   * @param {string} shortCode - Short code
   * @returns {number} Click count
   */
  async getClicks(shortCode) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);

    const count = await client.get(key);
    return count ? parseInt(count, 10) : 0;
  }

  /**
   * Reset click count
   * @param {string} shortCode - Short code
   */
  async resetClicks(shortCode) {
    const client = await this._getClient();
    const key = this._getKey(shortCode);

    await client.del(key);
    return true;
  }
}

/**
 * Rate Limiter for preventing abuse
 */
class RateLimiter {
  constructor(client = null, keyPrefix = 'ratelimit:') {
    this.client = client;
    this.keyPrefix = keyPrefix;
    this.maxRequests = 100; // Max requests per window
    this.windowSeconds = 3600; // 1 hour window
  }

  async _getClient() {
    if (!this.client) {
      this.client = await getRedisClient();
    }
    return this.client;
  }

  _getKey(identifier) {
    return `${this.keyPrefix}${identifier}`;
  }

  /**
   * Check if request is allowed
   * @param {string} identifier - IP address or user ID
   * @returns {Object} { allowed: boolean, remaining: number, resetAt: number }
   */
  async checkLimit(identifier) {
    const client = await this._getClient();
    const key = this._getKey(identifier);

    const count = await client.incr(key);

    if (count === 1) {
      await client.expire(key, this.windowSeconds);
    }

    const ttl = await client.ttl(key);
    const resetAt = Date.now() + (ttl * 1000);

    return {
      allowed: count <= this.maxRequests,
      remaining: Math.max(0, this.maxRequests - count),
      resetAt,
      current: count,
    };
  }
}

module.exports = {
  createRedisClient,
  getRedisClient,
  redisHealthCheck,
  UrlCache,
  ClickCounter,
  RateLimiter,
};
