# IAPS System Architecture

## 1. ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER (Frontend)                   │
│                                                                   │
│  React SPA (Vite) - Login, Dashboard, Engagement Management     │
│  Port: 5173 (dev), 80 (prod)                                    │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  │ HTTPS
                                  │
┌─────────────────────────────────▼────────────────────────────────┐
│                    API GATEWAY LAYER                              │
│                                                                   │
│  Traefik (Reverse Proxy + Load Balancing)                        │
│  - Route requests to backend services                            │
│  - SSL/TLS termination                                           │
│  - Rate limiting                                                 │
│  Port: 80, 443                                                   │
└────────────────┬────────────────────────────────┬────────────────┘
                 │                                │
                 │                                │
    ┌────────────▼────────────────────┐   ┌──────▼──────────────┐
    │    AUTHENTICATION SERVICE        │   │  MAIN API SERVICE   │
    │                                  │   │                     │
    │  Keycloak                        │   │  Django + DRF       │
    │  - User registration             │   │  - Engagement CRUD  │
    │  - 2FA/MFA                       │   │  - Financial Data   │
    │  - JWT token management          │   │  - Analytics        │
    │  - RBAC (Roles)                  │   │  - Materiality      │
    │  - SSO support                   │   │  - Risk Assessment  │
    │  Port: 8080                      │   │  - Dashboards       │
    │                                  │   │  - Documents        │
    └────────────────┬─────────────────┘   │  - Audit Logs       │
                     │                      │  Port: 8000         │
                     │                      │                     │
                     │                      └──────┬──────────────┘
                     │                             │
                     │                             │
                     └────────────────┬────────────┘
                                      │
                ┌─────────────────────▼─────────────────────┐
                │    ASYNC PROCESSING & AI LAYER             │
                │                                            │
                │  Celery Worker + Redis Queue               │
                │  - Process AI requests (Claude API)        │
                │  - Handle long-running tasks               │
                │  - Manage rate limiting for AI calls       │
                │  - Cache AI responses                      │
                │                                            │
                └────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        │                │                │
   ┌────▼────┐      ┌────▼────┐     ┌────▼────┐
   │          │      │         │     │         │
   │PostgreSQL│      │ Redis   │     │ Claude  │
   │Database  │      │ Cache   │     │ 3.5     │
   │          │      │         │     │ Sonnet  │
   │- Users   │      │- Cache  │     │  API    │
   │- Engage  │      │- Queues │     │ (Cloud) │
   │- Finance │      │- Sessions│     │         │
   │- Risks   │      │         │     │         │
   │- Logs    │      │         │     │         │
   │Port:5432 │      │Port:6379│     │         │
   └──────────┘      └─────────┘     └─────────┘
```

---

## 2. LAYERED ARCHITECTURE

### 2.1 Presentation Layer (Frontend)
**Technology:** React 18+ with Vite  
**Responsibilities:**
- User interface rendering
- Form validation (client-side)
- State management (Redux/Context)
- API communication
- Chart/Dashboard visualization

**Components:**
- Login/Registration pages
- Engagement management pages
- Financial data upload page
- Analytics/Dashboard pages
- Risk assessment pages
- AI recommendations page
- Document management page
- Task management page

**Port:** 5173 (dev), 80/443 (prod)

### 2.2 API Gateway Layer
**Technology:** Traefik  
**Responsibilities:**
- Route incoming requests to appropriate services
- SSL/TLS termination
- Rate limiting and throttling
- Request/response logging
- Load balancing across service instances
- CORS handling

**Features:**
- Dynamic routing based on path/hostname
- Automatic HTTPS redirect
- Middleware for authentication validation
- Circuit breaker for failing services

**Port:** 80 (HTTP), 443 (HTTPS)

### 2.3 Authentication Service
**Technology:** Keycloak  
**Responsibilities:**
- User registration and account management
- Login/logout with JWT tokens
- 2FA/MFA support
- Role-Based Access Control (RBAC)
- Token refresh and validation
- SSO capability for future integration
- User audit trail

**Key Endpoints:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login with credentials
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/logout` - Logout and invalidate token
- `GET /auth/user` - Get current user profile
- `POST /auth/2fa/setup` - Setup 2FA

**Port:** 8080

### 2.4 Main API Service
**Technology:** Django + Django REST Framework (DRF)  
**Responsibilities:**
- Core business logic implementation
- CRUD operations for all entities
- Financial calculations and analytics
- Risk assessment and scoring
- Materiality calculations
- Dashboard data aggregation
- Audit logging
- Document management
- PDF/Excel report generation

**Key Modules:**
1. **Engagement Service**
   - Create, read, update, delete engagements
   - Assign users to engagements
   - Engagement status management

2. **Financial Data Service**
   - Upload and validate financial data
   - Data cleaning and normalization
   - Financial ratio calculations
   - Trend analysis

3. **Analytics Service**
   - Calculate financial ratios
   - Perform variance analysis
   - Generate trend reports
   - Benchmark comparisons

4. **Materiality Service**
   - Quantitative materiality calculations
   - Qualitative assessment
   - Performance materiality determination
   - Clearly trivial threshold calculation

5. **Risk Assessment Service**
   - Risk identification
   - Risk scoring and prioritization
   - Internal control assessment
   - ROMM (Risk of Material Misstatement) calculation

6. **Planning Service**
   - Generate audit procedures based on risks
   - Coordinate with AI service for recommendations
   - Procedure assignment and tracking
   - Sample size determination

7. **Document Service**
   - Document upload and storage
   - Version control
   - Document classification
   - Audit trail for document access

8. **Dashboard Service**
   - Aggregate data for dashboards
   - Real-time metrics compilation
   - KPI calculations
   - Cached responses for performance

9. **Audit Trail Service**
   - Log all user actions
   - Track data changes
   - Compliance reporting
   - User activity audit

**Port:** 8000

### 2.5 Asynchronous Processing Layer
**Technology:** Celery + Redis  
**Responsibilities:**
- Queue long-running tasks
- Process AI requests without blocking API
- Manage Claude API rate limiting
- Handle background job processing
- Cache AI responses

**Tasks:**
- `process_ai_recommendation` - Call Claude API for planning suggestions
- `generate_pdf_report` - Generate audit plan PDF
- `calculate_bulk_ratios` - Calculate financial ratios for large datasets
- `send_email_notifications` - Send task reminders
- `cleanup_temporary_files` - Housekeeping tasks

**Queue Manager:** Redis (also used for response caching)

### 2.6 Data Layer
**Technology:** PostgreSQL 14+  
**Responsibilities:**
- Persistent data storage
- Data integrity via constraints and transactions
- Efficient data retrieval via indexing
- Audit trail storage
- Backup and recovery

**Key Databases:**
- `iaps_db` - Main application database
- Connection pooling for performance
- Replication setup for production HA

**Port:** 5432

### 2.7 Cache Layer
**Technology:** Redis  
**Responsibilities:**
- Caching frequently accessed data
- Session storage
- Task queue management
- Rate limiting counters
- AI response caching (to reduce API calls)

**Use Cases:**
- Dashboard data cache (5-min TTL)
- User session store (24-hour TTL)
- Financial ratio cache (1-day TTL)
- AI recommendation cache (persistent)
- API rate limit counters (1-hour TTL)

**Port:** 6379

### 2.8 External AI Service
**Technology:** Anthropic Claude 3.5 Sonnet API  
**Responsibilities:**
- Generate audit procedure recommendations
- Suggest sample sizes based on risk profiles
- Recommend resource allocation
- Provide risk commentary
- Generate audit approach guidance

**Integration Points:**
- Called via Celery async tasks
- Requests queued to manage rate limits
- Responses cached in database
- Audit trail logged for all AI interactions

**Rate Limits:** Managed by Celery queue + throttling
**Cost:** Pay-per-use via Anthropic API

---

## 3. MICROSERVICES DECOMPOSITION (Future)

While currently a monolithic Django backend, the architecture allows future microservices decomposition:

```
Current (Monolithic):
┌─────────────────────────────────────────┐
│   Django Monolith (All services)        │
│  - Engagement, Analytics, Risk, etc.    │
└─────────────────────────────────────────┘

Future Phase (Microservices):
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Engagement Svc   │  │ Analytics Svc    │  │ Risk Svc         │
│ (Port: 8001)     │  │ (Port: 8002)     │  │ (Port: 8003)     │
└──────────────────┘  └──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Materiality Svc  │  │ Planning Svc     │  │ Document Svc     │
│ (Port: 8004)     │  │ (Port: 8005)     │  │ (Port: 8006)     │
└──────────────────┘  └──────────────────┘  └──────────────────┘

All behind Traefik API Gateway
Coordinated via message queue (Kafka/RabbitMQ)
```

---

## 4. DATA FLOW EXAMPLES

### 4.1 User Registration Flow
```
1. Frontend: User fills registration form
2. Frontend: Submit to /auth/register (Traefik)
3. Traefik: Route to Keycloak auth service
4. Keycloak: Create user account, hash password
5. Keycloak: Return JWT token
6. Frontend: Store token, redirect to dashboard
```

### 4.2 Financial Data Analysis Flow
```
1. Frontend: Upload CSV/Excel file
2. Traefik: Route to Django API (/api/financial-data/upload)
3. Django: Save file, validate format
4. Django: Parse and insert into database (financial_data table)
5. Django: Trigger Celery task (calculate_ratios)
6. Celery Worker: Calculate financial ratios from data
7. Django: Store ratios in database (financial_ratio table)
8. Frontend: Poll API or receive notification, display dashboard
```

### 4.3 Risk Assessment & AI Planning Flow
```
1. Frontend: Review risks, click "Get AI Recommendations"
2. Django API: Fetch risks, prepare prompt
3. Celery Task: Queue AI request to Claude API
4. Claude API: Process request, return recommendations
5. Celery Task: Store recommendations in database (ai_recommendation table)
6. Django API: Mark task as complete
7. Frontend: Display AI recommendations for supervisor review
8. Supervisor: Approve/reject recommendations
9. Django API: Store final audit procedures
10. Frontend: Generate audit plan report
```

### 4.4 Dashboard Data Aggregation Flow
```
1. Frontend: Request dashboard data (/api/dashboard/engagement/1)
2. Traefik: Route to Django API
3. Django: Check Redis cache for data (5-min TTL)
4. If cached: Return immediately
5. If not cached:
   - Query financial_ratio table
   - Query risk table (sum by category)
   - Query audit_procedure table (count by status)
   - Query materiality table
   - Aggregate into dashboard DTO
   - Cache in Redis for 5 minutes
   - Return to frontend
6. Frontend: Render charts and widgets
```

---

## 5. DEPLOYMENT ARCHITECTURE

### 5.1 Local Development (Docker Compose)
```yaml
services:
  postgres:
    image: postgres:14
    ports: [5432:5432]
    
  redis:
    image: redis:7-alpine
    ports: [6379:6379]
    
  keycloak:
    image: keycloak/keycloak:latest
    ports: [8080:8080]
    
  django-api:
    build: ./api-gateway
    ports: [8000:8000]
    depends_on: [postgres, redis, keycloak]
    
  celery-worker:
    build: ./api-gateway
    command: celery -A config worker -l info
    depends_on: [postgres, redis]
    
  react-frontend:
    build: ./frontend
    ports: [5173:5173] (dev) or [80:80] (prod)
    
  traefik:
    image: traefik:v2
    ports: [80:80, 443:443]
    command: See traefik.yml for routing rules
```

### 5.2 Production (Kubernetes)
```
Namespace: iaps-prod

Deployments:
- keycloak-deployment (replicas: 2)
- django-api-deployment (replicas: 3)
- celery-worker-deployment (replicas: 2)
- frontend-deployment (replicas: 2)

StatefulSets:
- postgres-statefulset (replicas: 1, with persistent volume)
- redis-statefulset (replicas: 1, with persistent volume)

Services:
- keycloak-service (ClusterIP)
- django-api-service (ClusterIP)
- postgres-service (ClusterIP)
- redis-service (ClusterIP)
- frontend-service (LoadBalancer or NodePort)

ConfigMaps:
- django-settings-configmap
- traefik-config-configmap

Secrets:
- postgres-credentials
- jwt-secret
- claude-api-key
```

---

## 6. SECURITY ARCHITECTURE

### 6.1 Authentication & Authorization Flow
```
1. User login via Keycloak
2. Keycloak validates credentials (2FA if enabled)
3. Keycloak returns JWT token with roles embedded
4. Frontend stores JWT in secure httpOnly cookie
5. Frontend sends JWT in Authorization header for subsequent requests
6. Traefik/Django validates JWT signature
7. Django checks user roles for endpoint authorization
8. Audit log recorded for sensitive operations
```

### 6.2 Data Security
- **In Transit:** TLS 1.3 for all HTTP communications
- **At Rest:** Database encryption (PostgreSQL pgcrypto or disk-level)
- **Access Control:** PostgreSQL role-based row-level security
- **Secrets Management:** Docker secrets (dev), Kubernetes secrets (prod)
- **Backup Encryption:** Encrypted database backups

### 6.3 API Security
- **Rate Limiting:** Traefik rate limiter + Django throttling
- **Input Validation:** DRF serializers + custom validators
- **SQL Injection Prevention:** Django ORM + parameterized queries
- **CSRF Protection:** Django CSRF middleware + SameSite cookies
- **XSS Protection:** React automatic escaping + Content Security Policy
- **CORS:** Configured for frontend domain only
- **HTTPS:** Enforced redirect, HSTS headers

---

## 7. SCALABILITY CONSIDERATIONS

### Horizontal Scaling
- **Django API:** Multiple pods behind load balancer
- **Celery Workers:** Scale up/down based on queue depth
- **PostgreSQL:** Read replicas for read-heavy operations
- **Redis:** Cluster mode for distributed caching

### Vertical Scaling
- **Database:** Increase CPU, RAM, storage as needed
- **Cache:** Increase Redis memory
- **API Servers:** Increase pod resource requests

### Performance Optimization
- **Database:** Indexes on frequently queried columns
- **Caching:** Multi-level (Redis, HTTP caching)
- **Async Processing:** Long tasks via Celery
- **CDN:** Static assets (frontend CSS, JS)
- **Pagination:** Limit returned records
- **Lazy Loading:** Load data on-demand

---

## 8. MONITORING & OBSERVABILITY

### Logging
- **Application Logs:** Django + Python logging (ELK stack or CloudWatch)
- **Access Logs:** Traefik access logs
- **Audit Logs:** Stored in database + shipped to audit system
- **Celery Logs:** Task execution and errors

### Metrics
- **Application Metrics:** Request latency, error rates, throughput (Prometheus)
- **Database Metrics:** Query performance, connection pool usage
- **Cache Metrics:** Hit/miss ratio, evictions
- **System Metrics:** CPU, memory, disk usage

### Alerting
- **High Error Rate:** Alert on 500 errors > 5% of requests
- **Slow Response:** Alert on p95 latency > 2 seconds
- **Database:** Alert on connection pool exhaustion
- **Celery:** Alert on queue depth > threshold
- **Disk:** Alert on disk usage > 80%

---

## 9. DISASTER RECOVERY

### Backup Strategy
- **Database:** Automated daily backups (pg_dump), stored off-site
- **Code:** Distributed version control (GitHub)
- **Configuration:** Infrastructure as Code (Docker Compose, Kubernetes YAML)

### Recovery Time Objectives (RTOs)
- **Database Corruption:** 1 hour (restore from backup)
- **API Service Outage:** 15 minutes (automated restart + failover)
- **Complete System Failure:** 2 hours (full infrastructure rebuild from code)

### High Availability (Production)
- **Multi-region deployment:** Failover to secondary region
- **Database replication:** Real-time replication to standby
- **Load balancing:** Automatic failover across instances
- **Health checks:** Continuous monitoring and auto-recovery

---

**Document Version:** 1.0  
**Last Updated:** 2026-08-16  
**Architecture Pattern:** Layered with API Gateway + Microservices-ready design
