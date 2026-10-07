# **BRD — Shrinkr**

## **Production-Oriented URL Shortener & Analytics API**

**Project Type:** Backend / REST API  
**Primary Framework:** FastAPI  
**Initial Development Window:** 4 weeks  
**Available Time:** \~2 hours/day  
**Estimated Core Effort:** \~56 hours  
**Architecture:** Modular Monolith  
**Frontend:** Out of scope

---

# **1\. Project Overview**

**Shrinkr** is a production-oriented URL shortener and analytics REST API.

The URL-shortener domain is intentionally simple. The purpose of the project is to use a manageable business domain to learn **end-to-end backend development with FastAPI**.

The project will progressively introduce:

* API development  
* request validation  
* database design  
* authentication and authorization  
* transactions  
* concurrency  
* caching  
* asynchronous processing  
* email systems  
* rate limiting  
* testing  
* Docker  
* observability  
* resilience  
* CI/CD  
* distributed-system concepts

The initial implementation is intentionally limited to what can reasonably be completed in approximately **56 hours**.

Advanced production features will be preserved as **Future CRs** and implemented after the core system is complete.

---

# **2\. Primary Objective**

The primary objective is **not simply to build a URL shortener**.

The objective is to learn how to design, build, test, operate and explain a real backend system using FastAPI.

By the end of the core project, the developer should understand the complete flow:

Client  
   ↓  
HTTP Request  
   ↓  
FastAPI Router  
   ↓  
Dependency Injection  
   ↓  
Validation  
   ↓  
Service Layer  
   ↓  
Repository Layer  
   ↓  
PostgreSQL / Redis  
   ↓  
Response

and the asynchronous flow:

FastAPI  
   ↓  
Celery / Redis  
   ↓  
Background Worker  
   ↓  
Email / Analytics / Scheduled Processing  
---

# **3\. Learning Objectives**

By completing the core project, the developer should be able to explain and implement:

## **FastAPI**

* Application structure  
* Routers  
* Path/query/body parameters  
* Pydantic schemas  
* Dependency Injection  
* Middleware  
* Lifespan  
* Startup/shutdown  
* Exception handlers  
* OpenAPI documentation

## **Database**

* PostgreSQL  
* SQLAlchemy 2.0 async  
* Database sessions  
* Repository pattern  
* Transactions  
* Commit/rollback  
* Constraints  
* Indexes  
* Query optimization  
* Alembic migrations  
* Connection pooling

## **Authentication**

* Password hashing  
* JWT access tokens  
* Refresh tokens  
* Refresh-token rotation  
* Token revocation  
* RBAC  
* Authentication dependencies

## **Distributed/backend systems**

* Redis  
* Caching  
* Cache invalidation  
* Cache stampede  
* Celery  
* Background processing  
* Task retries  
* Idempotent tasks  
* Scheduled tasks

## **Production engineering**

* Error handling  
* Rate limiting  
* Structured logging  
* Health checks  
* Docker  
* Automated testing  
* Basic CI/CD  
* Failure handling

---

# **4\. Scope**

## **4.1 Core Scope**

The core project will contain:

* REST API  
* User authentication  
* User authorization  
* Email verification  
* Password reset  
* URL shortening  
* Redirects  
* Click analytics  
* PostgreSQL  
* Redis  
* Celery  
* Docker  
* Testing  
* Rate limiting  
* Basic observability

## **4.2 Out of Scope — Core Phase**

The following will **not** be implemented during the initial 56-hour phase:

* OAuth2/social login  
* API keys  
* Nginx load balancing  
* multiple API instances  
* Prometheus  
* Grafana  
* Jaeger  
* OpenTelemetry  
* advanced circuit breakers  
* transactional outbox  
* WebSockets  
* Kafka  
* Kubernetes  
* multi-region deployment  
* Vault  
* read replicas

These are documented under **Future CRs**.

---

# **5\. Architecture**

Shrinkr will be implemented as a **modular monolith**.

                        ┌──────────────────┐  
                         │      Client      │  
                         └────────┬─────────┘  
                                  │  
                                  ▼  
                         ┌──────────────────┐  
                         │     FastAPI      │  
                         └────────┬─────────┘  
                                  │  
                  ┌───────────────┼───────────────┐  
                  │               │               │  
                  ▼               ▼               ▼  
             PostgreSQL        Redis          Celery  
                  │               │               │  
                  │               │               ├── Email  
                  │               │               │  
                  │               │               └── Analytics  
                  │               │  
                  │               └── Cache  
                  │  
                  └── Persistent Data  
---

# **6\. Application Architecture**

The application should follow:

Router  
   ↓  
Service  
   ↓  
Repository  
   ↓  
Database

### **Responsibilities**

### **Router**

Responsible for:

* HTTP handling  
* request/response schemas  
* dependency injection  
* authentication dependencies  
* calling services

Routers should contain minimal business logic.

### **Service**

Responsible for:

* business rules  
* workflows  
* transaction coordination  
* interaction between repositories and infrastructure services

### **Repository**

Responsible for:

* database access  
* queries  
* persistence  
* database-specific operations

### **Infrastructure**

External-system integrations should be isolated.

app/  
├── api/  
├── services/  
├── repositories/  
├── infrastructure/  
│   ├── database/  
│   ├── redis/  
│   └── email/  
├── tasks/  
├── middleware/  
├── models/  
├── schemas/  
└── core/  
---

# **7\. Functional Requirements**

## **FR-1 — User Registration**

### **Endpoint**

POST /api/v1/auth/register

### **Requirements**

* Accept user registration data.  
* Validate request using Pydantic.  
* Hash password.  
* Store user in PostgreSQL.  
* Prevent duplicate email registration.  
* Generate email-verification token.  
* Queue verification email asynchronously.

---

# **8\. Authentication**

## **FR-2 — Login**

POST /api/v1/auth/login

Requirements:

* Validate credentials.  
* Verify password.  
* Return access token.  
* Return refresh token.  
* Reject unverified accounts if configured as required.

### **Access Token**

Lifetime: 15 minutes

### **Refresh Token**

Lifetime: 7 days  
---

# **9\. Refresh Token Rotation**

## **FR-3 — Refresh**

POST /api/v1/auth/refresh

Requirements:

* Validate refresh token.  
* Issue a new access token.  
* Issue a new refresh token.  
* Revoke the previous refresh token.

If an already-rotated refresh token is reused, the system must treat it as potential token theft and revoke the associated session/token family.

---

# **10\. Logout**

## **FR-4 — Logout**

POST /api/v1/auth/logout

Requirements:

* Revoke the current refresh token.  
* Ensure the revoked token cannot be used again.

---

# **11\. Current User**

## **FR-5 — Current User**

GET /api/v1/auth/me

Returns the authenticated user's profile.

---

# **12\. RBAC**

## **FR-6 — Role-Based Access Control**

Initial roles:

USER  
ADMIN

Authorization must be implemented through FastAPI dependencies.

Admin-only functionality may include:

* viewing administrative information  
* deleting any link  
* inspecting failed background tasks in future versions

---

# **13\. Email Verification**

## **FR-7 — Email Verification**

GET /api/v1/auth/verify-email

Requirements:

* Generate secure token.  
* Store token securely.  
* Token must expire.  
* Token must be single-use.  
* Mark account as verified after successful validation.  
* Token must not be logged.

Email sending must happen asynchronously.

---

# **14\. Password Reset**

## **FR-8 — Request Password Reset**

POST /api/v1/auth/forgot-password

The endpoint must not reveal whether a given email address exists.

If appropriate, queue a password-reset email.

## **FR-9 — Reset Password**

POST /api/v1/auth/reset-password

Requirements:

* Validate reset token.  
* Check expiration.  
* Ensure token has not already been used.  
* Change password.  
* Invalidate token.  
* Ensure appropriate existing sessions/tokens are handled.

---

# **15\. Email Subsystem**

Email is a first-class subsystem rather than a simple utility function.

Architecture:

FastAPI  
   ↓  
Service  
   ↓  
Celery Task  
   ↓  
Email Service  
   ↓  
Email Provider

The application must not tightly couple business logic to a specific provider.

## **Email Requirements**

* Verification email  
* Password-reset email  
* HTML template  
* Plain-text fallback  
* Secure token links  
* Token expiry  
* Retry on transient failures  
* Provider timeout  
* Failure logging  
* No sensitive values in logs  
* Test email delivery without sending real emails

### **Local Development**

Use a local mail server such as **Mailpit**.

---

# **16\. URL Shortening**

## **FR-10 — Create Short Link**

POST /api/v1/links

Request:

target\_url  
custom\_alias (optional)

Requirements:

* Validate target URL.  
* Generate Base62 short code.  
* Detect collisions.  
* Support custom aliases.  
* Prevent duplicate custom aliases.  
* Associate link with authenticated user.

---

# **17\. Idempotency**

## **FR-11 — Idempotent Link Creation**

`POST /api/v1/links` must support:

Idempotency-Key: \<key\>

Requirements:

* Same user \+ same key should not create duplicate resources.  
* Original response should be returned for repeated requests.  
* Keys expire after approximately 24 hours.  
* Concurrent identical requests must be handled safely.

This must be implemented using appropriate database constraints/transactions rather than relying solely on an application-level "check then insert".

---

# **18\. Link Listing**

## **FR-12 — List Links**

GET /api/v1/links

Requirements:

* Cursor-based pagination  
* Filtering  
* Sorting  
* Active/deleted filtering  
* Creation-date filtering

Response:

{  
  "data": \[\],  
  "next\_cursor": "..."  
}

Cursor pagination should use a stable ordering such as:

created\_at \+ id  
---

# **19\. Link Details**

## **FR-13 — Link Details**

GET /api/v1/links/{code}

Return:

* target URL  
* creation information  
* status  
* ownership information  
* summary statistics

---

# **20\. Link Deletion**

## **FR-14 — Delete Link**

DELETE /api/v1/links/{code}

Use soft deletion:

deleted\_at

Normal application behavior must never hard-delete links.

Cache must be invalidated after deletion.

---

# **21\. Redirect**

## **FR-15 — Redirect**

GET /{code}

Requirements:

* Find the target URL.  
* Return HTTP `302`.  
* Use Redis cache.  
* Fall back to PostgreSQL on cache miss.  
* Populate cache after a miss.  
* Do not perform expensive analytics processing synchronously.

---

# **22\. Redirect Performance**

Target:

Warm-cache p95: \< 50ms  
Cache miss p95: \< 200ms

The redirect path must be optimized as the application's hot path.

---

# **23\. Click Analytics**

Every successful redirect should generate a click event containing:

link/code  
timestamp  
IP  
user-agent  
referrer

Analytics processing must not block the redirect response.

Architecture:

Redirect  
   ↓  
Generate Click Event  
   ↓  
Queue  
   ↓  
Celery Worker  
   ↓  
PostgreSQL  
---

# **24\. Analytics Statistics**

## **FR-16 — Statistics**

GET /api/v1/links/{code}/stats

Statistics should be based on pre-aggregated data rather than repeatedly scanning the raw click table.

Support:

* hourly statistics  
* daily statistics

---

# **25\. Redis Caching**

Redis will initially be used for:

* URL redirect cache  
* rate limiting  
* idempotency support where appropriate  
* Celery broker  
* token/revocation data where appropriate

## **Cache Strategy**

Use cache-aside:

Request  
   ↓  
Redis?  
 ┌─┴─┐  
Hit  Miss  
 │     │  
 │     ▼  
 │   PostgreSQL  
 │     │  
 │     ▼  
 │   Redis SET  
 │  
 ▼  
Response

Requirements:

* TTL  
* cache invalidation  
* TTL jitter  
* cache-hit measurement  
* protection against cache stampede

---

# **26\. Cache Invalidation**

When a link is deleted or modified:

Database Update  
      ↓  
Cache Invalidation

The system must prevent stale links from remaining cached indefinitely.

---

# **27\. Cache Stampede**

The implementation should demonstrate protection against multiple simultaneous cache misses.

Example:

1,000 requests  
      ↓  
Redis MISS  
      ↓  
Only one DB lookup  
      ↓  
Redis populated  
      ↓  
Remaining requests use cache

A Redis lock may be used for this.

---

# **28\. Celery**

Use:

Celery \+ Redis

Celery will process:

* click events  
* verification emails  
* password-reset emails  
* scheduled statistics aggregation

Tasks should be designed to be idempotent.

---

# **29\. Task Reliability**

Tasks should support:

* retries  
* exponential backoff  
* jitter  
* reasonable timeout configuration  
* failure logging

A duplicate task must not result in duplicate analytics counting or repeated destructive operations.

---

# **30\. Celery Beat**

Use Celery Beat for scheduled work.

Initial scheduled task:

Daily statistics rollup  
---

# **31\. Rate Limiting**

Implement application-level rate limiting using Redis.

Initial limits:

Anonymous users:      10 requests/minute  
Authenticated users:  60 requests/minute  
Redirect endpoint:    Dedicated higher limit

Rate limiting identity may be based on:

* IP  
* authenticated user  
* API key in future versions

When the limit is exceeded:

429 Too Many Requests

Include:

Retry-After  
X-RateLimit-Limit  
X-RateLimit-Remaining  
---

# **32\. Database**

Use:

PostgreSQL  
SQLAlchemy 2.0 async  
Alembic

## **Database Requirements**

* relational modeling  
* foreign keys  
* unique constraints  
* indexes  
* transactions  
* connection pooling  
* async database access

---

# **33\. Transactions**

The project must explicitly practice:

* transaction boundaries  
* commit  
* rollback  
* atomic operations  
* handling transaction failures  
* integrity errors

Example:

Create Link  
   ├── Create link  
   └── Store idempotency result  
          ↓  
       COMMIT

If either operation fails:

ROLLBACK  
---

# **34\. Concurrency**

The system must address race conditions involving:

* custom aliases  
* idempotency keys  
* refresh-token rotation  
* duplicate tasks  
* concurrent link updates

The implementation should demonstrate the difference between:

Application-level checks  
        vs  
Database constraints  
        vs  
Database locks  
---

# **35\. Database Optimization**

Practice:

* indexes  
* composite indexes  
* query plans  
* `EXPLAIN ANALYZE`  
* joins  
* N+1 query detection  
* eager/lazy loading  
* connection pool tuning

---

# **36\. Data Model**

## **users**

id  
email  
hashed\_password  
role  
is\_verified  
created\_at  
updated\_at

## **refresh\_tokens**

id  
user\_id  
token\_hash  
expires\_at  
revoked\_at  
created\_at

## **links**

id  
code  
target\_url  
user\_id  
deleted\_at  
created\_at  
updated\_at

## **clicks**

id  
link\_id  
created\_at  
ip  
user\_agent  
referrer

## **click\_stats\_hourly**

link\_id  
hour  
count

## **click\_stats\_daily**

link\_id  
date  
count

## **idempotency\_keys**

id  
key  
user\_id  
request\_hash  
response  
status\_code  
expires\_at  
created\_at

## **email\_tokens**

id  
user\_id  
token\_hash  
purpose  
expires\_at  
used\_at  
created\_at  
---

# **37\. API Standards**

All application APIs should use:

/api/v1/...

Requirements:

* consistent HTTP methods  
* appropriate HTTP status codes  
* Pydantic response models  
* consistent error format  
* cursor pagination  
* OpenAPI documentation  
* request/response examples

---

# **38\. Error Handling**

Use a consistent RFC 7807-style error response.

Common status codes:

400 Bad Request  
401 Unauthorized  
403 Forbidden  
404 Not Found  
409 Conflict  
422 Validation Error  
429 Too Many Requests  
500 Internal Server Error  
503 Service Unavailable

Application/business exceptions should be translated by global exception handlers.

Do not expose:

* stack traces  
* database errors  
* internal implementation details  
* secrets

---

# **39\. FastAPI Dependency Injection**

Dependency Injection should be used for:

* database sessions  
* authentication  
* authorization  
* configuration  
* Redis  
* services  
* repository dependencies

Tests should use dependency overrides where appropriate.

---

# **40\. Application Lifecycle**

Use FastAPI lifespan mechanisms for:

* database connection resources  
* Redis resources  
* initialization  
* cleanup

The application must shut down gracefully.

---

# **41\. Security**

The core project must implement:

* secure password hashing  
* JWT validation  
* refresh-token protection  
* RBAC  
* CORS configuration  
* security headers  
* rate limiting  
* secret management  
* input validation  
* brute-force protection  
* password-reset protection  
* email enumeration protection

The developer should understand SSRF and open-redirect risks associated with URL-shortener applications.

Sensitive information must never be logged.

Never log:

passwords  
JWTs  
refresh tokens  
API keys  
email tokens  
password-reset tokens  
application secrets  
---

# **42\. Logging**

Implement structured application logging.

Log useful information such as:

request ID  
HTTP method  
route  
status code  
latency  
user ID where appropriate  
error information

Sensitive data must be excluded.

---

# **43\. Health & Readiness**

## **Liveness**

GET /healthz

Checks whether the application process is alive.

## **Readiness**

GET /readyz

Checks whether the application is capable of serving requests based on required dependencies.

---

# **44\. Testing**

Use:

pytest  
pytest-asyncio  
httpx  
factory-boy  
testcontainers

## **Unit Tests**

Test:

* services  
* business logic  
* validators  
* utilities  
* middleware

## **Integration Tests**

Test against real infrastructure where appropriate:

* PostgreSQL  
* Redis

Test:

* registration  
* login  
* refresh  
* logout  
* RBAC  
* link creation  
* idempotency  
* redirects  
* pagination  
* caching  
* rate limiting  
* analytics

## **Failure Tests**

Test:

* invalid credentials  
* expired JWT  
* revoked refresh token  
* duplicate request  
* Redis failure  
* database failure  
* Celery failure  
* task retry

Target:

≥ 80% coverage  
---

# **45\. Docker**

Use Docker for local development.

Services:

FastAPI  
PostgreSQL  
Redis  
Celery Worker  
Celery Beat  
Mailpit

Use:

* multi-stage Dockerfile  
* non-root user  
* environment variables  
* `.env.example`  
* health checks

The entire core system should eventually start with:

docker compose up  
---

# **46\. Configuration**

Use:

pydantic-settings

Configuration should be environment-driven.

Separate:

development  
test  
production

Real secrets must never be committed.

---

# **47\. CI/CD**

If time permits within the core 56-hour window, implement a basic GitHub Actions pipeline:

Lint  
 ↓  
Type Check  
 ↓  
Test  
 ↓  
Coverage  
 ↓  
Docker Build

Tools:

Ruff  
MyPy  
Pytest  
Docker

CI should fail if tests fail or coverage falls below the defined threshold.

---

# **48\. Core Non-Functional Requirements**

## **Performance**

Redirect target:

p95 \< 50ms

for warm-cache requests.

## **Reliability**

Application should gracefully handle:

* Redis failure  
* failed background tasks  
* invalid requests  
* transient external failures

## **Security**

* no secrets in source code  
* no sensitive information in logs  
* password hashing  
* token expiry  
* authorization enforcement

## **Maintainability**

* layered architecture  
* clear responsibilities  
* type hints  
* automated tests  
* documented APIs

---

# **49\. Core Technology Stack**

| Concern | Technology |
| ----- | ----- |
| Framework | FastAPI |
| Language | Python |
| Validation | Pydantic |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Cache | Redis |
| Background Tasks | Celery |
| Scheduler | Celery Beat |
| Email Development | Mailpit |
| Testing | Pytest \+ HTTPX |
| Test Infrastructure | Testcontainers |
| Containerization | Docker |
| Linting | Ruff |
| Type Checking | MyPy |
| CI | GitHub Actions |

---

# **50\. Future CRs — Advanced Backend Engineering**

The following requirements are **not part of the initial 56-hour implementation**.

They are future implementation requirements for continuing the Shrinkr backend-learning project.

---

## **FCR-1 — OAuth2**

Implement OAuth2 authorization-code flow.

Providers:

* Google  
* GitHub

Requirements:

* OAuth login  
* account linking  
* existing-account detection  
* secure callback handling

**Concepts:** OAuth2, third-party identity, authorization code flow.

---

## **FCR-2 — API Keys**

Implement machine-to-machine authentication.

Requirements:

* create API key  
* hash key at rest  
* show only once  
* revoke key  
* expiration  
* scopes

**Concepts:** API authentication, scopes, credential lifecycle.

---

## **FCR-3 — Nginx & Load Balancing**

Architecture:

Client  
  ↓  
Nginx  
 ├── FastAPI \#1  
 └── FastAPI \#2

Implement:

* reverse proxy  
* TLS termination  
* load balancing  
* health checks

**Concepts:** horizontal scaling, reverse proxies, traffic management.

---

## **FCR-4 — Prometheus & Grafana**

Add:

* request metrics  
* latency histograms  
* error rates  
* cache hit ratio  
* DB pool usage  
* Celery queue depth

Create Grafana dashboards.

---

## **FCR-5 — Distributed Tracing**

Implement:

OpenTelemetry  
      ↓  
Jaeger

Trace:

HTTP  
 ↓  
FastAPI  
 ↓  
Redis/PostgreSQL  
 ↓  
Celery  
 ↓  
Worker  
 ↓  
Database  
---

## **FCR-6 — Advanced Resilience**

Implement:

* timeout policies  
* retry policies  
* exponential backoff  
* jitter  
* circuit breakers  
* graceful degradation

Explicitly define behavior when:

Redis fails  
Database fails  
Email provider fails  
OAuth provider fails  
Celery worker fails  
---

## **FCR-7 — Dead-Letter Queue**

Implement:

* permanently failed task storage  
* failure inspection  
* retry count  
* error information  
* admin re-drive mechanism

---

## **FCR-8 — Transactional Outbox**

Implement:

Database Transaction  
 ├── Business Data  
 └── Outbox Event  
          ↓  
      Publisher  
          ↓  
       Celery

Learn how to guarantee reliable event publication.

---

## **FCR-9 — WebSockets**

Add:

/ws/links/{code}/live

Display live click events.

Use Redis Pub/Sub to support multiple API instances.

**Concepts:**

* WebSocket lifecycle  
* persistent connections  
* async concurrency  
* Pub/Sub  
* horizontal scaling

---

## **FCR-10 — Database Partitioning**

Partition the `clicks` table by month.

Study:

* partition pruning  
* maintenance  
* indexes  
* query performance

---

## **FCR-11 — Read Replicas**

Introduce read/write separation.

Write → Primary  
Read  → Replica

Study:

* replication lag  
* consistency  
* routing  
* failure behavior

---

## **FCR-12 — Webhooks**

Add:

POST /api/v1/webhooks

Notify external systems about events such as link creation.

Implement:

* HMAC signatures  
* retries  
* timeout  
* failure handling  
* delivery history

---

## **FCR-13 — Kafka**

Replace the Celery/Redis event mechanism for selected event streams.

Learn:

* producers  
* consumers  
* topics  
* partitions  
* consumer groups  
* offsets  
* event replay

---

## **FCR-14 — Kubernetes**

Deploy Shrinkr using:

* Kubernetes  
* Helm  
* ConfigMaps  
* Secrets  
* Deployments  
* Services  
* Ingress  
* readiness/liveness probes

---

## **FCR-15 — Advanced Secrets Management**

Introduce Vault or an equivalent secrets-management solution.

Learn:

* secret injection  
* secret rotation  
* short-lived credentials  
* production secret management

---

# **51\. Core Definition of Done**

The **56-hour core project** is complete when:

1. FastAPI application is structured into routers, services and repositories.  
2. PostgreSQL is integrated using SQLAlchemy 2.0 async.  
3. Alembic migrations work.  
4. Users can register and log in.  
5. Passwords are securely hashed.  
6. JWT authentication works.  
7. Refresh-token rotation works.  
8. RBAC works.  
9. Email verification works.  
10. Password reset works.  
11. Emails are processed asynchronously.  
12. Users can create short URLs.  
13. Custom aliases work.  
14. Idempotency works.  
15. Concurrent requests are handled correctly.  
16. Cursor pagination works.  
17. Links can be soft-deleted.  
18. Redirects work.  
19. Redis caching works.  
20. Cache invalidation works.  
21. Click events are processed asynchronously.  
22. Statistics are aggregated.  
23. Celery retries failed tasks.  
24. Rate limiting works.  
25. Standardized errors are returned.  
26. Automated tests cover the major workflows.  
27. Docker Compose runs the core system.  
28. Health/readiness endpoints work.  
29. Structured logging exists.  
30. The developer can explain the complete architecture and major trade-offs.

---

# **52\. Final Learning Standard**

The project should not be considered successful merely because all endpoints work.

The developer should be able to answer:

### **Architecture**

* Why FastAPI?  
* Why a service layer?  
* Why a repository layer?  
* Why PostgreSQL?  
* Why Redis?  
* Why Celery?

### **Database**

* Where are transactions required?  
* What race conditions exist?  
* How does the database protect against duplicate aliases?  
* Why use indexes?  
* How would you diagnose a slow query?

### **Authentication**

* Why short-lived access tokens?  
* Why refresh tokens?  
* Why rotate refresh tokens?  
* What happens if a refresh token is stolen?

### **Caching**

* Why cache redirects?  
* What happens on a cache miss?  
* How is stale data handled?  
* What happens if Redis goes down?  
* What is a cache stampede?

### **Async Processing**

* Why shouldn't analytics block redirects?  
* Why use Celery instead of executing the task inside the request?  
* How are failed tasks retried?  
* What happens if a task runs twice?

### **Production**

* How do you handle failures?  
* How do you test the system?  
* How do you monitor it?  
* How would you scale it?  
* What would you change if traffic increased 100×?

The ultimate goal is to move from:

> **"I know FastAPI."**

to:

> **"I can design and reason about a backend system built with FastAPI."**

