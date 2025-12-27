# KAPI Production Deployment Guide

**Complete guide for deploying, monitoring, and operating KAPI services in production**

This document combines manual deployment procedures, automated deployment workflows, and template distribution setup.

---

## Production Architecture Overview

KAPI uses a **multi-server architecture** for better security and isolation:

| Server | SSH Alias | IP Address | Services |
|--------|-----------|------------|----------|
| **API Server** | `Kapi-New` | 130.131.126.114 | Backend API (port 4000), Admin Panel |
| **Landing Pages Server** | `All-Landing` | (separate server) | Frontend/Landing (port 3003), Other landing pages |

**DNS Configuration** (Cloudflare):
- `api.getkapi.com` → 130.131.126.114 (proxied, Full SSL via Configuration Rule)
- `admin.getkapi.com` → 130.131.126.114 (proxied, Full SSL via Configuration Rule)
- `getkapi.com` → All-Landing server (proxied, Flexible SSL)

---

## Must Do Checklist

```bash
# 1. Local verification
npm run build && node dist/server.js  # Test production build

# 2. Server pre-check (API Server)
ssh Kapi-New "bash -lc 'pm2 status && lsof -i :4000'"

# 3. Deploy Backend (Choose one)
# Option A: Automated (Recommended)
npm run deploy:prod
# Option B: Manual
ssh Kapi-New "cd /home/azureuser/kapi/backend && ./deploy.sh"

# 4. Deploy Frontend (on All-Landing server)
ssh All-Landing "cd /home/azureuser/landing-pages/apps/kapi && git pull && npm run build && pm2 restart kapi"

# 5. Verify
curl https://api.getkapi.com/health
curl https://getkapi.com
```

---

## 1. Production Architecture

**Last Updated:** December 15, 2025
**Environment:** Production (Multi-Server)
**Strategy:** Subdomain-based routing via Cloudflare + Nginx

### 1.1 Server Topology

KAPI services are split across two servers for security isolation:

#### API Server (Kapi-New: 130.131.126.114)

| Service              | Port | Domain                | Purpose                          | PM2 Process        |
|----------------------|------|-----------------------|----------------------------------|--------------------|
| **Backend API**      | 4000 | api.getkapi.com      | Express API + Admin panel        | kapi-backend       |

**Repo Path:** `/home/azureuser/kapi/backend/`

#### Landing Pages Server (All-Landing)

| Service              | Port | Domain                | Purpose                          | PM2 Process        |
|----------------------|------|-----------------------|----------------------------------|--------------------|
| **KAPI Frontend**    | 3003 | getkapi.com          | Next.js landing page + auth      | kapi               |
| Other Landing Pages  | various | -                 | Other company landing pages      | various            |

**Repo Path:** `/home/azureuser/landing-pages/apps/kapi/`

### 1.2 DNS Configuration (Cloudflare)

```
Type    Name     Value                  Proxy Status    TTL       SSL Mode
A       @        <All-Landing IP>      ✅ Proxied      Auto      Flexible
A       api      130.131.126.114       ✅ Proxied      Auto      Full (via Config Rule)
A       admin    130.131.126.114       ✅ Proxied      Auto      Full (via Config Rule)
CNAME   www      getkapi.com           ✅ Proxied      Auto      Flexible
```

**Important:** A Cloudflare Configuration Rule named "Full SSL for API/Admin" enforces Full SSL mode for `api.getkapi.com` and `admin.getkapi.com` subdomains, while the main landing page uses Flexible SSL.

---

## 2. Infrastructure Configuration

### 2.1 Nginx Configuration

#### API Server (Kapi-New) - `/etc/nginx/sites-available/api.getkapi.com`

```nginx
# API subdomain configuration
server {
    listen 80;
    listen [::]:80;
    server_name api.getkapi.com admin.getkapi.com;

    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.getkapi.com admin.getkapi.com;

    # SSL certificates from Cloudflare Origin
    ssl_certificate /etc/ssl/certs/getkapi.pem;
    ssl_certificate_key /etc/ssl/private/getkapi.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    access_log /var/log/nginx/api-getkapi-access.log;
    error_log /var/log/nginx/api-getkapi-error.log;

    # All routes proxy to backend on port 4000
    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

#### Landing Pages Server (All-Landing) - Nginx Configuration

The All-Landing server hosts multiple landing pages. KAPI frontend runs on port 3003:

```nginx
# KAPI landing page (part of multi-site configuration)
server {
    listen 80;
    server_name getkapi.com www.getkapi.com;

    location / {
        proxy_pass http://localhost:3003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2.2 SSL Configuration (Cloudflare Origin)

**Note**: Using Cloudflare Origin certificates (not Let's Encrypt)

```bash
# Certificates already installed at:
# - /etc/ssl/certs/getkapi.pem
# - /etc/ssl/private/getkapi.key

# Verify certificates
sudo ls -la /etc/ssl/certs/getkapi.pem
sudo ls -la /etc/ssl/private/getkapi.key

# Note: Cloudflare handles external SSL/TLS
# Origin certificates secure Cloudflare <-> Server connection
```

---

## 3. Service Deployments

### 3.1 Backend Deployment (API Server - Kapi-New)

#### Environment Configuration

**Location:** `/home/azureuser/kapi/backend/.env`

```bash
# Core
NODE_ENV=production
PORT=4000

# Database / Cache
DATABASE_URL=postgresql://kapiadmin:password@localhost:5432/kapi_mvp
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=<48-character-production-secret>
JWT_EXPIRES_IN=7d

# API URLs
KAPI_API_URL=https://api.getkapi.com

# CORS (production domains)
CORS_ORIGIN=https://getkapi.com,https://www.getkapi.com

# AI Provider Keys
GEMINI_API_KEY=...
AZURE_API_KEY=...
AZURE_ENDPOINT=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Admin Credentials
ADMIN_EMAIL=admin@getkapi.com
ADMIN_PASSWORD=<secure-password>
API_KEY=<secure-api-key-for-cli>

# Templates Configuration
TEMPLATES_BASE_PATH=/home/azureuser/kapi/templates
TOOLKIT_BASE_PATH=/home/azureuser/kapi/templates/toolkits
TOOLKIT_BINARIES_PATH=/home/azureuser/kapi/toolkit-binaries

# Frontend URL (for CORS and redirects)
FRONTEND_URL=https://getkapi.com
```

#### PM2 Process Definition

**Location:** `/home/azureuser/kapi/backend/ecosystem.config.cjs`

```json
{
  "apps": [{
    "name": "kapi-backend",
    "script": "dist/server.js",
    "cwd": "/home/azureuser/kapi/backend",
    "instances": 1,
    "exec_mode": "cluster",
    "env": {
      "NODE_ENV": "production",
      "PORT": 4000
    },
    "max_memory_restart": "1G",
    "autorestart": true,
    "watch": false,
    "log_date_format": "YYYY-MM-DD HH:mm:ss Z",
    "error_file": "/home/azureuser/kapi/pm2-logs/kapi-backend-error.log",
    "out_file": "/home/azureuser/kapi/pm2-logs/kapi-backend-out.log",
    "merge_logs": true
  }]
}
```

#### Manual Deployment Script

**Location:** `/home/azureuser/kapi/backend/deploy.sh`

```bash
#!/bin/bash
set -e

echo "🚀 Deploying backend to port 4000..."

cd /home/azureuser/kapi/backend

# Pull latest code
git fetch origin
git pull origin dev

# Install dependencies
npm ci --production=false

# Build TypeScript
npm run build

# Run database migrations
npx prisma migrate deploy
npx prisma generate

# Reload PM2 (zero downtime)
~/.nvm/versions/node/v20.19.2/bin/pm2 reload kapi-backend --update-env

# Save PM2 process list
~/.nvm/versions/node/v20.19.2/bin/pm2 save

echo "✅ Backend deployed successfully"

# Health check
sleep 3
curl -f http://localhost:4000/health || echo "⚠️ Health check failed"
```

---

### 3.2 Frontend Deployment (Landing Pages Server - All-Landing)

The KAPI frontend runs on the All-Landing server alongside other landing pages.

#### Environment Configuration

**Location:** `/home/azureuser/landing-pages/apps/kapi/.env`

```bash
# Backend API Configuration
NEXT_PUBLIC_API_URL=https://api.getkapi.com

# Site Configuration
NEXT_PUBLIC_SITE_URL=https://getkapi.com
NEXT_PUBLIC_SUPPORT_EMAIL=support@getkapi.com
```

**Important:** `NEXT_PUBLIC_*` variables are baked into the build at compile time. After changing these values, you must rebuild the Next.js application.

#### PM2 Process

The KAPI frontend runs as PM2 process `kapi` on port 3003:

```bash
# Check status
ssh All-Landing "pm2 status kapi"

# View logs
ssh All-Landing "pm2 logs kapi --lines 50"
```

#### Manual Deployment Script

```bash
#!/bin/bash
# Deploy KAPI frontend on All-Landing server
set -e

echo "🚀 Deploying frontend to port 3003..."

cd /home/azureuser/landing-pages/apps/kapi

# Pull latest code
git fetch origin
git pull origin dev

# Install dependencies
npm ci

# Build Next.js (bakes in NEXT_PUBLIC_* env vars)
rm -rf .next
npm run build

# Reload PM2 (zero downtime)
pm2 reload kapi --update-env

# Save PM2 process list
pm2 save

echo "✅ Frontend deployed successfully"

# Health check
sleep 3
curl -f http://localhost:3003 || echo "⚠️ Health check failed"
```

**Note:** The All-Landing server hosts multiple landing pages on different ports. Be careful not to interfere with other services when deploying.

---

## 4. Deployment Automation

### 4.1 Production Deployment Script (deploy-prod.sh)

**Automated deployment from local machine to production server.**

#### Usage

```bash
# Basic backend deployment
npm run deploy:prod

# Backend + Frontend + Templates + Reindex
npm run deploy:prod:full

# Dry run (preview changes)
npm run deploy:prod:dry

# Or directly:
./deploy-prod.sh [options]
```

#### Options

| Flag | Description |
|------|-------------|
| `--frontend` | Deploy frontend in addition to backend |
| `--templates` | Update templates repository and regenerate bundles |
| `--reindex` | Reindex blueprints and components after deployment |
| `--dry-run` | Show what would be done without executing |
| `--skip-health` | Skip health checks |
| `-h, --help` | Show help message |

#### Examples

```bash
# Deploy backend only (most common)
./deploy-prod.sh

# Deploy backend + frontend
./deploy-prod.sh --frontend

# Deploy with new templates and reindex
./deploy-prod.sh --templates --reindex

# Full stack deployment with everything
./deploy-prod.sh --frontend --templates --reindex

# Preview changes before deploying
./deploy-prod.sh --frontend --templates --reindex --dry-run
```

---

### 4.2 Admin API Endpoints

#### Authentication

All admin endpoints require authentication via API key:

```bash
curl -H "X-API-Key: your-api-key" https://api.getkapi.com/api/v1/admin/...
```

#### Available Endpoints

##### 1. Reindex Blueprints

Reindex all blueprints into LanceDB for semantic search.

```bash
POST /api/v1/admin/reindex/blueprints

# Example
curl -X POST https://api.getkapi.com/api/v1/admin/reindex/blueprints \
  -H "X-API-Key: $API_KEY"
```

**Response:**
```json
{
  "success": true,
  "message": "Blueprint reindexing completed",
  "indexed": 34,
  "failed": 0,
  "timestamp": "2025-10-07T20:00:00.000Z"
}
```

##### 2. Reindex Components

Reindex all components into LanceDB for semantic search.

```bash
POST /api/v1/admin/reindex/components

# Example
curl -X POST https://api.getkapi.com/api/v1/admin/reindex/components \
  -H "X-API-Key: $API_KEY"
```

**Response:**
```json
{
  "success": true,
  "message": "Component reindexing completed",
  "indexed": 36,
  "failed": 0,
  "timestamp": "2025-10-07T20:00:00.000Z"
}
```

##### 3. Reindex All

Reindex both blueprints and components in one call.

```bash
POST /api/v1/admin/reindex/all

# Example
curl -X POST https://api.getkapi.com/api/v1/admin/reindex/all \
  -H "X-API-Key: $API_KEY"
```

**Response:**
```json
{
  "success": true,
  "message": "Full reindex completed",
  "blueprints": {
    "indexed": 34,
    "failed": 0
  },
  "components": {
    "indexed": 36,
    "failed": 0
  },
  "total": {
    "indexed": 70,
    "failed": 0
  },
  "timestamp": "2025-10-07T20:00:00.000Z"
}
```

##### 4. Admin Stats

Get statistics about indexed items.

```bash
GET /api/v1/admin/stats

# Example
curl https://api.getkapi.com/api/v1/admin/stats \
  -H "X-API-Key: $API_KEY"
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "components": {
      "total": 36,
      "byCategory": {
        "authentication": 3,
        "database": 4,
        "deployment": 5
      },
      "totalTokenSavings": 150000,
      "averageSetupTime": 8
    }
  },
  "timestamp": "2025-10-07T20:00:00.000Z"
}
```

---

### 4.3 When to Reindex

#### Automatic Reindex (Recommended)

Use the deployment script with `--reindex` flag:

```bash
./deploy-prod.sh --templates --reindex
```

This will:
1. Pull latest templates
2. Regenerate bundles
3. Deploy backend
4. Trigger reindex via API

#### Manual Reindex

Trigger reindex manually when:
- New blueprints/components added to templates repo
- Template metadata updated
- LanceDB database needs refresh
- After templates repository sync

```bash
# On server
curl -X POST http://localhost:4000/api/v1/admin/reindex/all \
  -H "X-API-Key: $API_KEY"

# Or remotely
curl -X POST https://api.getkapi.com/api/v1/admin/reindex/all \
  -H "X-API-Key: $API_KEY"
```

---

## 5. Deployment Workflows

### 5.1 Manual Full Stack Deployment

```bash
# === API Server (Kapi-New) ===
ssh Kapi-New

# 1. Deploy Backend
cd /home/azureuser/kapi/backend
./deploy.sh

# 2. Verify backend
pm2 status kapi-backend
pm2 logs kapi-backend --lines 50

# === Landing Pages Server (All-Landing) ===
ssh All-Landing

# 3. Deploy Frontend
cd /home/azureuser/landing-pages/apps/kapi
git pull origin dev
rm -rf .next && npm run build
pm2 reload kapi

# 4. Verify frontend
pm2 status kapi
pm2 logs kapi --lines 50
```

### 5.2 Automated Deployment (Recommended)

#### Standard Feature Update

```bash
# From local machine

# 1. Local verification
npm run build

# 2. Deploy to production
npm run deploy:prod

# 3. Verify
curl https://api.getkapi.com/health
```

#### Full Stack Update (With New Templates)

```bash
# From local machine

# 1. Test locally
npm run deploy:prod:dry

# 2. Deploy everything
npm run deploy:prod:full
# This runs: ./deploy-prod.sh --frontend --templates --reindex

# 3. Verify all services
curl https://api.getkapi.com/health
curl https://getkapi.com
curl https://api.getkapi.com/api/v1/templates/catalog
```

#### Rollback

**Backend rollback (on Kapi-New):**
```bash
ssh Kapi-New
cd /home/azureuser/kapi/backend
git log -5  # Find previous commit
git checkout <commit-hash>
npm ci
npm run build
pm2 reload kapi-backend
```

**Frontend rollback (on All-Landing):**
```bash
ssh All-Landing
cd /home/azureuser/landing-pages/apps/kapi
git log -5  # Find previous commit
git checkout <previous-commit-hash>
npm ci
rm -rf .next && npm run build
pm2 reload kapi
```

### 5.3 Quick PM2 Commands

```bash
# === API Server (Kapi-New) ===
ssh Kapi-New

# Status
pm2 status
pm2 monit

# Logs
pm2 logs kapi-backend

# Restart
pm2 restart kapi-backend
pm2 reload kapi-backend  # zero downtime

# === Landing Pages Server (All-Landing) ===
ssh All-Landing

# Status
pm2 status kapi

# Logs
pm2 logs kapi

# Restart
pm2 reload kapi  # zero downtime
```

---

## 6. Template Distribution Setup

### 6.1 Directory Structure

**API Server (Kapi-New) Layout:**

```
/home/azureuser/kapi/
├── backend/                       # Backend API (Express.js)
│   ├── src/
│   ├── dist/
│   ├── .env
│   └── ecosystem.config.cjs
├── templates/                     # Templates repo (SEPARATE git repo)
│   ├── .git/                     # git@github.com:Kapi-IDE/templates.git
│   ├── catalog.json              # Unified manifest (generated)
│   ├── blueprints/               # 34 production blueprints
│   ├── components/               # 36 reusable components
│   ├── quality-baselines/        # Quality checklists
│   ├── recipes/                  # Methodology guides
│   └── toolkits/                 # Toolkit manifest
├── toolkit-binaries/             # Analysis tools
│   ├── scc                       # 6 MB - Code counting
│   ├── gitleaks                  # 12 MB - Secret detection
│   ├── semgrep                   # 100 MB - Security scanning (LGPL-2.1)
│   └── hugot                     # 50 MB - Embedding model
└── pm2-logs/                     # PM2 log files
```

**Landing Pages Server (All-Landing) Layout:**

```
/home/azureuser/landing-pages/
├── apps/
│   ├── kapi/                     # KAPI frontend (Next.js)
│   │   ├── src/
│   │   ├── .next/
│   │   ├── .env
│   │   └── package.json
│   ├── other-landing-1/          # Other landing pages
│   └── other-landing-2/
└── nginx/                        # Nginx configs
```

---

### 6.2 Initial Setup (One-Time)

#### Step 1: Clone Templates Repository (on Kapi-New)

```bash
ssh Kapi-New

# Clone separate templates repo
cd /home/azureuser/kapi
git clone https://github.com/Kapi-IDE/templates.git templates

cd templates
git log -3 --oneline
```

---

#### Step 2: Generate Asset Bundles

**Option A: Minimal catalog for testing (RECOMMENDED FOR FIRST DEPLOYMENT)**

```bash
cd /home/azureuser/kapi/templates

cat > catalog.json << 'EOF'
{
  "version": "2025.10.05",
  "generatedAt": "2025-10-05T23:20:00.000Z",
  "schemaVersion": "1.0.0",
  "assets": {
    "blueprints": [],
    "components": [],
    "quality-baselines": [],
    "recipes": []
  },
  "statistics": {
    "blueprints": 0,
    "components": 0,
    "qualityBaselines": 0,
    "recipes": 0,
    "total": 0
  }
}
EOF
```

**Option B: Generate full bundles and catalog (REQUIRES NODE.JS SETUP)**

```bash
cd /home/azureuser/kapi/templates

# Make bundling script executable
chmod +x scripts/bundle-assets.sh

# Install js-yaml dependency
~/.nvm/versions/node/v20.19.2/bin/npm install --no-save js-yaml

# Generate all bundles and catalog.json
./scripts/bundle-assets.sh

# Verify catalog was generated
ls -lh catalog.json
cat catalog.json | head -30
```

---

#### Step 3: Download Toolkit Binaries

**Context**: Per DAD-20250129-001 Decision 4, KAPI requires 5 external tools for analysis:
- **scc** (6 MB) - Code statistics [MIT/Unlicense]
- **gitleaks** (12 MB) - Secret detection [MIT]
- **semgrep** (100 MB) - Security scanning (SAST) [LGPL-2.1]
- **jscpd** (~5 MB) - Copy-paste detection [MIT]
- **hugot** (50 MB) - Local embeddings [MIT]

```bash
# Create binaries directory
mkdir -p /home/azureuser/kapi/toolkit-binaries
cd /home/azureuser/kapi/toolkit-binaries

# Download scc (6 MB) - Code counting
echo "📦 Downloading scc..."
wget https://github.com/boyter/scc/releases/download/v3.3.5/scc_Linux_x86_64.tar.gz
tar -xzf scc_Linux_x86_64.tar.gz
chmod +x scc
rm scc_Linux_x86_64.tar.gz LICENSE* README.md 2>/dev/null || true
./scc --version

# Download gitleaks (12 MB) - Secret detection
echo "📦 Downloading gitleaks..."
wget https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz
tar -xzf gitleaks_8.21.2_linux_x64.tar.gz
chmod +x gitleaks
rm gitleaks_8.21.2_linux_x64.tar.gz LICENSE* README.md 2>/dev/null || true
./gitleaks version

# Download semgrep (100 MB) - Security scanning (LGPL-2.1)
echo "📦 Downloading semgrep..."
wget -q https://github.com/semgrep/semgrep/releases/download/v1.72.0/semgrep-v1.72.0-ubuntu-generic-x86_64.tar.gz
tar -xzf semgrep-v1.72.0-ubuntu-generic-x86_64.tar.gz
mv semgrep-files/semgrep-core semgrep
chmod +x semgrep
rm -rf semgrep-files semgrep-v1.72.0-ubuntu-generic-x86_64.tar.gz
./semgrep --version

# Install jscpd (~5 MB) - Copy-paste detection (via npm global)
echo "📦 Installing jscpd..."
~/.nvm/versions/node/v20.19.2/bin/npm install -g jscpd
~/.nvm/versions/node/v20.19.2/bin/jscpd --version
# Optional: Create symlink for easier access
sudo ln -sf ~/.nvm/versions/node/v20.19.2/bin/jscpd /usr/local/bin/jscpd 2>/dev/null || true

# Download hugot (50 MB) - Embedding model
echo "📦 Downloading hugot..."
# Note: hugot download URL to be added
# wget -q <hugot-download-url>
# chmod +x hugot
echo "⚠️  hugot download URL needed"

# Verify all binaries
echo "✅ Toolkit binaries installed:"
ls -lh
file scc gitleaks semgrep
which jscpd
```

**Expected Output:**
```
total 168M
-rwxr-xr-x 1 azureuser azureuser   6M Oct  5 12:00 scc
-rwxr-xr-x 1 azureuser azureuser  12M Oct  5 12:01 gitleaks
-rwxr-xr-x 1 azureuser azureuser 100M Oct  5 12:02 semgrep
-rwxr-xr-x 1 azureuser azureuser  50M Oct  5 12:03 hugot

jscpd: /usr/local/bin/jscpd (installed via npm global)
```

---

#### Step 4: Configure Backend Environment (on Kapi-New)

Add to `/home/azureuser/kapi/backend/.env`:

```bash
# Add templates configuration
cd /home/azureuser/kapi/backend

# Add environment variables (if not already present)
grep -q "^TEMPLATES_BASE_PATH=" .env || echo "TEMPLATES_BASE_PATH=/home/azureuser/kapi/templates" >> .env
grep -q "^TOOLKIT_BASE_PATH=" .env || echo "TOOLKIT_BASE_PATH=/home/azureuser/kapi/templates/toolkits" >> .env

# Verify
tail -5 .env
```

---

#### Step 5: Restart Backend API (on Kapi-New)

```bash
# Set PATH and reload PM2 process
export PATH="/home/azureuser/.nvm/versions/node/v20.19.2/bin:$PATH"
pm2 reload kapi-backend --update-env

# Wait for restart
sleep 3

# Verify backend is running
pm2 status kapi-backend

# Check logs for any errors
pm2 logs kapi-backend --lines 20 --nostream
```

---

### 6.3 Regular Updates

#### Update Templates Repository (on Kapi-New)

```bash
ssh Kapi-New
cd /home/azureuser/kapi/templates

# Pull latest from GitHub
git fetch origin
git pull origin main

# Regenerate bundles and catalog
./scripts/bundle-assets.sh

# Verify new version
cat catalog.json | jq '.version'

# Restart backend to pick up changes
pm2 reload kapi-backend
```

#### Update Toolkit Binaries (as needed)

```bash
cd /home/azureuser/kapi/toolkit-binaries

# Check current versions
./scc --version
./gitleaks version
./semgrep --version

# Download new versions (replace URLs with latest)
# Follow Step 3 download commands with updated version numbers
```

---

### 6.4 Health Checks

#### Verify Templates Setup

```bash
# 1. Check templates repo exists
ls -la /home/azureuser/kapi/templates
cat /home/azureuser/kapi/templates/catalog.json | jq '.version'

# 2. Check toolkit binaries exist
ls -lh /home/azureuser/kapi/toolkit-binaries

# 3. Check backend can read catalog
curl http://localhost:4000/api/v1/templates/catalog

# 4. Check public API access
curl https://api.getkapi.com/api/v1/templates/catalog | jq '.catalog.version'

# 5. Check toolkit manifest
curl https://api.getkapi.com/api/v1/toolkits/manifest | jq '.version'

# 6. Test blueprint details endpoint
curl https://api.getkapi.com/api/v1/templates/blueprints/deep-document-analysis/details | jq '.asset.name'

# 7. Test download endpoint (requires auth)
curl -I -H "X-API-Key: $API_KEY" \
  https://api.getkapi.com/api/v1/templates/blueprints/deep-document-analysis/download

# Expected headers:
# Content-Type: application/octet-stream
# Content-Disposition: attachment; filename="bundle.tar.zst"
# X-Asset-Version: 1.0.0
# X-Asset-Sha256: abc123...
```

#### Production Health Check Script

```bash
#!/bin/bash
# templates-health-check.sh

echo "🔍 KAPI Templates Health Check"
echo "================================"

# Check templates repo
if [ -d "/home/azureuser/kapi/templates" ]; then
  echo "✅ Templates repo exists"
  VERSION=$(cat /home/azureuser/kapi/templates/catalog.json | jq -r '.version')
  echo "   Version: $VERSION"
else
  echo "❌ Templates repo NOT found"
  exit 1
fi

# Check binaries
BINARIES=("scc" "gitleaks" "semgrep" "hugot")
for binary in "${BINARIES[@]}"; do
  if [ -f "/home/azureuser/kapi/toolkit-binaries/$binary" ]; then
    echo "✅ $binary binary exists"
  else
    echo "⚠️  $binary binary missing"
  fi
done

# Check jscpd (npm global)
if command -v jscpd &> /dev/null; then
  echo "✅ jscpd installed ($(jscpd --version))"
else
  echo "⚠️  jscpd missing"
fi

# Check API endpoints
echo ""
echo "Testing API endpoints..."

CATALOG=$(curl -s http://localhost:4000/api/v1/templates/catalog | jq -r '.success')
if [ "$CATALOG" = "true" ]; then
  echo "✅ /api/v1/templates/catalog working"
else
  echo "❌ /api/v1/templates/catalog FAILED"
fi

TOOLKITS=$(curl -s http://localhost:4000/api/v1/toolkits/manifest | jq -r '.success')
if [ "$TOOLKITS" = "true" ]; then
  echo "✅ /api/v1/toolkits/manifest working"
else
  echo "❌ /api/v1/toolkits/manifest FAILED"
fi

echo ""
echo "✅ Health check complete"
```

---

### 6.5 Deployment Workflow (Templates-Specific)

**Complete Templates Deployment (on Kapi-New):**

```bash
#!/bin/bash
# Full deployment including templates and binaries

# 1. Update main code repo
cd /home/azureuser/kapi/backend
git pull origin dev
npm ci
npm run build
npx prisma migrate deploy

# 2. Update templates repo
cd /home/azureuser/kapi/templates
git pull origin main
./scripts/bundle-assets.sh

# 3. Verify toolkit binaries exist
ls -lh /home/azureuser/kapi/toolkit-binaries

# 4. Restart backend
pm2 reload kapi-backend --update-env

# 5. Health check
curl http://localhost:4000/health
curl http://localhost:4000/api/v1/templates/catalog | jq '.catalog.version'
```

---

### 6.6 Troubleshooting (Templates-Specific)

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| **Catalog not found** | Backend can't read catalog.json | Check `TEMPLATES_BASE_PATH` in `.env`, create minimal catalog.json (see Step 2) |
| **Bundle missing** | Bundles not generated | Create minimal catalog first, generate full bundles later |
| **Node PATH issues** | npm/node commands fail | Use full paths: `~/.nvm/versions/node/v20.19.2/bin/node` or set PATH |
| **Download fails** | Path traversal or missing bundle | Check bundle path in catalog.json, verify bundle exists on disk |
| **Binaries missing** | Toolkit binaries not downloaded | Re-run Step 3 binary downloads |
| **Permission denied** | File permissions wrong | Run `chmod +x /home/azureuser/kapi/toolkit-binaries/*` |
| **API returns 404** | Routes not mounted | Check backend logs, verify templates routes are registered |
| **Checksum mismatch** | Bundle changed after catalog generation | Regenerate catalog: `./scripts/bundle-assets.sh` |
| **Git pull fails** | Merge conflicts in templates repo | Stash changes: `git stash && git pull origin main` |

---

### 6.7 Monitoring & Maintenance

#### Disk Usage Monitoring

```bash
# Check templates repo size
du -sh /home/azureuser/kapi/templates

# Check individual categories
du -sh /home/azureuser/kapi/templates/blueprints/*
du -sh /home/azureuser/kapi/templates/components/*

# Check toolkit binaries size
du -sh /home/azureuser/kapi/toolkit-binaries
```

#### Log Monitoring

```bash
# Watch for template download requests
~/.nvm/versions/node/v20.19.2/bin/pm2 logs kapi-backend | grep -i "template"

# Check for errors
tail -f /home/azureuser/kapi/pm2-logs/kapi-backend-error.log | grep -i "catalog\|bundle"
```

#### Automated Updates (Optional)

```bash
# Add to crontab for weekly template updates
# crontab -e

# Update templates every Sunday at 2 AM
0 2 * * 0 cd /home/azureuser/kapi/templates && git pull origin main && ./scripts/bundle-assets.sh && pm2 reload kapi-backend
```

---

### 6.8 Security Considerations

1. **Path Traversal Prevention**: TemplateCatalogService validates all paths against base directory
2. **Checksum Verification**: SHA-256 checksums in catalog.json prevent tampering
3. **Authentication**: Download endpoints require API key or JWT token
4. **LGPL Compliance**: Semgrep (LGPL-2.1) - source links provided, no static bundling
5. **Audit Logging**: All downloads logged with user ID, asset ID, timestamp

---

### 6.9 Reference

**Environment Variables:**
```bash
TEMPLATES_BASE_PATH=/home/azureuser/kapi/templates
TOOLKIT_BASE_PATH=/home/azureuser/kapi/templates/toolkits
TOOLKIT_BINARIES_PATH=/home/azureuser/kapi/toolkit-binaries
```

**API Endpoints:**
```
GET  /api/v1/templates/catalog
GET  /api/v1/templates/:type/:slug/details
GET  /api/v1/templates/:type/:slug/download
GET  /api/v1/toolkits/manifest
GET  /api/v1/toolkits/:platform/download
```

**Related Documentation:**
- Templates Repo: `https://github.com/Kapi-IDE/templates`
- Blueprint Spec: `/docs/02-what/modes/blueprint.spec.md`
- DAD Decision 4: `/docs/05-project-management-meta/DAD-20250129-001-architectural-foundations.yaml`
- Toolkit Service: `backend-new/src/services/toolkit.service.ts`
- Template Catalog Service: `backend-new/src/services/template-catalog.service.ts`

---

## 7. Health Checks & Monitoring

### 7.1 Service Health Checks

#### Backend Health

```bash
# Local
curl http://localhost:4000/health
curl http://localhost:4000/

# Production
curl https://api.getkapi.com/health
curl https://api.getkapi.com/
```

#### Frontend Health

```bash
# Local
curl http://localhost:3001

# Production
curl https://getkapi.com
```

### 7.2 Monitoring Commands

```bash
# PM2 monitoring
pm2 monit
pm2 list
pm2 info kapi-backend

# System resources
htop
df -h
free -m

# Port usage
sudo netstat -tlnp | grep -E ':(3001|4000)'
sudo lsof -i :4000
```

### 7.3 Deployment Status Monitoring

#### Check Deployment Status

```bash
# PM2 status
ssh Kapi-New 'pm2 status'

# Logs
ssh Kapi-New 'pm2 logs kapi-backend --lines 100'

# Health checks
curl https://api.getkapi.com/health
curl https://api.getkapi.com/api/v1/admin/stats -H "X-API-Key: $API_KEY"
```

#### Check Reindex Status

```bash
# Check component stats
curl https://api.getkapi.com/api/v1/components/stats

# Test search
curl -X POST https://api.getkapi.com/api/v1/blueprints/search \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication system", "topK": 3}'
```

---

## 8. Troubleshooting

### 8.1 Service Issues

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Port already in use | `sudo lsof -i :4000` | Kill process or change port |
| PM2 not found | Check NVM path | Use full path: `~/.nvm/versions/node/v20.19.2/bin/pm2` |
| Build fails | Check TypeScript errors | Run `npm run build` locally first |
| Database errors | Check connection string | Verify `DATABASE_URL` in `.env` |
| CORS errors | Check origins | Update `CORS_ORIGIN` in backend `.env` |
| 502 Bad Gateway | Backend down | Check `pm2 logs kapi-backend` |
| SSL issues | Certificate expired | Verify Cloudflare Origin certificates |

### 8.2 Deployment Script Issues

#### Deployment Script Fails

```bash
# Check SSH access
ssh Kapi-New 'echo "Connection OK"'

# Check PM2 is available
ssh Kapi-New 'which pm2'

# Run in dry-run mode to debug
./deploy-prod.sh --dry-run
```

#### Reindex Fails

```bash
# Check LanceDB service
curl http://localhost:4000/api/v1/components/stats

# Check logs
pm2 logs kapi-backend | grep -i "reindex"

# Manual reindex with verbose output
curl -X POST http://localhost:4000/api/v1/admin/reindex/all \
  -H "X-API-Key: $API_KEY" \
  -v
```

#### Templates Not Updating

```bash
# Check templates repo on server
ssh Kapi-New 'cd /home/azureuser/kapi/templates && git status'

# Verify bundle generation script exists
ssh Kapi-New 'ls -la /home/azureuser/kapi/templates/scripts/bundle-assets.sh'

# Manual bundle generation
ssh Kapi-New 'cd /home/azureuser/kapi/templates && ./scripts/bundle-assets.sh'
```

---

## 9. Rollback Procedures

### Quick Rollback

```bash
# === Backend Rollback (on Kapi-New) ===
ssh Kapi-New
cd /home/azureuser/kapi/backend
git log -5  # Find previous commit
git checkout <previous-commit-hash>
npm ci
npm run build
pm2 reload kapi-backend

# === Frontend Rollback (on All-Landing) ===
ssh All-Landing
cd /home/azureuser/landing-pages/apps/kapi
git log -5  # Find previous commit
git checkout <previous-commit-hash>
npm ci
rm -rf .next && npm run build
pm2 reload kapi
```

### Database Rollback (on Kapi-New)

```bash
# If migration caused issues
ssh Kapi-New
cd /home/azureuser/kapi/backend

# Check migration history
npx prisma migrate status

# Rollback last migration (manual)
# Edit migrations directory and revert schema
npx prisma migrate resolve --rolled-back <migration-name>
npx prisma migrate deploy
```

---

## 10. Security Checklist

### Infrastructure Security

- [x] Firewall configured (ports 80, 443 open)
- [x] SSL certificates installed (Cloudflare Origin)
- [x] API key authentication for CLI
- [x] JWT authentication for web users
- [x] CORS configured for production domains
- [x] Environment secrets not in git
- [x] Database credentials secured
- [x] PM2 logs rotated

### Application Security

- [ ] Rate limiting enabled (in backend code)
- [ ] Fail2ban configured for SSH
- [ ] Regular security updates
- [x] Path traversal protection (templates)
- [x] Checksum verification (bundles)
- [x] Audit logging (downloads)

### Additional Security Notes

1. **API Key Protection**: Admin endpoints require valid API key
2. **SSH Access**: Deployment script requires SSH access to Kapi-New
3. **Dry Run First**: Always test with `--dry-run` for major changes
4. **Health Checks**: Script validates services after deployment
5. **LGPL Compliance**: Semgrep source links provided, no static bundling

---

## 11. Production URLs & Reference

### Production URLs

- **Frontend**: https://getkapi.com
- **API**: https://api.getkapi.com
- **Admin**: https://admin.getkapi.com
- **API Health**: https://api.getkapi.com/health
- **API Docs**: https://api.getkapi.com/api/v1

### Related Documentation

- **Backend README**: `/backend-new/README.md`
- **Frontend README**: `/frontend/README.md`
- **Templates Repo**: https://github.com/Kapi-IDE/templates
- **Blueprint Spec**: `/docs/02-what/modes/blueprint.spec.md`
- **Component Flow**: `/docs/03-how/implementation/component-installation-flow.md`

---

_Last updated: December 15, 2025_
_Migrated to multi-server architecture (API on Kapi-New, Frontend on All-Landing)_
