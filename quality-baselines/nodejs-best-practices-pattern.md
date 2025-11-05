# Node.js Best Practices Pattern
**KAPI Quality Baseline for All Node.js Blueprints**

_Source: [goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices) - 100+ battle-tested practices_

---

## Overview

This document defines the quality baseline that **every KAPI Node.js blueprint must meet**. These practices are extracted from the nodebestpractices repo (100K+ stars) and integrated into our brutal analysis system.

**Purpose**: Ensure all KAPI-generated code follows industry-standard best practices from day one.

---

## 1. Project Architecture (6 Practices)

### 1.1 Structure by Business Components
**Rule**: Root contains business domains (bounded contexts), not technical layers.

```
my-system/
├─ apps/
│  ├─ users/
│  ├─ orders/
│  ├─ payments/
├─ libraries/
│  ├─ logger/
│  ├─ authenticator/
```

**Why**: Autonomous components = less mental overhead, faster development, clearer modularity.

**KAPI Validation**: `❌ Technical folders at root (controllers/, models/, routes/)`

---

### 1.2 Layer Components with 3 Tiers
**Rule**: Each component has dedicated folders for web/entry-point, domain/logic, and data-access.

```
apps/orders/
├─ entry-points/
│  ├─ api/          # Controllers
│  ├─ message-queue/ # Consumers
├─ domain/          # Business logic, DTOs, services
├─ data-access/     # DB calls, no ORM coupling
```

**Why**: Separates technical concerns from pure logic. Makes code accessible from tests, jobs, queues.

**KAPI Validation**: `❌ Controllers calling DB directly`

---

### 1.3 Wrap Utilities as Packages
**Rule**: Reusable modules in dedicated folders with their own `package.json`.

```
libraries/logger/
├─ package.json
├─ src/
│  ├─ index.js
```

**Why**: Encapsulation, future publishing capability, clear public interfaces.

**KAPI Validation**: `❌ Shared code without package.json`

---

### 1.4 Environment-Aware Config
**Rule**: Config reads from files AND environment variables. Use convict, env-var, or zod.

**Requirements**:
- Keys readable from both file and env
- Secrets outside code
- Hierarchical structure
- Typing support
- Validation on startup
- Defaults for all keys

**KAPI Validation**: `❌ No config validation on startup`

---

### 1.5 Choose Framework Thoughtfully
**KAPI Recommendations** (2024):
- **Nest.js**: OOP teams, large-scale apps
- **Fastify**: Microservices, simple Node mechanics
- **Express**: Mature, stable, huge ecosystem
- **Koa**: Lightweight, modern

**KAPI Validation**: `⚠️ Framework choice lacks justification in specs`

---

### 1.6 Use TypeScript Sparingly
**Rule**: Use simple types for variables and function returns. Avoid advanced features unless necessary.

**Why**: [Research shows](https://earlbarr.com/publications/typestudy.pdf) TypeScript catches ~20% of bugs. Tests catch the other 80%. Overuse increases complexity.

**KAPI Validation**: `⚠️ Excessive use of advanced TS features (50+ keywords)`

---

## 2. Error Handling (13 Practices)

### 2.1 Use Async-Await for Error Handling
**Rule**: Always use async-await or promises. Never callback style.

```javascript
// ✅ Do
async function doSomething() {
  try {
    const result = await fetch();
    return result;
  } catch (error) {
    throw new AppError('Failed', error);
  }
}

// ❌ Avoid
function doSomething(callback) {
  fetch((err, result) => {
    if (err) callback(err);
    callback(null, result);
  });
}
```

**KAPI Validation**: `❌ Callback-style error handling found`

---

### 2.2 Extend Built-in Error Object
**Rule**: All errors extend Error. Use consistent properties: name, message, isCatastrophic, code.

```javascript
class AppError extends Error {
  constructor(message, code, isCatastrophic = false) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.isCatastrophic = isCatastrophic;
  }
}
```

**KAPI Validation**: `❌ Throwing strings or plain objects`

---

### 2.3 Distinguish Operational vs Catastrophic Errors
**Rule**: 
- **Operational**: Known, handled (invalid input, timeout)
- **Catastrophic**: Unknown, restart required (undefined function, syntax error)

**KAPI Validation**: `❌ No error classification strategy`

---

### 2.4 Handle Errors Centrally
**Rule**: Single error handler for logging, metrics, crash decisions.

```javascript
// Centralized handler
class ErrorHandler {
  handle(error) {
    logger.error(error);
    metrics.increment('errors');
    if (error.isCatastrophic) process.exit(1);
  }
}
```

**KAPI Validation**: `❌ Error handling scattered across codebase`

---

### 2.5 Document API Errors with OpenAPI/GraphQL
**Rule**: API consumers must know possible errors.

**KAPI Validation**: `❌ No error documentation in API specs`

---

### 2.6 Exit Gracefully on Unknown Errors
**Rule**: Crash process on catastrophic errors. Let orchestrator restart.

**KAPI Validation**: `❌ Process continues after unknown error`

---

### 2.7 Use Mature Logger (Pino/Winston)
**Rule**: Never console.log in production. Use structured logging.

**Features Required**:
- Log levels (debug, info, warn, error)
- JSON output
- Correlation IDs
- Performance (minimal serialization penalty)

**KAPI Validation**: `❌ console.log found in production code`

---

### 2.8 Test Error Flows
**Rule**: Test both happy paths AND error scenarios.

**KAPI Validation**: `❌ No tests for error handling`

---

### 2.9 Use APM for Error Discovery
**Rule**: Tools like Datadog, New Relic auto-detect errors, slow code, crashes.

**KAPI Validation**: `⚠️ No APM integration`

---

### 2.10 Catch Unhandled Promise Rejections
**Rule**: Subscribe to `process.unhandledRejection`.

```javascript
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection', { reason, promise });
  process.exit(1);
});
```

**KAPI Validation**: `❌ No unhandledRejection handler`

---

### 2.11 Validate Arguments with Dedicated Library
**Rule**: Use ajv, zod, or typebox for input validation.

**KAPI Validation**: `❌ Manual validation without library`

---

### 2.12 Always Await Before Returning
**Rule**: `return await promise` for full stack traces.

```javascript
// ✅ Do
async function getData() {
  return await fetch(); // Full stack trace
}

// ❌ Avoid
async function getData() {
  return fetch(); // Missing frames in stack
}
```

**KAPI Validation**: `❌ Returning promises without await`

---

### 2.13 Subscribe to EventEmitter Errors
**Rule**: EventEmitters don't throw, they emit 'error'.

```javascript
emitter.on('error', (err) => {
  errorHandler.handle(err);
});
```

**KAPI Validation**: `❌ EventEmitter without error handler`

---

## 3. Code Style (13 Practices)

### 3.1 Use ESLint + Prettier
**Rule**: Mandatory linting on every commit.

**KAPI Validation**: `❌ No ESLint config`

---

### 3.2 Node.js ESLint Plugins
**Required Plugins**:
- eslint-plugin-node
- eslint-plugin-security
- eslint-plugin-jest/mocha

**KAPI Validation**: `❌ Missing security plugin`

---

### 3.3-3.5 Basic Style Rules
- Curly braces on same line
- Proper statement separation
- Named functions (no anonymous)

**KAPI Validation**: Via ESLint config

---

### 3.6 Naming Conventions
- `lowerCamelCase`: variables, functions
- `UpperCamelCase`: classes
- `UPPER_SNAKE_CASE`: constants, globals

**KAPI Validation**: `❌ Inconsistent naming`

---

### 3.7 Prefer const > let, Avoid var
**Rule**: `const` by default. `let` only when reassignment needed.

**KAPI Validation**: `❌ var usage found`

---

### 3.8 Require Modules First
**Rule**: All imports at file top, before functions.

**KAPI Validation**: `❌ require() inside functions`

---

### 3.9 Explicit Module Entry Point
**Rule**: Use `index.js` or `package.json.main` to expose public interface.

**KAPI Validation**: `❌ Deep imports bypassing module interface`

---

### 3.10-3.12 Modern JS
- Use `===` not `==`
- Prefer async-await over callbacks
- Use arrow functions

**KAPI Validation**: Via ESLint rules

---

### 3.13 Avoid Side Effects Outside Functions
**Rule**: No code execution at module load (except exports).

**KAPI Validation**: `❌ DB/network calls at top level`

---

## 4. Testing (13 Practices)

### 4.1 Write API (Component) Tests
**Rule**: Minimum viable testing = API-level tests.

**Why**: More coverage than unit tests, easier to write.

**KAPI Validation**: `❌ No API tests found`

---

### 4.2 Test Names: 3 Parts
**Format**: `[UnitUnderTest] [Scenario] [ExpectedResult]`

**Example**: `POST /users - valid data - returns 201 and user object`

**KAPI Validation**: `❌ Unclear test names`

---

### 4.3 AAA Pattern
**Structure**:
1. **Arrange**: Setup
2. **Act**: Execute
3. **Assert**: Verify

**KAPI Validation**: `❌ Tests not structured as AAA`

---

### 4.4 Unified Node Version
**Rule**: Use nvm/Volta. Specify version in `.nvmrc`.

**KAPI Validation**: `❌ No Node version specified`

---

### 4.5 No Global Test Fixtures
**Rule**: Each test creates its own data. No shared state.

**KAPI Validation**: `❌ Tests depend on shared fixtures`

---

### 4.6 Tag Tests
**Rule**: Tag for different scenarios (#sanity, #integration, #e2e).

**KAPI Validation**: `⚠️ No test categorization`

---

### 4.7 Check Test Coverage
**Rule**: Use Istanbul/NYC. Fail build if < 80%.

**KAPI Validation**: `❌ Coverage below 80%`

---

### 4.8 Production-like E2E Environment
**Rule**: E2E tests use Docker Compose with real DB.

**KAPI Validation**: `❌ E2E tests use mocks instead of real services`

---

### 4.9 Static Analysis Tools
**Rule**: SonarQube or Code Climate in CI.

**KAPI Validation**: `⚠️ No static analysis`

---

### 4.10 Mock External HTTP Services
**Rule**: Use nock/Mock-Server. Test error scenarios.

**KAPI Validation**: `❌ Tests hit real external APIs`

---

### 4.11 Test Middlewares in Isolation
**Rule**: Stub {req, res, next} objects.

**KAPI Validation**: `❌ Middleware tests require full app`

---

### 4.12 Randomize Port in Tests
**Rule**: Use port 0 to avoid collisions.

**KAPI Validation**: `❌ Hardcoded test port`

---

### 4.13 Test Five Outcomes
**Categories**:
1. Response
2. State change (DB)
3. Outgoing API call
4. Message queue
5. Observability (logs, metrics)

**KAPI Validation**: `❌ Only testing response, ignoring side effects`

---

## 5. Production (19 Practices)

### 5.1 Monitoring is Strategic
**Must Monitor**:
- Uptime
- User-facing metrics
- Node.js metrics (event loop lag)
- Distributed traces (OpenTelemetry)
- Logs

**KAPI Validation**: `❌ No monitoring configured`

---

### 5.2 Smart Logging
**Requirements**:
- Structured (JSON)
- Correlation IDs
- Log levels
- Performance-conscious

**KAPI Validation**: `❌ Unstructured logging`

---

### 5.3 Delegate to Reverse Proxy
**Rule**: Nginx/HAProxy handles gzip, SSL, static files.

**KAPI Validation**: `⚠️ Node handling infrastructure concerns`

---

### 5.4 Lock Dependencies
**Rule**: Commit `package-lock.json`.

**KAPI Validation**: `❌ No lockfile in repo`

---

### 5.5 Process Uptime Tools
**Rule**: Docker/K8s handles restarts. Avoid PM2 in containers.

**KAPI Validation**: `❌ PM2 in Dockerized app`

---

### 5.6 Utilize All CPU Cores
**Rule**: Replicate instances across cores.

**KAPI Validation**: `⚠️ Single instance, underutilized CPUs`

---

### 5.7 Maintenance Endpoint
**Rule**: `/health` endpoint with system info.

**KAPI Validation**: `❌ No health check endpoint`

---

### 5.8 APM Products
**Rule**: Use Datadog, New Relic, or equivalent.

**KAPI Validation**: `⚠️ No APM integration`

---

### 5.9 Production-Ready Code
**Checklist**:
- Config from env
- Graceful shutdown
- Error handling
- Logging
- Monitoring

**KAPI Validation**: Comprehensive checks

---

### 5.10 Guard Memory Usage
**Rule**: Monitor with APM. Set limits.

**KAPI Validation**: `⚠️ No memory monitoring`

---

### 5.11 Frontend Assets Out of Node
**Rule**: Serve via CDN/nginx, not Node.

**KAPI Validation**: `⚠️ Node serving static files`

---

### 5.12 Strive for Stateless
**Rule**: No in-process sessions, cache, or files.

**KAPI Validation**: `❌ Stateful session storage`

---

### 5.13 Vulnerability Scanning
**Rule**: npm audit, Snyk in CI.

**KAPI Validation**: `❌ No vulnerability scanning`

---

### 5.14 Transaction IDs
**Rule**: AsyncLocalStorage for correlation IDs.

**KAPI Validation**: `❌ No correlation ID system`

---

### 5.15 Set NODE_ENV=production
**Rule**: Enables framework optimizations.

**KAPI Validation**: `❌ NODE_ENV not set`

---

### 5.16 Automated Zero-Downtime Deploys
**Rule**: Blue-green or rolling deployments.

**KAPI Validation**: `⚠️ Manual deployment process`

---

### 5.17 Use LTS Node Version
**Rule**: Even-numbered versions (18, 20, 22).

**KAPI Validation**: `❌ Non-LTS Node version`

---

### 5.18 Log to stdout
**Rule**: Let infrastructure route logs.

**KAPI Validation**: `❌ Hardcoded log destinations`

---

### 5.19 Install with npm ci
**Rule**: Production uses `npm ci`, not `npm install`.

**KAPI Validation**: `❌ Deployment uses npm install`

---

## 6. Security (27 Practices)

### 6.1 Linter Security Rules
**Rule**: eslint-plugin-security in every project.

**KAPI Validation**: `❌ No security linting`

---

### 6.2 Rate Limiting
**Rule**: Use nginx, cloud firewall, or rate-limiter-flexible.

**KAPI Validation**: `❌ No rate limiting configured`

---

### 6.3 Extract Secrets from Code
**Rule**: Use Vault, K8s Secrets, or env vars. Never hardcode.

**KAPI Validation**: `❌ Secrets in source code`

---

### 6.4 Prevent Query Injection
**Rule**: Use ORM/ODM with parameterized queries.

**KAPI Validation**: `❌ String concatenation in queries`

---

### 6.5 Generic Security Practices
**Checklist**:
- HTTPS everywhere
- Secure cookies
- CSRF protection
- Input validation

**KAPI Validation**: Comprehensive checks

---

### 6.6 Secure HTTP Headers
**Rule**: Use Helmet middleware.

```javascript
const helmet = require('helmet');
app.use(helmet());
```

**KAPI Validation**: `❌ No helmet middleware`

---

### 6.7 Scan Dependencies
**Rule**: npm audit / Snyk in CI.

**KAPI Validation**: `❌ No dependency scanning`

---

### 6.8 Hash Passwords with bcrypt/scrypt
**Rule**: Never plain text or weak hashing.

**KAPI Validation**: `❌ Weak password hashing`

---

### 6.9 Escape HTML/JS/CSS Output
**Rule**: Prevent XSS with proper encoding.

**KAPI Validation**: `❌ Unescaped user input in templates`

---

### 6.10 Validate JSON Schemas
**Rule**: Use jsonschema, joi, or zod.

**KAPI Validation**: `❌ No input validation`

---

### 6.11 JWT Blocklisting
**Rule**: Revoke tokens when needed.

**KAPI Validation**: `⚠️ No JWT revocation strategy`

---

### 6.12 Prevent Brute Force
**Rule**: Limit login attempts by IP and user.

**KAPI Validation**: `❌ No login rate limiting`

---

### 6.13 Run as Non-Root
**Rule**: Docker USER directive.

```dockerfile
USER node
```

**KAPI Validation**: `❌ Container runs as root`

---

### 6.14 Limit Payload Size
**Rule**: Nginx or body-parser limits.

**KAPI Validation**: `❌ No payload limits`

---

### 6.15 Avoid eval()
**Rule**: Never use eval, new Function, or dynamic requires.

**KAPI Validation**: `❌ eval() usage found`

---

### 6.16-6.27 Additional Security
- Safe RegEx (no ReDoS)
- Avoid module loading with variables
- Sandbox unsafe code
- Child process safety
- Hide error details from clients
- 2FA for npm
- Secure session settings
- DOS attack prevention
- Safe redirects
- No secrets in npm registry
- Inspect outdated packages
- Use node: protocol for built-ins

**KAPI Validation**: Individual checks for each

---

## 7. Docker (15 Practices)

### 7.1 Multi-Stage Builds
**Rule**: Separate build and runtime stages.

```dockerfile
FROM node:20 AS build
COPY . .
RUN npm ci && npm run build

FROM node:20-slim
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm ci --production
CMD ["node", "dist/index.js"]
```

**KAPI Validation**: `❌ Single-stage Dockerfile`

---

### 7.2 Bootstrap with node, Not npm
**Rule**: `CMD ["node", "app.js"]` not `npm start`.

**Why**: npm doesn't pass signals to Node.

**KAPI Validation**: `❌ Using npm start in container`

---

### 7.3 Let Orchestrator Handle Restarts
**Rule**: No PM2/cluster in K8s/Docker Swarm.

**KAPI Validation**: `❌ PM2 in orchestrated environment`

---

### 7.4 Use .dockerignore
**Rule**: Exclude secrets, node_modules, .git.

**KAPI Validation**: `❌ No .dockerignore`

---

### 7.5 Clean Dependencies
**Rule**: `npm ci --production` in final stage.

**KAPI Validation**: `❌ Dev dependencies in production image`

---

### 7.6 Graceful Shutdown
**Rule**: Handle SIGTERM, close connections.

**KAPI Validation**: `❌ No SIGTERM handler`

---

### 7.7 Set Memory Limits
**Rule**: Docker limits + V8 `--max-old-space`.

**KAPI Validation**: `❌ No memory limits configured`

---

### 7.8 Efficient Caching
**Rule**: COPY package*.json before COPY . to cache npm install.

**KAPI Validation**: `❌ Inefficient layer caching`

---

### 7.9 Explicit Image Tags
**Rule**: Never use `latest`. Use SHA256 digests.

**KAPI Validation**: `❌ Using latest tag`

---

### 7.10 Smaller Base Images
**Rule**: Prefer Alpine or slim variants.

**KAPI Validation**: `⚠️ Using full Node image`

---

### 7.11 Clean Build-Time Secrets
**Rule**: Multi-stage build or BuildKit secrets.

**KAPI Validation**: `❌ Secrets in Docker history`

---

### 7.12 Scan Images
**Rule**: Trivy, Snyk, or Clair in CI.

**KAPI Validation**: `❌ No image scanning`

---

### 7.13 Clean NODE_MODULE Cache
**Rule**: Remove .npm cache after install.

```dockerfile
RUN npm ci --production && npm cache clean --force
```

**KAPI Validation**: `⚠️ Unnecessary cache in image`

---

### 7.14-7.15 Generic Docker + Linting
- Follow general Docker best practices
- Lint Dockerfile with hadolint

**KAPI Validation**: Individual checks

---

## 8. Performance (2 Practices)

### 8.1 Don't Block Event Loop
**Rule**: Offload CPU-intensive work to worker threads or separate services.

**KAPI Validation**: `⚠️ CPU-intensive operations on main thread`

---

### 8.2 Prefer Native Methods
**Rule**: Built-in JS > Lodash for performance.

**KAPI Validation**: `⚠️ Overuse of utility libraries`

---

## KAPI Integration

### Brutal Analysis Checks

**P0 (Critical - Block Deployment)**:
- ❌ No helmet middleware
- ❌ Secrets in code
- ❌ SQL injection risk
- ❌ No error handling
- ❌ console.log in production
- ❌ No tests
- ❌ Container runs as root
- ❌ Using npm install instead of npm ci

**P1 (High - Warn)**:
- ⚠️ No APM integration
- ⚠️ Coverage < 80%
- ⚠️ No static analysis
- ⚠️ PM2 in containers
- ⚠️ No monitoring

**P2 (Medium - Suggest)**:
- ℹ️ Missing JSDoc
- ℹ️ No TypeScript
- ℹ️ Could use smaller Docker image

### Blueprint Generation

Every KAPI blueprint includes:
1. **ESLint config** with security plugins
2. **Prettier** for formatting
3. **.dockerignore** and optimized Dockerfile
4. **Test setup** with coverage requirements
5. **Error handling** middleware
6. **Logging** with Pino
7. **Health check** endpoint
8. **Environment validation** on startup

### Living Specifications

Blueprints document which practices are implemented:
```markdown
## Best Practices Compliance

✅ 1.1 Structure by components
✅ 2.7 Pino logger configured
✅ 4.1 API tests with 85% coverage
✅ 6.6 Helmet middleware
✅ 7.1 Multi-stage Docker build
⚠️  5.8 APM - manual setup required
```

---

## Quick Reference Checklist

### Essential (Must Have)
- [ ] Component-based structure
- [ ] ESLint + security plugins
- [ ] Async-await error handling
- [ ] Central error handler
- [ ] Pino/Winston logger
- [ ] Input validation (zod/joi)
- [ ] Helmet middleware
- [ ] ORM for DB queries
- [ ] API tests with AAA pattern
- [ ] 80%+ test coverage
- [ ] package-lock.json committed
- [ ] Multi-stage Dockerfile
- [ ] .dockerignore
- [ ] Non-root user in container
- [ ] Health check endpoint

### Important (Should Have)
- [ ] TypeScript with simple types
- [ ] Config validation on startup
- [ ] APM integration
- [ ] Correlation IDs
- [ ] Rate limiting
- [ ] JWT with revocation
- [ ] Dependency scanning
- [ ] Image scanning
- [ ] Graceful shutdown
- [ ] Memory limits

### Nice to Have
- [ ] Static analysis (SonarQube)
- [ ] E2E tests
- [ ] Blue-green deployments
- [ ] Alpine base images
- [ ] Worker threads for CPU work

---

## Further Reading

- **Full Guide**: https://github.com/goldbergyoni/nodebestpractices
- **Testing Guide**: https://github.com/goldbergyoni/javascript-testing-best-practices
- **Practica.js Example**: https://github.com/practicajs/practica
- **KAPI Blueprint Catalog**: [../../../docs-new/02-what/product/04-blueprint-catalog.md](../../../docs-new/02-what/product/04-blueprint-catalog.md)

---

**Last Updated**: January 2025  
**Maintained by**: KAPI Team  
**Source Version**: nodebestpractices@July-2024
