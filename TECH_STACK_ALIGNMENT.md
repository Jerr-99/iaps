# IAPS Technology Stack - Current vs. Intended

## EXECUTIVE SUMMARY

The current IAPS project has a **foundation** that aligns with the intended project in some areas, but requires **significant changes** to fully support the intended system. This document outlines the alignment gaps and recommends necessary updates.

---

## 1. COMPONENT COMPARISON

### 1.1 Frontend

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **Framework** | React 18+ | React 18+ | ✅ ALIGNED | No change |
| **Build Tool** | Vite | Vite | ✅ ALIGNED | No change |
| **UI Library** | Not specified | Bootstrap 5 / Material-UI | ⚠️ PARTIAL | Add UI library |
| **Charts/Viz** | Not specified | Chart.js / D3.js | ❌ MISSING | Install charting library |
| **State Mgmt** | Not specified | Redux / Context API | ⚠️ MISSING | Implement state management |
| **Package Mgr** | npm | npm | ✅ ALIGNED | No change |
| **Testing** | Not specified | Jest + React Testing Library | ❌ MISSING | Add test framework |
| **Port (Dev)** | Not specified | 5173 | ✅ ALIGNED | Vite default |
| **Port (Prod)** | Not specified | 80/443 | ✅ ALIGNED | Configure nginx/Traefik |

### 1.2 Backend

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **Language** | JavaScript/Node.js | Python 3.11+ | ❌ DIFFERENT | Rewrite in Python/Django |
| **Framework** | Express.js | Django 4.2+ + DRF | ❌ DIFFERENT | Rewrite using Django |
| **Database Driver** | pg (Node.js) | psycopg2 (Python) | ⚠️ COMPATIBLE | Switch driver |
| **Authentication** | JWT (custom) | Keycloak + JWT | ❌ MISSING | Integrate Keycloak |
| **2FA Support** | Not specified | Keycloak 2FA | ❌ MISSING | Enable in Keycloak |
| **Task Queue** | Not specified | Celery + Redis | ❌ MISSING | Add Celery |
| **Cache** | Not specified | Redis | ❌ MISSING | Add Redis caching |
| **Migration Tool** | Not specified | Django migrations | ✅ COMPATIBLE | Use Django ORM |
| **Port** | 4000 | 8000 | ⚠️ DIFFERENT | Update port in config |
| **Testing** | Not specified | pytest + coverage | ❌ MISSING | Add pytest |
| **Async Processing** | Not specified | Celery workers | ❌ MISSING | Add Celery workers |

### 1.3 Database

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **DBMS** | PostgreSQL 14+ | PostgreSQL 14+ | ✅ ALIGNED | No change |
| **Schema** | Basic (users table) | Complex (15+ tables) | ⚠️ PARTIAL | Expand schema |
| **Migrations** | 001_create_users.sql | Django migrations | ⚠️ COMPATIBLE | Migrate to Django migrations |
| **Port** | 5432 | 5432 | ✅ ALIGNED | No change |
| **Connection Pooling** | Not specified | Yes (via Django) | ⚠️ MISSING | Configure in Django |
| **Indexing** | Not specified | Yes (on frequently queried columns) | ⚠️ MISSING | Add indexes in schema |
| **Row-Level Security** | Not specified | Optional (PostgreSQL RLS) | ⚠️ MISSING | Implement if needed |

### 1.4 Authentication & Security

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **Auth Method** | JWT (custom implementation) | Keycloak + JWT | ❌ DIFFERENT | Deploy Keycloak |
| **2FA/MFA** | Not specified | Keycloak support | ❌ MISSING | Configure Keycloak |
| **Password Hashing** | bcrypt | bcrypt (via Django/Keycloak) | ✅ ALIGNED | No change |
| **RBAC** | Not implemented | Full RBAC (4 roles) | ❌ MISSING | Implement role system |
| **Token Type** | JWT | JWT | ✅ ALIGNED | No change |
| **Session Management** | Not specified | Redis-backed sessions | ❌ MISSING | Add session management |
| **Audit Logging** | Not specified | Comprehensive audit trail | ❌ MISSING | Implement audit system |

### 1.5 Containerization & Orchestration

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **Container Runtime** | Docker | Docker | ✅ ALIGNED | No change |
| **Orchestration (Dev)** | Docker Compose | Docker Compose | ✅ ALIGNED | No change |
| **Orchestration (Prod)** | Not specified | Kubernetes | ⚠️ MISSING | Add K8s manifests |
| **API Gateway (Dev)** | Not specified | Traefik | ❌ MISSING | Add Traefik container |
| **API Gateway (Prod)** | Not specified | Traefik | ❌ MISSING | Configure Traefik |
| **Keycloak** | Not included | Required | ❌ MISSING | Add Keycloak service |
| **Redis** | Not included | Required | ❌ MISSING | Add Redis service |
| **Celery Workers** | Not included | Required | ❌ MISSING | Add Celery containers |

### 1.6 CI/CD & Deployment

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **CI/CD Tool** | GitHub Actions | GitHub Actions | ✅ ALIGNED | No change |
| **Container Registry** | GHCR | GHCR | ✅ ALIGNED | No change |
| **Build Pipeline** | Basic (implied) | Multi-service builds | ⚠️ NEEDS EXPANSION | Expand pipeline |
| **Testing in CI** | Not specified | Unit + Integration tests | ❌ MISSING | Add to workflow |
| **Security Scanning** | Not specified | Dependency scanning | ❌ MISSING | Add to workflow |
| **Artifact Signing** | Not specified | Optional | ⚠️ MISSING | Consider adding |

### 1.7 External Services

| Component | Current | Intended | Status | Action |
|-----------|---------|----------|--------|--------|
| **AI Service** | None | Claude 3.5 Sonnet (Anthropic) | ❌ MISSING | Setup API account + integration |
| **Email Service** | Not specified | SMTP (for notifications) | ⚠️ MISSING | Configure if needed |
| **Monitoring** | Not specified | Optional (Prometheus/ELK) | ⚠️ FUTURE | Add in Phase 2 |
| **APM** | Not specified | Optional (New Relic/DataDog) | ⚠️ FUTURE | Add in Phase 2 |

---

## 2. CRITICAL CHANGES REQUIRED

### Priority 1: MUST IMPLEMENT (Project Won't Work Without These)

#### 2.1 Backend Rewrite: Node.js → Python/Django
**Current State:** Express.js backend with basic auth routes  
**Required State:** Full Django + DRF backend with all business logic  
**Effort:** High (2-3 weeks)  
**Rationale:**
- Django ORM provides better abstractions for complex data models
- Django Admin for internal management
- DRF better suited for complex API endpoints
- Better ecosystem for AI integration (Celery, OpenAI/Anthropic SDKs)
- Easier async task processing via Celery

**Implementation Plan:**
1. Create Django project structure
2. Define all data models (15+ tables)
3. Implement all serializers and viewsets
4. Create API endpoints for all features
5. Migrate existing auth logic to Keycloak
6. Write comprehensive tests

#### 2.2 Authentication: Custom → Keycloak
**Current State:** Custom JWT in Express.js  
**Required State:** Keycloak for centralized auth with 2FA/RBAC  
**Effort:** Medium (1-2 weeks)  
**Rationale:**
- 2FA/MFA support built-in
- RBAC management UI
- SSO-ready for future enterprise needs
- Removes auth burden from main API

**Implementation Plan:**
1. Deploy Keycloak container
2. Configure realms, clients, and roles
3. Setup 2FA requirements
4. Update frontend to use Keycloak
5. Update Django to validate Keycloak tokens
6. Test all auth flows

#### 2.3 Async Processing: Add Celery + Redis
**Current State:** No async task processing  
**Required State:** Celery for AI requests + background jobs  
**Effort:** Medium (1-2 weeks)  
**Rationale:**
- AI API calls are slow (5-30 seconds)
- Cannot block HTTP requests waiting for Claude API
- Rate limiting for API calls
- Retry logic for failed requests
- Response caching

**Implementation Plan:**
1. Add Celery to Django project
2. Add Redis service to Docker Compose
3. Create Celery tasks for:
   - `process_ai_recommendation`
   - `generate_reports`
   - `calculate_analytics`
4. Setup task monitoring
5. Add task status polling to frontend

#### 2.4 API Gateway: Add Traefik
**Current State:** No API gateway  
**Required State:** Traefik for request routing, SSL termination, rate limiting  
**Effort:** Medium (1 week)  
**Rationale:**
- Single entry point for all services
- SSL/TLS termination
- Automatic HTTP→HTTPS redirect
- Rate limiting at gateway level
- Load balancing across instances
- Path-based routing to different services

**Implementation Plan:**
1. Add Traefik container to Docker Compose
2. Configure routing rules:
   - `/auth/*` → Keycloak (port 8080)
   - `/api/*` → Django (port 8000)
   - `/` → React frontend (port 80)
3. Setup SSL certificates (Let's Encrypt for prod)
4. Configure rate limiting
5. Test all routes

#### 2.5 Database Schema: Expand Significantly
**Current State:** 1 table (users) with basic auth fields  
**Required State:** 15+ tables for full IAPS system  
**Effort:** Medium (1 week)  
**Rationale:**
- Support all 12 functional areas
- Proper data normalization
- Foreign key relationships
- Audit trail storage

**Implementation Plan:**
1. Design complete ER diagram
2. Create Django models for:
   - Engagement
   - FinancialData
   - FinancialRatio
   - Materiality
   - InternalControl
   - Risk
   - AuditProcedure
   - AIRecommendation
   - Document
   - AuditLog
3. Create Django migrations
4. Setup indexes for performance
5. Implement constraints and validations

#### 2.6 Docker Compose: Update with All Services
**Current State:** Basic setup (postgres, maybe api-gateway)  
**Required State:** Full stack (postgres, redis, keycloak, django, celery, traefik, react)  
**Effort:** Low-Medium (3-4 days)  
**Rationale:**
- "docker-compose up" should start everything needed
- Matches production architecture
- Consistent development environment

**Implementation Plan:**
1. Update docker-compose.yml with:
   - PostgreSQL 14
   - Redis 7
   - Keycloak (with initial realm setup)
   - Django API (custom build)
   - Celery worker (custom build)
   - Celery beat (optional, for scheduled tasks)
   - Traefik
   - React frontend
2. Configure volumes for persistence
3. Configure environment variables
4. Setup health checks
5. Test full stack startup

---

### Priority 2: SHOULD IMPLEMENT (Needed for Full Functionality)

#### 2.7 Frontend State Management: Add Redux/Context
**Current State:** Not specified (likely component-level state)  
**Required State:** Centralized state management  
**Effort:** Medium (1-2 weeks)  
**Rationale:**
- Complex state across multiple pages
- Dashboard data, user data, engagement data
- Easier to manage API loading states
- Better debugging and time-travel

#### 2.8 Frontend UI Components: Add Bootstrap/Material-UI
**Current State:** Basic styling (App.css)  
**Required State:** Comprehensive UI component library  
**Effort:** Low (3-4 days)  
**Rationale:**
- Professional, responsive design
- Accessible components
- Consistent look and feel
- Faster development

#### 2.9 Charts & Visualization: Add Chart.js/D3.js
**Current State:** None  
**Required State:** Interactive charts for dashboards  
**Effort:** Medium (1 week)  
**Rationale:**
- Financial ratio trends
- Risk heatmaps
- Variance analysis visualization
- Risk scoring distribution

#### 2.10 Celery Beat: Scheduled Tasks
**Current State:** Not included  
**Required State:** Optional but useful  
**Effort:** Low (2-3 days)  
**Rationale:**
- Nightly data analysis
- Scheduled report generation
- Cache refresh
- Notification reminders

#### 2.11 AI Integration: Claude 3.5 Sonnet API
**Current State:** None  
**Required State:** Integrated via Celery  
**Effort:** Medium (1 week)  
**Rationale:**
- Core feature for AI-assisted planning
- Requires prompt engineering
- Response caching to reduce costs
- Audit logging of all AI interactions

---

### Priority 3: NICE TO HAVE (For Production Readiness)

#### 2.12 Testing: Add Unit & Integration Tests
- pytest for Django
- Jest for React
- Target: 80%+ code coverage

#### 2.13 Monitoring & Logging
- Prometheus for metrics
- ELK Stack or CloudWatch for logs
- Sentry for error tracking

#### 2.14 Kubernetes Manifests
- K8s deployments, services, configmaps
- For production deployment

#### 2.15 Documentation
- API documentation (Swagger/OpenAPI)
- User documentation
- Architecture documentation

---

## 3. CURRENT PROJECT ASSESSMENT

### What's Good (Reusable)
✅ Docker + Docker Compose foundation  
✅ PostgreSQL database choice  
✅ GitHub Actions setup  
✅ React + Vite frontend foundation  
✅ JWT concept (though implementation will change)  
✅ Repository structure

### What Needs to Change
❌ Backend technology (Node.js → Python/Django)  
❌ Authentication approach (Custom → Keycloak)  
❌ Missing services (Keycloak, Redis, Traefik, Celery)  
❌ Database schema (needs massive expansion)  
❌ Frontend features (missing UI lib, state mgmt, charts)  
❌ Async processing (none exists)  

### Effort Estimate
- **Backend Rewrite:** 2-3 weeks
- **Services Integration:** 1-2 weeks
- **Frontend Enhancements:** 1-2 weeks
- **Integration & Testing:** 1 week
- **Total:** 5-8 weeks (for core Phase 1)

---

## 4. RECOMMENDED TECH STACK CHANGES

### Backend: Express.js → Django

**Comparison:**

| Aspect | Express.js | Django |
|--------|-----------|--------|
| **Learning Curve** | Low | Medium |
| **Scalability** | Good | Excellent |
| **ORM** | Sequelize/TypeORM (third-party) | Django ORM (built-in) |
| **Admin Panel** | Build from scratch | Built-in Admin |
| **Authentication** | Build or add auth0/passport | Many options (Keycloak compatible) |
| **Async Tasks** | Bull, RabbitMQ, etc. | Celery (built-in support) |
| **CLI Tools** | Limited | Django CLI (manage.py) |
| **Community** | Large | Massive (most popular web framework) |
| **Security** | Good | Excellent (CSRF, SQL injection, XSS) |
| **Documentation** | Good | Excellent |
| **Enterprise Adoption** | Growing | Dominant in enterprises |

**Decision: Use Django 4.2 LTS + Django REST Framework**

---

## 5. DEPLOYMENT ENVIRONMENT CHANGES

### Local Development

**Current:**
```yaml
services:
  postgres
  api-gateway (Node.js)
  frontend (React)
```

**Intended:**
```yaml
services:
  postgres
  redis
  keycloak
  django-api
  celery-worker
  traefik
  react-frontend
```

### Production

**Current:** Not specified  

**Intended:**
```
Kubernetes Cluster
├── Keycloak StatefulSet (HA)
├── Django Deployment (3 replicas)
├── Celery Worker Deployment (2 replicas)
├── Frontend Deployment (2 replicas)
├── PostgreSQL StatefulSet
└── Redis StatefulSet (for caching)

Plus:
- Traefik Ingress Controller
- Persistent Volumes for databases
- Configmaps and Secrets
- Network policies
- Service mesh (optional, future)
```

---

## 6. ACTION PLAN SUMMARY

### Immediate Actions (Week 1)
1. ✅ Read and understand intended project requirements
2. ✅ Create this technology stack alignment document
3. Create updated docker-compose.yml with all services
4. Start Django project structure (models definition)
5. Setup Keycloak realm and initial configuration

### Phase 1 Implementation (Weeks 1-4)
1. Rewrite backend in Django with all models
2. Implement Keycloak integration
3. Setup Celery + Redis
4. Deploy Traefik API gateway
5. Expand database schema

### Phase 2 Implementation (Weeks 5-8)
1. Implement all business logic (analytics, risk, materiality)
2. AI integration (Claude 3.5 Sonnet)
3. Frontend enhancements (state management, UI components)
4. Comprehensive testing

### Phase 3 (Weeks 9-10)
1. Integration testing
2. Performance optimization
3. Security audit
4. Documentation and deployment

---

## 7. TECHNOLOGY STACK FINAL DECISION

### Confirmed Tech Stack (Aligned with Project Requirements)

| Layer | Technology | Version | Port(s) | Status |
|-------|-----------|---------|---------|--------|
| **Frontend** | React + Vite | 18+, latest | 5173/80/443 | ✅ Keep |
| **Frontend UI** | Bootstrap 5 + Chart.js | Latest | - | ✅ Add |
| **Backend API** | Django + DRF | 4.2 LTS, 3.14+ | 8000 | ✅ New |
| **Auth Service** | Keycloak | Latest | 8080 | ✅ New |
| **Task Queue** | Celery | 5.3+ | - | ✅ New |
| **Cache/Queue** | Redis | 7+ | 6379 | ✅ New |
| **Database** | PostgreSQL | 14+ | 5432 | ✅ Keep |
| **API Gateway** | Traefik | 2.11+ | 80/443 | ✅ New |
| **Container Runtime** | Docker | Latest | - | ✅ Keep |
| **Orchestration (Dev)** | Docker Compose | 2.0+ | - | ✅ Keep |
| **Orchestration (Prod)** | Kubernetes | 1.27+ | - | ✅ New |
| **AI Integration** | Claude 3.5 Sonnet API | Latest | Cloud | ✅ New |
| **CI/CD** | GitHub Actions | - | - | ✅ Keep |
| **Container Registry** | GHCR | - | - | ✅ Keep |
| **Testing (Backend)** | pytest | Latest | - | ✅ New |
| **Testing (Frontend)** | Jest + RTL | Latest | - | ✅ New |

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-16  
**Status:** Ready for Implementation  
**Next Review:** After Backend Rewrite Completion
