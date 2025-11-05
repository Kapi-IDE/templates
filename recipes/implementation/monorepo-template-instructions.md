# Modern Monorepo Structure Template Instructions

This template provides comprehensive instructions for creating a production-ready monorepo structure using FastAPI, React, Poetry, and other modern development tools. Follow these instructions sequentially to create a well-organized, scalable project structure.

## Prerequisites
Ensure the following are installed and also giving instructions for the same.
- Python 3.9+
- Node.js 18+
- Poetry
- Git
- Poetry 2.0

## 1. Initialize Monorepo Structure

Create the base directory structure:

```bash
mkdir -p {project_name}
cd {project_name}
git init

# Create base directories
mkdir -p backend
mkdir -p frontend
mkdir -p shared
mkdir -p docs
mkdir -p tests
mkdir -p .github/workflows
mkdir -p scripts
mkdir -p infrastructure
```

## 2. Backend Setup (FastAPI + Poetry + Pydantic)

### 2.1 Initialize Backend Project

```bash
cd backend
poetry init --name="{project_name}-backend" --description="Backend service for {project_name}" --author="Your Name <your.email@example.com>"
```

### 2.2 Add Dependencies

```bash
# Core dependencies
poetry add fastapi uvicorn pydantic python-dotenv sqlalchemy alembic asyncpg psycopg2-binary
poetry add jwt redis celery 
poetry add loguru

# Development dependencies
poetry add --group dev pytest pytest-asyncio pytest-cov black ruff mypy types-redis httpx
```

### 2.3 Create Backend Structure

```bash
mkdir -p app/{core,models,schemas,services,routes,utils}
mkdir -p tests/{unit,integration,e2e}
mkdir -p migrations

# Create __init__.py files
touch app/__init__.py
touch app/{core,models,schemas,services,routes,utils}/__init__.py
touch tests/__init__.py
touch tests/{unit,integration,e2e}/__init__.py
```

### 2.4 Create Core Backend Files

Create app/main.py:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Create app/core/config.py:
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "{project_name}"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for {project_name}"
    API_V1_STR: str = "/api/v1"
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 2.5 Setup Backend Testing
{Setup a folder for manual testing. Create the initial test cases for that}

Create tests/conftest.py:
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
```

Create pyproject.toml configuration:
```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=app --cov-report=html"
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 88
target-version = "py39"
select = ["E", "F", "W", "C90", "I", "N", "UP", "S", "B", "A", "C4", "ISC", "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SIM", "TID", "TCH", "INT", "ARG", "PTH"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.9"
strict = true
```

## 3. Frontend Setup (React + Vite + TypeScript)

### 3.1 Initialize Frontend Project

```bash
cd ../frontend
npm create vite@latest . -- --template react-ts
npm install
```

### 3.2 Add Dependencies

```bash
# Core dependencies
npm install @tanstack/react-query axios react-router-dom zustand
npm install @emotion/react @emotion/styled @mui/material @mui/icons-material

# Development dependencies
npm install -D @types/node @typescript-eslint/eslint-plugin @typescript-eslint/parser
npm install -D eslint eslint-config-prettier eslint-plugin-react eslint-plugin-react-hooks
npm install -D prettier vitest @testing-library/react @testing-library/jest-dom
npm install -D @playwright/test
```

### 3.3 Create Frontend Structure

```bash
mkdir -p src/{components,pages,hooks,services,store,utils,types,styles}
mkdir -p src/components/{common,layout}
mkdir -p src/tests/{unit,integration,e2e}
```

### 3.4 Configure ESLint and Prettier

Create .eslintrc.cjs:
```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'plugin:react/recommended',
    'prettier'
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  settings: {
    react: {
      version: 'detect'
    }
  },
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'react/react-in-jsx-scope': 'off'
  },
}
```

Create .prettierrc:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### 3.5 Setup Playwright

Create playwright.config.ts:
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './src/tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 4. Shared Module Setup

```bash
cd ../shared
mkdir -p types models utils
touch index.ts
```

Create package.json for shared module:
```json
{
  "name": "@{project_name}/shared",
  "version": "1.0.0",
  "main": "index.ts",
  "types": "index.ts",
  "scripts": {
    "build": "tsc",
    "lint": "eslint . --ext .ts,.tsx"
  }
}
```

## 5. Root Configuration

### 5.1 Create Root package.json

```json
{
  "name": "{project_name}",
  "private": true,
  "workspaces": [
    "frontend",
    "shared"
  ],
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd backend && poetry run uvicorn app.main:app --reload",
    "dev:frontend": "cd frontend && npm run dev",
    "test": "npm run test:backend && npm run test:frontend",
    "test:backend": "cd backend && poetry run pytest",
    "test:frontend": "cd frontend && npm run test",
    "lint": "npm run lint:backend && npm run lint:frontend",
    "lint:backend": "cd backend && poetry run ruff check . && poetry run mypy .",
    "lint:frontend": "cd frontend && npm run lint",
    "format": "npm run format:backend && npm run format:frontend",
    "format:backend": "cd backend && poetry run black .",
    "format:frontend": "cd frontend && npm run prettier",
    "e2e": "cd frontend && npm run test:e2e"
  },
  "devDependencies": {
    "concurrently": "^8.0.0"
  }
}
```

### 5.2 Create .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
.env
.venv
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/

# Node
node_modules/
dist/
build/
.DS_Store
*.log
npm-debug.log*
.eslintcache

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Project specific
*.sqlite3
*.db
.env.local
.env.*.local
coverage/
playwright-report/
test-results/
```

## 6. Infrastructure Templates

### 6.1 Docker Configuration

Create Dockerfile.backend:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create Dockerfile.frontend:
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

Create docker-compose.yml:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 7. GitHub Actions CI/CD

Create .github/workflows/ci.yml:
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install Poetry
        run: pip install poetry
      - name: Install dependencies
        run: cd backend && poetry install
      - name: Run tests
        run: cd backend && poetry run pytest
      - name: Lint
        run: cd backend && poetry run ruff check . && poetry run mypy .

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend && npm ci
      - name: Lint
        run: cd frontend && npm run lint
      - name: Test
        run: cd frontend && npm run test
      - name: Build
        run: cd frontend && npm run build

  e2e-test:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install Playwright
        run: cd frontend && npm ci && npx playwright install --with-deps
      - name: Run E2E tests
        run: cd frontend && npm run test:e2e
```

## Usage Instructions

1. Replace `{project_name}` with your actual project name throughout all files
2. Run `poetry install` in the backend directory
3. Run `npm install` in the frontend directory
4. Create necessary .env files based on the configuration
5. Start development with `npm run dev` from the root directory

## Key Features

- **Modular Architecture**: Clean separation between frontend, backend, and shared code
- **Type Safety**: TypeScript in frontend, Pydantic in backend
- **Testing**: Unit, integration, and E2E tests with Pytest and Playwright
- **Code Quality**: ESLint, Prettier, Ruff, and MyPy for code formatting and linting
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Containerization**: Docker and Docker Compose for deployment
- **Developer Experience**: Hot reloading, concurrent development servers, unified scripts

This template provides a solid foundation for a production-ready monorepo setup that follows modern best practices and conventions.
