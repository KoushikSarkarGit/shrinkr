# Shrinkr — Phase-Wise Learning & Implementation Plan

**4 Weeks • 56 Hours • 2 Hours/Day**

Purpose: Build the Core Requirements of Shrinkr while learning backend development end-to-end with FastAPI. The plan follows the agreed BRD and intentionally leaves advanced production features for the Future CR phase.

# **1\. How to Use This Plan**

* Each day is one focused 2-hour session.  
* Do not try to finish a topic by watching tutorials alone. Learn the concept, implement it, then test it.  
* Prefer one concept per meaningful commit/PR.  
* If a day's implementation takes longer, carry it into the next session rather than adding new scope.  
* Do not implement Future CRs during these four weeks.

# **2\. Standard 2-Hour Session Structure**

| Time | Activity | Goal |
| :---- | :---- | :---- |
| 0–25 min | Learn / review | Understand the day's backend concept |
| 25–100 min | Implement | Build the feature in Shrinkr |
| 100–120 min | Test \+ notes | Verify behavior and record what you learned |

# **3\. Phase Overview**

| Phase | Days | Hours | Primary Outcome |
| :---- | :---- | :---- | :---- |
| Phase 1 — FastAPI & Database Foundation | 1–7 | 14h | Working FastAPI \+ PostgreSQL backend |
| Phase 2 — Authentication & Email | 8–14 | 14h | Complete authentication subsystem |
| Phase 3 — Redis, Celery & Analytics | 15–21 | 14h | Cached redirects \+ async analytics |
| Phase 4 — Production Engineering | 22–28 | 14h | Testing, rate limiting, Docker, logging and final hardening |

# **Phase 1 — FastAPI & Database Foundation**

Goal: Establish the architecture and learn the complete synchronous request → database flow.

## **Day 1 — Project Setup & FastAPI Fundamentals**

**Learn:** FastAPI application structure, routers, path/query/body parameters, Pydantic request and response models.

**Build:** Create the Shrinkr project, package structure, first router, configuration, basic health endpoint and initial Docker setup.

**Checkpoint:** Application starts successfully and /healthz returns a valid response.

## **Day 2 — Dependency Injection, Lifespan & Middleware**

**Learn:** FastAPI dependency injection, dependency overrides, middleware and application lifespan.

**Build:** Create reusable dependencies for configuration and request context. Add basic middleware and startup/shutdown lifecycle handling.

**Checkpoint:** You can explain why dependencies belong outside individual route functions.

## **Day 3 — PostgreSQL & SQLAlchemy 2.0 Async**

**Learn:** Async SQLAlchemy sessions, models, engine, connection pooling and relational modeling.

**Build:** Connect PostgreSQL. Create User and Link models and an async database session dependency.

**Checkpoint:** Create and query a User/Link successfully through SQLAlchemy.

## **Day 4 — Repository & Service Architecture**

**Learn:** Separation of concerns: router → service → repository.

**Build:** Implement UserRepository and LinkRepository plus corresponding services. Keep routers thin.

**Checkpoint:** A request can travel cleanly from router to service to repository to PostgreSQL.

## **Day 5 — CRUD, Validation & Error Handling**

**Learn:** Pydantic validation, HTTP status codes, domain/application errors and global exception handling.

**Build:** Implement basic link CRUD with consistent response/error schemas and validation.

**Checkpoint:** Invalid input and common business errors return predictable API responses.

## **Day 6 — Alembic Migrations**

**Learn:** Schema migration workflow, upgrade/downgrade and migration safety.

**Build:** Configure Alembic and create migrations for the current schema. Practice an upgrade and downgrade.

**Checkpoint:** A fresh database can be created entirely through migrations.

## **Day 7 — Transactions & Concurrency Basics**

**Learn:** Transactions, commit/rollback, unique constraints, race conditions and the difference between application checks and DB guarantees.

**Build:** Add transaction boundaries to a multi-step operation and handle duplicate/custom-alias conflicts safely.

**Checkpoint:** You can explain what happens when two requests try to create the same alias simultaneously.

# **Phase 2 — Authentication & Email**

Goal: Build a secure, complete authentication workflow rather than only a login endpoint.

## **Day 8 — Registration & Password Hashing**

**Learn:** Password hashing, secure credential handling and registration flow.

**Build:** Implement POST /auth/register, password hashing, duplicate-email handling and user creation.

**Checkpoint:** Passwords are never stored or logged in plaintext.

## **Day 9 — JWT Access Authentication**

**Learn:** JWT structure, signing, claims, expiry and FastAPI authentication dependencies.

**Build:** Implement login and short-lived access tokens. Protect /auth/me and a sample protected endpoint.

**Checkpoint:** An authenticated request can reliably identify the current user.

## **Day 10 — Refresh Tokens**

**Learn:** Why access and refresh tokens are separated; secure refresh-token storage and expiry.

**Build:** Implement refresh-token persistence, hashing and POST /auth/refresh.

**Checkpoint:** Access tokens can be renewed without re-authenticating with a password.

## **Day 11 — Refresh Rotation & Logout**

**Learn:** Refresh-token rotation, revocation and token-reuse detection.

**Build:** Rotate refresh tokens on every refresh. Implement logout and invalidation of revoked tokens.

**Checkpoint:** Reusing an old refresh token is detected and handled safely.

## **Day 12 — RBAC & Authorization**

**Learn:** Authentication vs authorization, roles and FastAPI authorization dependencies.

**Build:** Add USER/ADMIN roles and reusable role-checking dependencies. Protect admin-only operations.

**Checkpoint:** A valid user cannot access an endpoint requiring a higher role.

## **Day 13 — Email Verification**

**Learn:** Secure one-time tokens, expiry, token hashing and asynchronous email architecture.

**Build:** Create email-verification tokens, verification endpoint and Celery-ready email service abstraction. Add Mailpit for local email testing.

**Checkpoint:** Registration can produce a verification email that can be inspected locally.

## **Day 14 — Password Reset**

**Learn:** Password-reset security, single-use tokens and email enumeration protection.

**Build:** Implement forgot-password and reset-password flows, token expiry/use tracking and async email delivery.

**Checkpoint:** The full password-reset flow works without revealing whether an email exists.

# **Phase 3 — Redis, Celery & Analytics**

Goal: Learn caching and asynchronous backend processing while keeping analytics off the redirect critical path.

## **Day 15 — Redis Integration**

**Learn:** Redis data model, connections and using Redis from an async FastAPI application.

**Build:** Add Redis connection lifecycle and a small reusable Redis dependency/service.

**Checkpoint:** FastAPI can safely communicate with Redis.

## **Day 16 — Redirect Cache**

**Learn:** Cache-aside pattern and cache hit/miss flow.

**Build:** Implement GET /{code} with Redis-first lookup, PostgreSQL fallback and cache population.

**Checkpoint:** A warm redirect is served from Redis.

## **Day 17 — TTL & Cache Invalidation**

**Learn:** TTL, stale data and invalidation strategy.

**Build:** Add TTLs and invalidate cached links when links are deleted/changed. Add TTL jitter where appropriate.

**Checkpoint:** Deleted/updated links do not remain indefinitely in cache.

## **Day 18 — Cache Stampede Protection**

**Learn:** Cache stampede and distributed locking concepts.

**Build:** Implement a simple Redis lock/protection mechanism around concurrent cache misses.

**Checkpoint:** Concurrent misses do not cause uncontrolled duplicate database reads.

## **Day 19 — Celery Fundamentals**

**Learn:** Workers, broker, tasks, retries and why background processing is needed.

**Build:** Add Celery \+ Redis and create a basic task. Run worker locally and through Docker Compose.

**Checkpoint:** A FastAPI request can enqueue a task and a worker can process it.

## **Day 20 — Click Events & Analytics**

**Learn:** Event-driven processing and idempotent task handling.

**Build:** Emit click events from redirects, store raw click data through Celery and implement hourly/daily aggregation.

**Checkpoint:** Redirect response does not wait for analytics processing.

## **Day 21 — Celery Reliability & Scheduled Jobs**

**Learn:** Task retry, exponential backoff, idempotency and scheduled tasks.

**Build:** Add retries/backoff and Celery Beat for scheduled statistics rollups. Test a failed task and retry behavior.

**Checkpoint:** You can explain what happens when a worker fails during a task.

# **Phase 4 — Production Engineering & Final Hardening**

Goal: Make the core application testable, observable and runnable as a complete backend system.

## **Day 22 — Cursor Pagination & Filtering**

**Learn:** Stable cursor pagination, ordering by created\_at \+ id, filtering and invalid cursors.

**Build:** Complete GET /links with cursor pagination, active/deleted filters and creation-date filtering.

**Checkpoint:** Pagination remains stable when records are inserted or deleted between requests.

## **Day 23 — Redis Rate Limiting**

**Learn:** Rate-limiting algorithms and identity-based limits.

**Build:** Implement anonymous and authenticated limits using Redis. Return 429, Retry-After and rate-limit headers.

**Checkpoint:** Repeated requests eventually receive a correct 429 response.

## **Day 24 — Unit Testing**

**Learn:** Testing services, dependency overrides, mocks and isolated business logic.

**Build:** Create unit tests for services, validators, authentication logic and important edge cases.

**Checkpoint:** Core business logic has meaningful automated unit coverage.

## **Day 25 — Integration Testing**

**Learn:** Testing FastAPI endpoints with HTTPX and real infrastructure.

**Build:** Use Testcontainers or an equivalent isolated environment to test PostgreSQL/Redis-backed flows.

**Checkpoint:** Major API workflows pass against realistic dependencies.

## **Day 26 — Docker Compose**

**Learn:** Containers, networking, environment variables, volumes and service dependencies.

**Build:** Containerize FastAPI, PostgreSQL, Redis, Celery Worker, Celery Beat and Mailpit. Add health checks.

**Checkpoint:** The core system starts with docker compose up.

## **Day 27 — Logging, Health & Basic CI**

**Learn:** Structured logging, request IDs, readiness/liveness and CI quality gates.

**Build:** Add structured logs, /healthz, /readyz and a GitHub Actions pipeline for linting, type checks and tests.

**Checkpoint:** A clean commit can pass the CI pipeline and the application exposes useful operational information.

## **Day 28 — Final Integration, Failure Testing & Architecture Review**

**Learn:** Failure-oriented testing and system-level reasoning.

**Build:** Run the complete system. Intentionally test Redis failure, invalid authentication, duplicate requests, failed tasks and database-related errors. Fix important issues and document architecture/trade-offs.

**Checkpoint:** You can draw the complete architecture and explain every major component, failure mode and design decision.

# **4\. Daily Definition of Done**

* The day's feature is implemented, not merely watched or copied.  
* At least one meaningful test or manual verification is performed.  
* The code is committed with a clear commit message.  
* You can explain what problem the feature solves.  
* You can explain at least one failure case or trade-off.

# **5\. Weekly Checkpoints**

| Checkpoint | Expected State |
| :---- | :---- |
| End of Week 1 | FastAPI → Service → Repository → PostgreSQL flow works. Migrations and basic transaction handling work. |
| End of Week 2 | Registration, login, JWT, refresh rotation, RBAC, email verification and password reset work end-to-end. |
| End of Week 3 | Redis-backed redirects and Celery-based analytics/email processing work end-to-end. |
| End of Week 4 | Pagination, rate limiting, tests, Docker, health checks and basic CI work. Full system can be demonstrated. |

# **6\. What Not to Implement During These 4 Weeks**

* OAuth2/social login  
* API keys and scopes  
* Nginx and multi-instance deployment  
* Prometheus/Grafana  
* OpenTelemetry/Jaeger  
* Advanced circuit breakers  
* Transactional Outbox  
* WebSockets  
* Kafka  
* Kubernetes  
* Read replicas and database partitioning  
* Webhooks and Vault

These are not discarded topics. They remain Future CRs in the BRD and should be implemented after the core project when the fundamentals are solid.

# **7\. Recommended Git Milestones**

| Milestone | Scope |
| :---- | :---- |
| M1 | FastAPI foundation |
| M2 | Database \+ architecture |
| M3 | Transactions \+ concurrency |
| M4 | Authentication |
| M5 | Email |
| M6 | Redis caching |
| M7 | Celery \+ analytics |
| M8 | Rate limiting \+ pagination |
| M9 | Testing |
| M10 | Docker \+ CI \+ final hardening |

# **8\. Final Outcome After 56 Hours**

At the end of the four weeks, Shrinkr should be a working, tested, containerized FastAPI backend with PostgreSQL, Redis, Celery and email processing. More importantly, the developer should be able to explain the complete request lifecycle, database transaction boundaries, authentication flow, cache strategy, asynchronous processing model, testing strategy and basic failure behavior.

The next stage is not to start another unrelated project immediately. Instead, use the existing Shrinkr codebase to implement the Future CRs one at a time, turning it into a progressively more production-grade backend system.