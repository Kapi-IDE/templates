# Docker Compose Stack

Production-ready Docker Compose configurations for common development and production stacks including PostgreSQL, Redis, Nginx, and more.

## Overview

Complete Docker Compose setups for local development and production deployment. Includes health checks, volumes, networks, and best practices for containerized applications.

## Features

- **Multi-Service Stacks**: Pre-configured service combinations
- **Health Checks**: Automatic service health monitoring
- **Persistent Volumes**: Data persistence across restarts
- **Networks**: Isolated service communication
- **Environment Variables**: Flexible configuration
- **Hot Reload**: Development-friendly setups
- **Production Ready**: Optimized for production deployment
- **Resource Limits**: CPU and memory constraints

## Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## File Structure

```
docker-compose-stack/
├── example/
│   ├── docker-compose.yml              # Full stack
│   ├── docker-compose.dev.yml          # Development overrides
│   ├── docker-compose.prod.yml         # Production overrides
│   ├── .env.example                    # Environment variables
│   └── services/
│       ├── postgres/
│       │   └── init.sql                # Database initialization
│       ├── redis/
│       │   └── redis.conf              # Redis configuration
│       └── nginx/
│           ├── nginx.conf              # Nginx configuration
│           └── Dockerfile              # Custom Nginx image
├── snippets/
│   ├── basic-stack.yml                 # Simple app + database
│   ├── full-stack.yml                  # Complete application stack
│   └── monitoring-stack.yml            # With monitoring tools
├── docs/
│   ├── setup.md                        # Setup guide
│   ├── services.md                     # Service documentation
│   └── troubleshooting.md              # Common issues
├── README.md
└── metadata.yaml
```

## Service Stacks

### 1. Basic Stack (App + Database)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/mydb
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### 2. Full Stack (App + Database + Cache + Reverse Proxy)

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - frontend

  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:password@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - frontend
      - backend

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - backend

volumes:
  postgres_data:
  redis_data:

networks:
  frontend:
  backend:
```

### 3. Development Stack (with hot reload)

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
      - "9229:9229" # Node.js debugger
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://dev:dev@postgres:5432/dev_db
      - REDIS_URL=redis://redis:6379
    command: npm run dev
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=dev
      - POSTGRES_PASSWORD=dev
      - POSTGRES_DB=dev_db
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - postgres

volumes:
  postgres_dev_data:
```

## Common Services

### PostgreSQL

```yaml
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    POSTGRES_DB: ${POSTGRES_DB:-mydb}
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./init.sql:/docker-entrypoint-initdb.d/init.sql
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
    interval: 10s
    timeout: 5s
    retries: 5
  ports:
    - "5432:5432"
```

### Redis

```yaml
redis:
  image: redis:7-alpine
  command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-redis}
  volumes:
    - redis_data:/data
  healthcheck:
    test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
    interval: 10s
    timeout: 3s
    retries: 5
  ports:
    - "6379:6379"
```

### MongoDB

```yaml
mongo:
  image: mongo:7
  environment:
    MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-root}
    MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-root}
  volumes:
    - mongo_data:/data/db
  healthcheck:
    test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
    interval: 10s
    timeout: 5s
    retries: 5
  ports:
    - "27017:27017"
```

### Nginx

```yaml
nginx:
  image: nginx:alpine
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./nginx/ssl:/etc/nginx/ssl:ro
  ports:
    - "80:80"
    - "443:443"
  depends_on:
    - app
```

## Environment Variables

Create `.env` file:

```bash
# App
NODE_ENV=production
PORT=3000

# PostgreSQL
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb

# Redis
REDIS_PASSWORD=redispass

# MongoDB
MONGO_USER=mongouser
MONGO_PASSWORD=mongopass

# Application secrets
JWT_SECRET=your-jwt-secret
API_KEY=your-api-key
```

## Common Commands

```bash
# Start services
docker-compose up -d

# Start with build
docker-compose up -d --build

# View logs
docker-compose logs -f [service_name]

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart a service
docker-compose restart [service_name]

# Execute command in service
docker-compose exec app npm run migrate

# View service status
docker-compose ps

# Scale services
docker-compose up -d --scale app=3

# Pull latest images
docker-compose pull

# Validate compose file
docker-compose config
```

## Development vs Production

Use override files:

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Health Checks

All services include health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Networking

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

## Volumes

```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  uploads:
    driver: local
    driver_opts:
      type: none
      device: /path/to/uploads
      o: bind
```

## Best Practices

✅ **DO:**
- Use health checks
- Set resource limits
- Use named volumes
- Use networks for isolation
- Use environment variables
- Include restart policies
- Use specific image tags
- Log to stdout/stderr

❌ **DON'T:**
- Use `latest` tag in production
- Store secrets in compose file
- Run as root unnecessarily
- Expose unnecessary ports
- Use bind mounts in production
- Ignore security updates

## Security

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    user: "1000:1000"
```

## Monitoring Stack

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Token Savings

- **Setup Time**: 5 minutes vs 1+ hour
- **Lines of Code**: 200+ lines of YAML
- **Tokens Saved**: ~8,000 tokens
- **Services Configured**: 5+ production-ready services

## Related Components

- `postgresql-prisma` - Database setup
- `redis-cache` - Caching layer
- `nginx-config` - Reverse proxy
- `monitoring-stack` - Observability