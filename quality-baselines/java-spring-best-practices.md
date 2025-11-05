# Java/Spring Boot Best Practices Pattern

**KAPI Quality Baseline for Java/Spring Blueprints**

_Based on Spring Petclinic, JHipster, Spring Boot best practices_

## 1. Project Structure (7)
- Package by feature not layer
- Multi-module Maven/Gradle
- Clean Architecture layers
- Thin controllers, fat services
- Resources organized
- Test structure mirrors source
- Config classes centralized

## 2. Spring Practices (12)
- Use Spring Boot Starters
- Constructor injection (not @Autowired fields)
- Externalized configuration (profiles)
- @RestController for APIs
- @ControllerAdvice for errors
- DTOs separate from entities
- Bean Validation (@Valid)
- Actuator for health/metrics
- @Async for long operations
- Caching with @Cacheable
- Profile-specific beans
- Component scanning limits

## 3. Data Access (10)
- Spring Data JPA repositories
- Flyway/Liquibase migrations
- Avoid N+1 queries (@EntityGraph)
- Optimistic locking (@Version)
- Pagination (Pageable)
- Auditing annotations
- @Transactional on services only
- HikariCP connection pooling
- Database indexes
- Derived query methods

## 4. Security (15)
- Spring Security framework
- BCryptPasswordEncoder
- Secure JWT configuration
- CORS explicit origins
- CSRF when stateful
- @PreAuthorize for authorization
- Parameterized queries only
- Input validation (@Valid)
- Security headers
- HTTPS only
- Rate limiting (Bucket4j)
- OWASP Dependency Check
- Externalized secrets
- Audit logging
- OAuth2/OIDC

## 5. Testing (12)
- JaCoCo coverage > 80%
- @SpringBootTest integration
- @WebMvcTest for controllers
- @DataJpaTest for repos
- TestContainers for real DB
- MockMvc for REST
- @MockBean for mocks
- AssertJ assertions
- @ActiveProfiles("test")
- @ParameterizedTest
- Test fixtures (@BeforeEach)
- Contract testing

## 6. Production (14)
- Logback JSON logs
- Actuator endpoints
- Micrometer metrics
- Graceful shutdown
- Connection pool tuning
- Thread pool config
- Structured error logging
- APM integration
- DB connection retry
- Circuit breakers (Resilience4j)
- Dependency locking
- Externalized config
- Distributed tracing (Sleuth)
- Custom health indicators

## 7. Docker (8)
- Multi-stage builds
- JRE not JDK
- Non-root user
- .dockerignore
- Health check (actuator)
- JVM memory settings
- Layer caching
- Trivy scanning

## KAPI Validation

**P0**: No security, plain passwords, SQL injection, no tests, root user
**P1**: Coverage <80%, no health, no migrations, field injection
**P2**: No caching, no APM, basic assertions

## References
- https://github.com/spring-projects/spring-petclinic
- https://github.com/jhipster/generator-jhipster
- https://spring.io/projects/spring-boot
