# C#/.NET Best Practices Pattern

**KAPI Quality Baseline for C#/.NET Blueprints**

_Based on Jason Taylor Clean Architecture, eShopOnContainers, ASP.NET Core best practices_

## 1. Project Structure (8)
- Clean Architecture layers (Domain, Application, Infrastructure, Web)
- CQRS with MediatR
- Domain at center (no dependencies)
- Feature folders not technical layers
- Shared kernel for cross-cutting
- API/Web separate from core
- Tests mirror source structure
- Solution folder organization

## 2. ASP.NET Core (12)
- Minimal APIs or Controllers (consistent choice)
- Dependency injection via IServiceCollection
- Configuration from appsettings.json + env
- Options pattern for settings
- Middleware pipeline order
- ActionResult<T> return types
- Model validation with DataAnnotations
- Global exception handling
- Health checks (/health, /ready)
- API versioning
- Swagger/OpenAPI generation
- Async/await everywhere

## 3. Entity Framework Core (10)
- Code-first with migrations
- DbContext per bounded context
- Fluent API over attributes
- Value objects for DDD
- Soft deletes with query filters
- Optimistic concurrency (RowVersion)
- AsNoTracking for read-only
- Include() to avoid N+1
- Connection resiliency
- Database indexes on foreign keys

## 4. Security (15)
- ASP.NET Core Identity
- IdentityServer/Duende for OAuth
- Password hashing (built-in)
- JWT Bearer authentication
- Policy-based authorization
- CORS explicit origins
- Anti-forgery tokens
- Input validation (FluentValidation)
- SQL injection prevention (EF)
- HTTPS enforcement
- Security headers middleware
- Rate limiting
- Secrets in User Secrets/Azure KeyVault
- Dependency scanning (Dependabot)
- OWASP ZAP for pen testing

## 5. Testing (12)
- xUnit preferred
- Test coverage > 80%
- Unit tests (domain + application)
- Integration tests (WebApplicationFactory)
- Repository tests (in-memory provider)
- FluentAssertions
- Moq for mocking
- AutoFixture for test data
- Respawn for database cleanup
- Test containers for real DB
- BDD with SpecFlow (optional)
- Mutation testing (Stryker)

## 6. Code Quality (10)
- StyleCop/Roslyn analyzers
- EditorConfig for consistency
- Nullable reference types enabled
- C# latest features
- SOLID principles
- DRY via extension methods
- Async suffix for async methods
- IDisposable with using
- Avoid magic strings (constants)
- Records for DTOs

## 7. Production (14)
- Serilog structured logging
- Application Insights/Seq
- Health checks with dependencies
- Graceful shutdown
- Connection pooling (default)
- Background services (IHostedService)
- Response caching
- Output caching (.NET 7+)
- Distributed caching (Redis)
- Circuit breakers (Polly)
- Retry policies with exponential backoff
- Correlation IDs
- Exception logging
- Performance counters

## 8. Docker (8)
- Multi-stage builds
- ASP.NET runtime (not SDK)
- Non-root user
- .dockerignore
- HEALTHCHECK directive
- Environment variables
- Layer caching (restore before build)
- Trivy scanning

## KAPI Validation

**P0**: No authentication, plain passwords, SQL injection, no tests, root user, no migrations
**P1**: Coverage <80%, no health checks, field injection, no logging, sync methods
**P2**: No caching, no analyzers, no rate limiting, basic DTOs

## Blueprint Includes

1. Clean Architecture template
2. MediatR + FluentValidation
3. EF Core + migrations
4. Identity + JWT
5. Serilog + App Insights
6. xUnit + FluentAssertions
7. Health checks
8. Swagger/OpenAPI
9. Docker multi-stage
10. Global exception handler

## References
- https://github.com/jasontaylordev/CleanArchitecture
- https://github.com/dotnet-architecture/eShopOnContainers
- https://learn.microsoft.com/aspnet/core
- https://github.com/ardalis/CleanArchitecture

---

**Last Updated**: January 2025
