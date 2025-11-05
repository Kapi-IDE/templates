# URL Shortener

Production-ready URL shortener with Redis caching, analytics, QR codes, and custom slugs.

**Gateway App #1** - First quickwin application built with KAPI methodology.

## ✨ Features

- **Custom Short URLs**: Create memorable short links with custom slugs
- **QR Code Generation**: Automatic QR codes for sharing
- **Click Analytics**: Track clicks with browser, country, device, and referrer data
- **Redis Caching**: Lightning-fast redirects with Redis
- **URL Expiration**: Set expiration dates for temporary links
- **Rate Limiting**: Prevent abuse with intelligent rate limiting
- **Production Ready**: Docker, health checks, graceful shutdown

## 🚀 Quick Start (10 minutes)

### Prerequisites
- Node.js 18+
- Docker & Docker Compose (recommended)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone/copy this directory
cd url-shortener

# 2. Copy environment variables
cp .env.example .env

# 3. Configure environment (IMPORTANT)
# Edit .env file - NO API KEYS NEEDED for basic setup
# Database and Redis are pre-configured in docker-compose.yml
# Optional: Set BASE_URL if deploying to production domain

# 4. Start services (PostgreSQL + Redis)
docker-compose up -d postgres redis

# 5. Install dependencies
npm install

# 6. Setup database
npm run db:push

# 7. Start development server
npm run dev
```

Server runs at http://localhost:3000

### Option 2: Manual Setup

```bash
# 1. Install dependencies
npm install

# 2. Setup PostgreSQL and Redis
# PostgreSQL: brew install postgresql
# Redis: brew install redis

# 3. Configure environment (IMPORTANT)
cp .env.example .env

# EDIT .env FILE:
# - DATABASE_URL: Your PostgreSQL connection string
#   Example: postgresql://user:password@localhost:5432/url_shortener
# - REDIS_URL: Your Redis connection string
#   Example: redis://localhost:6379/0
# - BASE_URL: Your public domain (production) or http://localhost:3000 (dev)
# - PORT: Server port (default: 3000)
#
# ⚠️ IMPORTANT: Never commit .env to git - it's in .gitignore
# ⚠️ NO EXTERNAL API KEYS NEEDED - this app is self-contained

# 4. Setup database
npm run db:push

# 5. Start services
brew services start postgresql
brew services start redis

# 6. Start server
npm run dev
```

## 📖 API Documentation

### Create Short URL

```bash
POST /api/shorten
Content-Type: application/json

{
  "url": "https://example.com/very/long/url",
  "customSlug": "my-link",  // optional
  "expiresInDays": 30       // optional
}
```

**Response:**
```json
{
  "shortUrl": "http://localhost:3000/abc123",
  "shortCode": "abc123",
  "originalUrl": "https://example.com/very/long/url",
  "expiresAt": "2025-11-01T12:00:00.000Z",
  "createdAt": "2025-10-02T12:00:00.000Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:3000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/anthropics/claude-code"}'
```

### Redirect

```bash
GET /:shortCode
```

Redirects to original URL and tracks analytics.

**Example:**
```bash
curl -L http://localhost:3000/abc123
# Redirects to original URL
```

### Get Statistics

```bash
GET /api/stats/:shortCode
```

**Response:**
```json
{
  "shortCode": "abc123",
  "originalUrl": "https://example.com",
  "clicks": 42,
  "createdAt": "2025-10-02T12:00:00.000Z",
  "expiresAt": null,
  "isActive": true,
  "analytics": {
    "total": 42,
    "browsers": {
      "Chrome": 30,
      "Firefox": 8,
      "Safari": 4
    },
    "countries": {
      "United States": 25,
      "Canada": 10,
      "UK": 7
    },
    "referrers": {
      "twitter.com": 15,
      "facebook.com": 10,
      "direct": 17
    }
  }
}
```

**Example:**
```bash
curl http://localhost:3000/api/stats/abc123
```

### Generate QR Code

```bash
GET /api/qr/:shortCode
```

**Response:**
```json
{
  "shortCode": "abc123",
  "shortUrl": "http://localhost:3000/abc123",
  "qrCode": "data:image/png;base64,iVBORw0KG..."
}
```

**Example:**
```bash
curl http://localhost:3000/api/qr/abc123
```

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2025-10-02T12:00:00.000Z"
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Request                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Express Server                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Helmet     │  │   CORS       │  │   Rate Limiter   │  │
│  │   Security   │  │              │  │   (Redis)        │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  PostgreSQL  │  │    Redis     │  │  QR Code     │
    │  (Prisma)    │  │   Cache      │  │  Generator   │
    │              │  │              │  │              │
    │ • URLs       │  │ • URL Cache  │  │ • PNG/SVG    │
    │ • Analytics  │  │ • Counters   │  │ • Data URLs  │
    └──────────────┘  └──────────────┘  └──────────────┘
```

### Data Flow

1. **Create Short URL**: Client → Express → Validate → Prisma (DB) → Redis (cache) → Response
2. **Redirect**: Client → Express → Redis (cache hit) → Redirect → Analytics (async)
3. **Analytics**: Background job → Parse UA → GeoIP → Prisma (analytics table)

### Component Sources

- **Prisma Schema**: Adapted from `components/database/prisma-patterns/01-basic-blog.prisma`
- **Redis Client**: Adapted from `components/backend/caching/redis/client.py` (ported to Node.js)
- **Express Patterns**: Following Node.js best practices from `quality-baselines/nodejs-best-practices-pattern.md`

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `DATABASE_URL` | - | PostgreSQL connection string | ✅ Yes |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string | ✅ Yes |
| `PORT` | `3000` | Server port | Optional |
| `BASE_URL` | `http://localhost:3000` | Base URL for short links | Optional |
| `NODE_ENV` | `development` | Environment (development/production) | Optional |

### 🔐 Security Best Practices

**Setting Up Environment Variables:**

1. **Never commit `.env` file to git** (already in `.gitignore`)
2. **Use strong database passwords in production**
3. **For production deployments:**
   ```bash
   # Set environment variables via your hosting platform
   # Vercel: Settings → Environment Variables
   # Heroku: heroku config:set DATABASE_URL=...
   # Railway: Settings → Variables
   # Docker: Pass via docker run -e or docker-compose environment
   ```

4. **Database URL Format:**
   ```
   postgresql://username:password@host:port/database

   Example (local):
   postgresql://postgres:mypassword@localhost:5432/url_shortener

   Example (production):
   postgresql://user:complex_password_123@db.example.com:5432/shortener_prod
   ```

5. **Redis URL Format:**
   ```
   redis://[:password@]host:port/database

   Example (no password):
   redis://localhost:6379/0

   Example (with password):
   redis://:your_redis_password@redis-host:6379/0
   ```

**⚠️ IMPORTANT: This blueprint requires NO external API keys**
- No OpenAI, Anthropic, or other AI service keys needed
- No payment processor keys (Stripe, etc.)
- No cloud service credentials (AWS, GCP, etc.)
- Self-contained with PostgreSQL + Redis only

### Redis Configuration

Configured in `backend/redis-client.js`:
- **URL Cache TTL**: 1 hour (configurable)
- **Click Counter TTL**: 30 days
- **Rate Limit**: 100 requests/hour per IP

### Database Schema

See `database/schema.prisma` for full schema.

**Models:**
- `Url`: Short URL records with metadata
- `Analytics`: Click tracking with user agent, geo, referrer

## 📊 Performance

- **Redirect Speed**: <10ms (Redis cached)
- **DB Fallback**: <50ms (PostgreSQL)
- **QR Generation**: <100ms
- **Capacity**: 3.5 trillion unique short codes (62^7)

## 🛡️ Security

- **Helmet.js**: Security headers
- **Rate Limiting**: IP-based throttling
- **Input Validation**: URL and slug sanitization
- **CORS**: Configurable origins
- **No Secrets in Code**: All credentials via environment variables

## 🧪 Testing

```bash
# Run tests
npm test

# Test health endpoint
curl http://localhost:3000/health

# Test URL creation
curl -X POST http://localhost:3000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## 🚢 Production Deployment

### Docker Production Build

```bash
# Build image
docker build -t url-shortener:latest .

# Run with environment variables
docker run -p 3000:3000 \
  -e DATABASE_URL="postgresql://..." \
  -e REDIS_URL="redis://..." \
  -e BASE_URL="https://yourdomain.com" \
  url-shortener:latest
```

### Full Stack Deployment

```bash
# Start all services (PostgreSQL, Redis, App)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Environment Checklist

- [ ] Set `DATABASE_URL` to production PostgreSQL
- [ ] Set `REDIS_URL` to production Redis
- [ ] Set `BASE_URL` to public domain
- [ ] Set `NODE_ENV=production`
- [ ] Run database migrations: `npm run db:migrate`
- [ ] Configure HTTPS/SSL
- [ ] Setup monitoring and alerts

## 📈 Scaling

### Horizontal Scaling

- **Stateless Design**: Multiple instances can run behind load balancer
- **Redis Shared State**: All instances share Redis cache and counters
- **Database Pooling**: Prisma connection pooling built-in

### Redis Optimization

```javascript
// Increase cache TTL for popular URLs
await urlCache.cacheUrl(shortCode, url, 86400); // 24 hours
```

### Database Optimization

- Indexed on `shortCode`, `createdAt`, `isActive`
- Analytics partitioned by date (future enhancement)
- Click counter sync interval tunable

## 🐛 Troubleshooting

### Redis Connection Issues

```bash
# Check Redis is running
docker-compose ps redis

# Test connection
redis-cli ping
```

### Database Issues

```bash
# Reset database
npm run db:push

# View database in Prisma Studio
npm run db:studio
```

### Port Already in Use

```bash
# Change port in .env
PORT=3001
```

## 📝 Development

### Project Structure

```
url-shortener/
├── backend/
│   ├── server.js          # Express app and routes
│   └── redis-client.js    # Redis utilities
├── database/
│   └── schema.prisma      # Database schema
├── docker-compose.yml     # Docker services
├── Dockerfile             # Production image
├── package.json           # Dependencies
└── README.md              # This file
```

### Adding Features

1. **Custom Domains**: Add `domain` field to Url model
2. **Link Preview**: Add OpenGraph metadata scraping
3. **A/B Testing**: Add variant tracking to Analytics
4. **Bulk Import**: Add CSV upload endpoint
5. **API Keys**: Add authentication for API access

## 🎯 KAPI Methodology

This blueprint follows **Backwards Build** methodology:

1. ✅ **Specification**: Feature requirements defined (10-min setup, Redis caching, analytics)
2. ✅ **Architecture**: Component selection (Prisma, Redis, Express, QR codes)
3. ✅ **Database Schema**: Data model designed before implementation
4. ✅ **Implementation**: Code built following architecture
5. ✅ **Quality Gates**: Security, error handling, Docker, README

**Token Savings**: ~80% compared to building from scratch with AI prompts.

## 📚 Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Redis Node.js Guide](https://redis.io/docs/clients/nodejs/)
- [Express Best Practices](https://expressjs.com/en/advanced/best-practice-performance.html)
- [QRCode.js Documentation](https://www.npmjs.com/package/qrcode)

## 📄 License

MIT License - Free for commercial and personal use

---

**Built with KAPI** - Stop vibe coding. Start engineering.
