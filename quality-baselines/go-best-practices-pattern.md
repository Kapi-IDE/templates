# Go Best Practices Pattern
**KAPI Quality Baseline for All Go Blueprints**

_Based on golang-standards/project-layout, go-clean-template, and Wild Workouts DDD_

---

## Overview

Quality baseline for production-ready Go applications in KAPI blueprints.

---

## 1. Project Structure (8 Practices)

### 1.1 Standard Go Project Layout
**Rule**: Follow golang-standards/project-layout conventions.

```
myapp/
├── cmd/
│   └── myapp/
│       └── main.go
├── internal/
│   ├── domain/
│   ├── handler/
│   ├── repository/
│   └── service/
├── pkg/
│   └── shared/
├── api/
│   └── openapi.yaml
├── configs/
├── scripts/
├── build/
├── deployments/
└── test/
```

**KAPI Validation**: `❌ Non-standard directory structure`

---

### 1.2 Use internal/ for Private Code
**Rule**: Code in `internal/` can't be imported by external projects.

**KAPI Validation**: `❌ Business logic in pkg/`

---

### 1.3 cmd/ for Application Entry Points
**Rule**: One directory per executable under `cmd/`.

```
cmd/
├── api-server/
│   └── main.go
├── worker/
│   └── main.go
└── migration/
    └── main.go
```

**KAPI Validation**: `❌ Multiple main.go at root`

---

### 1.4 Domain-Driven Directory Organization
**Rule**: Organize by domain/feature, not technical layer.

```
internal/
├── orders/
│   ├── handler.go
│   ├── service.go
│   ├── repository.go
│   └── models.go
├── users/
└── payments/
```

**KAPI Validation**: `❌ handlers/, services/, repositories/ at root`

---

### 1.5 pkg/ for Reusable Libraries
**Rule**: Only truly reusable code goes in `pkg/`.

**KAPI Validation**: `❌ Domain logic in pkg/`

---

### 1.6 configs/ for Configuration Files
**Rule**: Config templates and defaults in dedicated directory.

**KAPI Validation**: `⚠️ Config files scattered`

---

### 1.7 scripts/ for Build/Deploy Scripts
**Rule**: Makefile, shell scripts, build tools.

**KAPI Validation**: `⚠️ Scripts at project root`

---

### 1.8 api/ for API Definitions
**Rule**: OpenAPI/Swagger specs, Protocol Buffers.

**KAPI Validation**: `⚠️ No API documentation`

---

## 2. Error Handling (10 Practices)

### 2.1 Always Check Errors
**Rule**: Never ignore errors. Handle or return.

```go
// ✅ Do
result, err := doSomething()
if err != nil {
    return nil, fmt.Errorf("failed to do something: %w", err)
}

// ❌ Avoid
result, _ := doSomething()
```

**KAPI Validation**: `❌ Unchecked errors (go vet)`

---

### 2.2 Wrap Errors with Context
**Rule**: Use `fmt.Errorf` with `%w` for error chains.

**KAPI Validation**: `❌ Error wrapping without %w`

---

### 2.3 Custom Error Types
**Rule**: Domain-specific errors with context.

```go
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}
```

**KAPI Validation**: `⚠️ Generic errors only`

---

### 2.4 Sentinel Errors
**Rule**: Package-level errors for known conditions.

```go
var (
    ErrNotFound = errors.New("not found")
    ErrInvalidInput = errors.New("invalid input")
)
```

**KAPI Validation**: `⚠️ String comparison for errors`

---

### 2.5 Don't Panic in Libraries
**Rule**: Only panic for unrecoverable errors. Return errors.

**KAPI Validation**: `❌ panic() in business logic`

---

### 2.6 Use errors.Is and errors.As
**Rule**: Check error types properly.

```go
if errors.Is(err, ErrNotFound) {
    // handle not found
}

var notFoundErr *NotFoundError
if errors.As(err, &notFoundErr) {
    // handle typed error
}
```

**KAPI Validation**: `❌ Direct error comparison`

---

### 2.7 Defer for Cleanup
**Rule**: Always use defer for resource cleanup.

```go
file, err := os.Open("file.txt")
if err != nil {
    return err
}
defer file.Close()
```

**KAPI Validation**: `❌ Missing defer for resources`

---

### 2.8 Log Errors with Context
**Rule**: Include request ID, user ID in error logs.

**KAPI Validation**: `❌ No context in error logs`

---

### 2.9 Error Response Standards
**Rule**: Consistent error JSON format.

```go
type ErrorResponse struct {
    Code    string `json:"code"`
    Message string `json:"message"`
    Details any    `json:"details,omitempty"`
}
```

**KAPI Validation**: `❌ Inconsistent error responses`

---

### 2.10 Graceful Degradation
**Rule**: Handle partial failures in distributed systems.

**KAPI Validation**: `⚠️ No fallback strategies`

---

## 3. Code Quality (12 Practices)

### 3.1 gofmt and goimports
**Rule**: Auto-format all code.

**KAPI Validation**: `❌ Unformatted code`

---

### 3.2 golangci-lint
**Rule**: Run comprehensive linting in CI.

```yaml
linters:
  enable:
    - errcheck
    - gosec
    - govet
    - staticcheck
    - unused
```

**KAPI Validation**: `❌ No linting configured`

---

### 3.3 Package Comments
**Rule**: Every package has doc comment.

```go
// Package orders handles order processing and fulfillment.
package orders
```

**KAPI Validation**: `❌ Missing package docs`

---

### 3.4 Exported Names Documentation
**Rule**: All exported types, functions documented.

**KAPI Validation**: `❌ Undocumented exports`

---

### 3.5 Interface Naming
**Rule**: Single-method interfaces end in -er.

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

**KAPI Validation**: `⚠️ Non-standard interface names`

---

### 3.6 Minimal Interfaces
**Rule**: Accept interfaces, return structs.

**KAPI Validation**: `⚠️ Large interfaces (>3 methods)`

---

### 3.7 Avoid init() Side Effects
**Rule**: No global state in init().

**KAPI Validation**: `❌ Database connections in init()`

---

### 3.8 Context as First Parameter
**Rule**: `ctx context.Context` always first param.

**KAPI Validation**: `❌ Context not first parameter`

---

### 3.9 Use Named Return Values Sparingly
**Rule**: Only for documentation, not control flow.

**KAPI Validation**: `⚠️ Overuse of named returns`

---

### 3.10 Avoid Naked Returns
**Rule**: Always explicit return values.

**KAPI Validation**: `❌ Naked returns in long functions`

---

### 3.11 Table-Driven Tests
**Rule**: Use subtests for multiple scenarios.

```go
tests := []struct {
    name    string
    input   int
    want    int
    wantErr bool
}{
    {"positive", 5, 10, false},
    {"zero", 0, 0, true},
}
```

**KAPI Validation**: `⚠️ No table-driven tests`

---

### 3.12 golangci-lint in CI
**Rule**: Fail builds on lint errors.

**KAPI Validation**: `❌ Linting not enforced`

---

## 4. Concurrency (8 Practices)

### 4.1 Use Channels for Communication
**Rule**: Don't communicate by sharing memory; share memory by communicating.

**KAPI Validation**: `⚠️ Excessive mutex usage`

---

### 4.2 Always Close Channels
**Rule**: Producer closes channels, not consumer.

**KAPI Validation**: `❌ Unclosed channels`

---

### 4.3 Use Context for Cancellation
**Rule**: Propagate cancellation with context.

```go
func process(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case <-time.After(time.Second):
        // work
    }
}
```

**KAPI Validation**: `❌ No context cancellation`

---

### 4.4 WaitGroup for Goroutine Coordination
**Rule**: Use sync.WaitGroup for parallel work.

**KAPI Validation**: `❌ Goroutines without coordination`

---

### 4.5 Avoid Goroutine Leaks
**Rule**: Every goroutine must have exit condition.

**KAPI Validation**: `❌ Infinite goroutines`

---

### 4.6 errgroup for Error Handling
**Rule**: Use golang.org/x/sync/errgroup for parallel errors.

**KAPI Validation**: `⚠️ Manual goroutine error handling`

---

### 4.7 Buffered Channels for Non-Blocking
**Rule**: Buffer size = expected concurrent senders.

**KAPI Validation**: `⚠️ Unbuffered channels causing deadlocks`

---

### 4.8 Mutex for Shared State
**Rule**: sync.RWMutex when reads >> writes.

**KAPI Validation**: `❌ Data races (go test -race)`

---

## 5. Testing (11 Practices)

### 5.1 Test Coverage > 80%
**Rule**: Enforce with go test -cover.

**KAPI Validation**: `❌ Coverage below 80%`

---

### 5.2 Table-Driven Tests
**Rule**: Use t.Run() with subtests.

**KAPI Validation**: `⚠️ Repetitive test code`

---

### 5.3 Test Fixtures in testdata/
**Rule**: Test files in testdata/ directory.

**KAPI Validation**: `⚠️ Test files scattered`

---

### 5.4 Use testing.T Helper Functions
**Rule**: Mark helper functions with t.Helper().

**KAPI Validation**: `⚠️ Missing t.Helper() calls`

---

### 5.5 Mock External Dependencies
**Rule**: Use interfaces for testability.

**KAPI Validation**: `❌ Tests hitting real APIs`

---

### 5.6 Test Race Detector
**Rule**: Run go test -race in CI.

**KAPI Validation**: `❌ No race detection`

---

### 5.7 Benchmark Critical Paths
**Rule**: Benchmark functions start with Benchmark.

**KAPI Validation**: `⚠️ No performance benchmarks`

---

### 5.8 Integration Tests Build Tag
**Rule**: Use `//go:build integration` tag.

**KAPI Validation**: `⚠️ Integration tests run always`

---

### 5.9 Example Tests for Documentation
**Rule**: Example functions in _test.go files.

**KAPI Validation**: `⚠️ No example tests`

---

### 5.10 testify for Assertions
**Rule**: Use github.com/stretchr/testify/assert.

**KAPI Validation**: `⚠️ Manual error checking in tests`

---

### 5.11 Golden Files for Complex Output
**Rule**: Store expected output in testdata/golden/.

**KAPI Validation**: `⚠️ Large inline test expectations`

---

## 6. Security (15 Practices)

### 6.1 Input Validation
**Rule**: Validate all external input.

**KAPI Validation**: `❌ No input validation`

---

### 6.2 gosec Security Linter
**Rule**: Run gosec in CI pipeline.

**KAPI Validation**: `❌ No security scanning`

---

### 6.3 No Hardcoded Secrets
**Rule**: Use environment variables or secret managers.

**KAPI Validation**: `❌ Secrets in code`

---

### 6.4 SQL Injection Prevention
**Rule**: Always use parameterized queries.

```go
// ✅ Do
rows, err := db.Query("SELECT * FROM users WHERE id = $1", userID)

// ❌ Never
query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)
```

**KAPI Validation**: `❌ String formatting in SQL`

---

### 6.5 Password Hashing
**Rule**: Use bcrypt or argon2.

**KAPI Validation**: `❌ Weak password hashing`

---

### 6.6 TLS Configuration
**Rule**: Minimum TLS 1.2, strong ciphers.

**KAPI Validation**: `❌ Weak TLS config`

---

### 6.7 CORS Configuration
**Rule**: Explicit allowed origins.

**KAPI Validation**: `❌ CORS AllowAllOrigins = true`

---

### 6.8 Rate Limiting
**Rule**: Use tollbooth or custom middleware.

**KAPI Validation**: `❌ No rate limiting`

---

### 6.9 JWT Security
**Rule**: Short expiration, secure signing algorithm.

**KAPI Validation**: `❌ Long-lived JWT tokens`

---

### 6.10 Dependency Scanning
**Rule**: govulncheck in CI.

**KAPI Validation**: `❌ No vulnerability scanning`

---

### 6.11 Secure HTTP Headers
**Rule**: CSP, X-Frame-Options, HSTS.

**KAPI Validation**: `❌ Missing security headers`

---

### 6.12 Context Timeout Enforcement
**Rule**: All external calls have timeouts.

**KAPI Validation**: `❌ No request timeouts`

---

### 6.13 Limit Request Body Size
**Rule**: http.MaxBytesReader for uploads.

**KAPI Validation**: `❌ No body size limits`

---

### 6.14 Path Traversal Prevention
**Rule**: Validate file paths with filepath.Clean.

**KAPI Validation**: `❌ Unsafe file operations`

---

### 6.15 Run as Non-Root
**Rule**: Docker USER directive.

**KAPI Validation**: `❌ Container runs as root`

---

## 7. Performance (8 Practices)

### 7.1 Use sync.Pool for Temporary Objects
**Rule**: Pool frequently allocated objects.

**KAPI Validation**: `⚠️ Excessive allocations`

---

### 7.2 Avoid Premature String Concatenation
**Rule**: Use strings.Builder for loops.

```go
var sb strings.Builder
for _, s := range items {
    sb.WriteString(s)
}
```

**KAPI Validation**: `⚠️ String concat in loops`

---

### 7.3 Benchmark Before Optimizing
**Rule**: Measure with pprof before changes.

**KAPI Validation**: `⚠️ No baseline benchmarks`

---

### 7.4 Connection Pooling
**Rule**: Reuse database/HTTP connections.

**KAPI Validation**: `❌ New connection per request`

---

### 7.5 Use Context for Timeouts
**Rule**: context.WithTimeout for external calls.

**KAPI Validation**: `❌ No timeout enforcement`

---

### 7.6 Limit Goroutines
**Rule**: Worker pools for bounded concurrency.

**KAPI Validation**: `⚠️ Unbounded goroutine creation`

---

### 7.7 Pre-Allocate Slices
**Rule**: make([]T, 0, expectedSize) when size known.

**KAPI Validation**: `⚠️ Frequent slice reallocation`

---

### 7.8 Avoid Reflection in Hot Paths
**Rule**: Use code generation instead.

**KAPI Validation**: `⚠️ Reflection in request handlers`

---

## 8. Production (14 Practices)

### 8.1 Structured Logging
**Rule**: Use zap or zerolog with JSON output.

**KAPI Validation**: `❌ log.Printf in production`

---

### 8.2 Metrics with Prometheus
**Rule**: Instrument with prometheus/client_golang.

**KAPI Validation**: `⚠️ No metrics collection`

---

### 8.3 Health Check Endpoint
**Rule**: /health with dependency checks.

```go
http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
    if err := db.Ping(r.Context()); err != nil {
        w.WriteHeader(http.StatusServiceUnavailable)
        return
    }
    w.WriteHeader(http.StatusOK)
})
```

**KAPI Validation**: `❌ No health endpoint`

---

### 8.4 Graceful Shutdown
**Rule**: Handle SIGTERM, close connections.

```go
srv := &http.Server{Addr: ":8080"}
go func() {
    srv.ListenAndServe()
}()

quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGTERM, syscall.SIGINT)
<-quit

ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
srv.Shutdown(ctx)
```

**KAPI Validation**: `❌ No graceful shutdown`

---

### 8.5 Configuration via Environment
**Rule**: Use viper or envconfig.

**KAPI Validation**: `❌ Hardcoded configuration`

---

### 8.6 Database Migration Tool
**Rule**: Use golang-migrate or goose.

**KAPI Validation**: `❌ No migration system`

---

### 8.7 Tracing with OpenTelemetry
**Rule**: Distributed tracing for microservices.

**KAPI Validation**: `⚠️ No distributed tracing`

---

### 8.8 Request ID Propagation
**Rule**: Generate and log request IDs.

**KAPI Validation**: `❌ No request correlation`

---

### 8.9 Dependency Management
**Rule**: Use go.mod and go.sum.

**KAPI Validation**: `❌ No go.sum committed`

---

### 8.10 Versioned Releases
**Rule**: Semantic versioning with git tags.

**KAPI Validation**: `⚠️ No version tags`

---

### 8.11 Circuit Breaker Pattern
**Rule**: Use gobreaker for external services.

**KAPI Validation**: `⚠️ No circuit breakers`

---

### 8.12 Retry Logic with Backoff
**Rule**: Exponential backoff for failures.

**KAPI Validation**: `❌ No retry mechanism`

---

### 8.13 Resource Limits
**Rule**: Set GOMAXPROCS, memory limits.

**KAPI Validation**: `⚠️ No resource constraints`

---

### 8.14 Profiling Endpoints
**Rule**: pprof endpoints for debugging.

**KAPI Validation**: `⚠️ No profiling available`

---

## 9. Docker (10 Practices)

### 9.1 Multi-Stage Builds
**Rule**: Separate build and runtime images.

```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/server

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/server /server
USER nobody
ENTRYPOINT ["/server"]
```

**KAPI Validation**: `❌ Single-stage build`

---

### 9.2 Minimal Base Image
**Rule**: Use scratch or alpine.

**KAPI Validation**: `⚠️ Large base image`

---

### 9.3 Static Binary
**Rule**: CGO_ENABLED=0 for portability.

**KAPI Validation**: `❌ Dynamic linking`

---

### 9.4 Non-Root User
**Rule**: Use USER nobody.

**KAPI Validation**: `❌ Running as root`

---

### 9.5 .dockerignore
**Rule**: Exclude .git, vendor, test files.

**KAPI Validation**: `❌ No .dockerignore`

---

### 9.6 Health Check
**Rule**: HEALTHCHECK directive.

**KAPI Validation**: `⚠️ No Docker health check`

---

### 9.7 Layer Caching
**Rule**: Copy go.mod before source code.

**KAPI Validation**: `❌ Inefficient layer order`

---

### 9.8 Security Scanning
**Rule**: Trivy or grype in CI.

**KAPI Validation**: `❌ No image scanning`

---

### 9.9 Explicit Tags
**Rule**: Never use latest.

**KAPI Validation**: `❌ Using latest tag`

---

### 9.10 Signal Handling
**Rule**: Use exec form for ENTRYPOINT.

**KAPI Validation**: `❌ Shell form in ENTRYPOINT`

---

## KAPI Integration

### Brutal Analysis Checks

**P0 (Critical - Block Deployment)**:
- ❌ Unchecked errors
- ❌ Data races (go test -race)
- ❌ Secrets in code
- ❌ SQL injection risk
- ❌ No input validation
- ❌ Container runs as root
- ❌ No tests

**P1 (High - Warn)**:
- ⚠️ Coverage < 80%
- ⚠️ No linting (golangci-lint)
- ⚠️ No security scanning (gosec)
- ⚠️ No graceful shutdown
- ⚠️ Non-standard project structure

**P2 (Medium - Suggest)**:
- ℹ️ Missing package docs
- ℹ️ No benchmarks
- ℹ️ No metrics
- ℹ️ Could use smaller Docker image

### Blueprint Generation

Every KAPI Go blueprint includes:
1. **Standard project layout** (golang-standards)
2. **Makefile** with common tasks
3. **golangci-lint** configuration
4. **go.mod/go.sum** committed
5. **Docker multi-stage** build
6. **Health check** endpoint
7. **Graceful shutdown** handler
8. **Structured logging** (zap)
9. **Test setup** with table-driven tests
10. **CI configuration** (.github/workflows)

### Living Specifications

```markdown
## Best Practices Compliance

✅ 1.1 Standard project layout
✅ 2.1 All errors checked
✅ 3.2 golangci-lint enabled
✅ 5.1 Test coverage 85%
✅ 6.2 gosec security scanning
✅ 8.3 Health check endpoint
✅ 9.1 Multi-stage Docker build
⚠️  7.7 OpenTelemetry - optional
⚠️  8.11 Circuit breakers - optional
```

---

## Quick Reference Checklist

### Essential (Must Have)
- [ ] Standard project layout
- [ ] All errors checked (no _ assignments)
- [ ] golangci-lint in CI
- [ ] go test -race passes
- [ ] Test coverage > 80%
- [ ] gosec security scanning
- [ ] No hardcoded secrets
- [ ] Parameterized SQL queries
- [ ] Context for cancellation
- [ ] Graceful shutdown
- [ ] Health check endpoint
- [ ] Structured logging
- [ ] go.mod/go.sum committed
- [ ] Multi-stage Dockerfile
- [ ] Non-root Docker user
- [ ] .dockerignore

### Important (Should Have)
- [ ] Package documentation
- [ ] Custom error types
- [ ] Table-driven tests
- [ ] Interface-based design
- [ ] Connection pooling
- [ ] Rate limiting
- [ ] Request ID propagation
- [ ] Metrics (Prometheus)
- [ ] Database migrations
- [ ] govulncheck in CI
- [ ] Docker health check
- [ ] Image scanning

### Nice to Have
- [ ] Distributed tracing
- [ ] Circuit breakers
- [ ] Benchmarks
- [ ] Example tests
- [ ] pprof endpoints
- [ ] Worker pools
- [ ] Alpine base image

---

## References

- **Project Layout**: https://github.com/golang-standards/project-layout
- **Clean Template**: https://github.com/evrone/go-clean-template
- **DDD Example**: https://github.com/ThreeDotsLabs/wild-workouts-go-ddd-example
- **Effective Go**: https://go.dev/doc/effective_go
- **Go Code Review**: https://github.com/golang/go/wiki/CodeReviewComments

---

**Last Updated**: January 2025  
**Maintained by**: KAPI Team
