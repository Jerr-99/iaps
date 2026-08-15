# IAPS Technology Stack - Final Decision

**Date:** August 2026  
**Project:** Integrated Authentication and Provisioning System (IAPS)

## Overview

This document outlines the finalized technology choices for the IAPS microservices platform and the rationale behind each decision.

---

## 1. Frontend

### **React with Vite**
- **Why:** Fast build tool, excellent for modern React development, smaller bundle sizes, instant HMR
- **Alignment:** Microservices architecture requires lightweight, independent frontends that can be deployed separately
- **Version:** React 18+
- **Package Manager:** npm/yarn

**Alternatives considered:**
- Create React App (CRA): Slower builds, heavier bundler
- Next.js: Good for SSR but adds server dependency (we prefer frontend independence)
- Vue/Svelte: Not as mature ecosystem for enterprise features

---

## 2. Backend

### **Node.js with Express**
- **Why:** 
  - Lightweight, event-driven I/O fits microservices pattern
  - Excellent async/await support
  - Large ecosystem and middleware community
  - Same language (JavaScript) as frontend reduces cognitive load
- **Version:** 18 LTS (stable, long-term support)
- **Framework:** Express.js (minimal, flexible)

**Alternatives considered:**
- Fastify: Faster but smaller ecosystem
- Django/Python: Overkill for lightweight auth microservices
- Go: Good performance but different language/team skill requirement
- NestJS: Over-engineered for initial phase

---

## 3. Database

### **PostgreSQL**
- **Why:**
  - Reliable, battle-tested relational database
  - ACID compliance ensures data integrity
  - JSON support (JSONB) for flexible schemas
  - Built-in role-based access control (RBAC)
  - Excellent for microservices (separate DB per service possible)
- **Version:** 14+ (stable, modern features)

**Alternatives considered:**
- MySQL: Simpler but fewer features
- MongoDB: Good for unstructured data but overkill for user/auth data
- SQLite: Single-file, not suitable for multi-service architecture

---

## 4. Authentication & Security

### **JWT + bcrypt**
- **JWT (JSON Web Tokens):**
  - Stateless tokens fit microservices (no shared session store needed)
  - Easy to validate across services
  - Standard, widely supported
  
- **bcrypt:**
  - Industry standard for password hashing
  - Built-in salt generation
  - Configurable work factor for future-proofing

**Alternatives considered:**
- Session-based auth: Requires shared session store (Redis/Memcached)
- OAuth2: More complex, better for third-party integrations (future phase)
- Passwords only: Insecure (bcrypt hashing mandatory)

---

## 5. Containerization & Orchestration

### **Docker & Docker Compose (Local Dev)**
- **Why:**
  - Containers ensure consistency between development, staging, and production
  - Docker Compose simplifies local development setup
  - Quick spinning up of full stack (postgres + backend + frontend)
  - Foundation for Kubernetes deployment

### **Kubernetes (Production)**
- **Why:**
  - Auto-scaling, self-healing
  - Service mesh support (Istio) for advanced microservices patterns
  - Industry standard for cloud-native deployments
  - Fits well with microservices expansion

**Alternatives considered:**
- Docker Swarm: Simpler but less feature-rich
- Lambda/Serverless: Not suitable for auth services (stateful)
- Traditional VMs: Too slow to provision/scale

---

## 6. CI/CD & Repository

### **GitHub Actions**
- **Why:**
  - Integrated with GitHub (no separate CI tool)
  - Free for public/private repos
  - Native Docker image building and pushing
  - Matrix builds for multiple Node versions/OS

### **GitHub Container Registry (GHCR)**
- **Why:**
  - Integrated with GitHub repositories
  - Private by default, no Docker Hub account needed
  - Seamless pull/push from Actions

**Alternatives considered:**
- GitLab CI: More powerful but hosted externally
- Jenkins: Self-hosted, more maintenance
- Docker Hub: Public images possible but less integrated

---

## 7. Database Migrations

### **node-pg-migrate**
- **Why:**
  - Simple CLI tool for PostgreSQL
  - Integrates well with Node.js projects
  - Easy rollback/forward
  - Lightweight compared to ORM migration systems

**Alternatives considered:**
- TypeORM/Sequelize: Heavier, introduces ORM complexity
- Flyway: Java-based, overkill for pure SQL needs
- Manual SQL: Error-prone, no version control

---

## 8. Development Environment

### **VS Code + DevContainers (Optional)**
- **Why:**
  - Consistent environment across team
  - Automatically installs Node.js, npm, extensions
  - No local environment pollution
  - Works on Windows/Mac/Linux

### **Docker Compose for Local Orchestration**
- **Why:**
  - One command to spin up entire stack
  - Database and backend run in containers
  - Frontend runs locally (HMR benefits for development)

---

## Decision Matrix

| Component | Choice | Rationale | Risk | Notes |
|-----------|--------|-----------|------|-------|
| Frontend | React + Vite | Speed, ecosystem | Low | Solid choice for UI |
| Backend | Node.js + Express | Lightweight, JS ecosystem | Low | Standard microservice stack |
| Database | PostgreSQL | ACID, features, scaling | Low | Industry standard |
| Auth | JWT + bcrypt | Stateless, secure, standard | Low | Must override JWT_SECRET in prod |
| Container Orchestration | Docker Compose (dev), K8s (prod) | Consistency, scalability | Medium | Requires K8s expertise for prod |
| CI/CD | GitHub Actions | Integrated, free | Low | Works seamlessly with GitHub |
| Migrations | node-pg-migrate | Lightweight, SQL-based | Low | Simple, no ORM lock-in |

---

## Deployment Strategy

### Development
```
docker-compose up
```

### Staging
- Push to GitHub
- GitHub Actions builds and pushes images to GHCR
- Deploy to staging Kubernetes cluster using Helm charts (future)

### Production
- Images from GHCR deployed to production Kubernetes
- Horizontal Pod Autoscaling enabled
- Health checks, resource limits, and monitoring via Prometheus/Grafana (future)

---

## Scalability & Growth Path

1. **Phase 1 (Current):** Single microservice (auth), monolithic frontend
2. **Phase 2:** Break auth into separate services (user service, token service)
3. **Phase 3:** Add resource provisioning microservice, implement API gateway pattern
4. **Phase 4:** Service mesh (Istio), advanced monitoring, multi-region deployment

---

## Security Considerations

- **Secrets Management:** GitHub Actions secrets (prod), .env files (local, not committed)
- **Database:** Separate credentials per environment, encrypted in transit (TLS)
- **API:** CORS policies, rate limiting (to be added)
- **Code:** Dependabot for dependency scanning, GitHub branch protections

---

## Cost Estimation

| Component | Cost | Notes |
|-----------|------|-------|
| GitHub Actions | Free | 2000 minutes/month free tier |
| GHCR | Free | Private images included |
| Kubernetes | $50–300/mo | GKE, EKS, DigitalOcean pricing varies |
| PostgreSQL (managed) | $15–100/mo | AWS RDS, DigitalOcean, Heroku options |
| **Total (production)** | **$65–400/mo** | Scales with usage; dev/test: minimal cost |

---

## Conclusion

This stack is **production-ready, scalable, and maintainable**:
- ✅ Fast development cycle (Vite HMR, npm dev servers)
- ✅ Cloud-native (Docker, Kubernetes ready)
- ✅ Secure (JWT, bcrypt, GitHub secrets)
- ✅ Cost-effective (open-source, free CI/CD tier)
- ✅ Team-friendly (single language, mature ecosystem, great docs)

The stack aligns perfectly with microservices architecture and is prepared for scaling as IAPS grows.
