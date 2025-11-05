# Redis Client Utilities (Node.js)

Node.js helpers for URL caching, click counters, and IP rate limiting using the `redis` v4 client.

## Install
```bash
npm install redis
```

## Usage
```js
const { UrlCache, ClickCounter, RateLimiter } = require('./redis-client');

const cache = new UrlCache();
await cache.cacheUrl('abc123', 'https://example.com', 3600);

const counter = new ClickCounter();
const clicks = await counter.incrementClicks('abc123');

const limiter = new RateLimiter({ maxRequests: 100, windowSeconds: 60 });
const result = await limiter.checkLimit('192.168.0.1');
if (!result.allowed) {
  // return 429
}
```

Set `REDIS_URL` to point to your Redis instance (defaults to `redis://localhost:6379`).
