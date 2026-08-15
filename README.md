# IAPS (Integrated Authentication and Provisioning System)

A microservices-based platform for user authentication, authorization, and resource provisioning.

## Tech Stack

- **Frontend:** React (Vite)
- **Backend:** Node.js + Express
- **Database:** PostgreSQL
- **Auth:** JWT + bcrypt
- **Orchestration:** Docker Compose (local dev), Kubernetes (production)
- **CI/CD:** GitHub Actions

## Project Structure

```
iaps/
├── api-gateway/          # Backend API microservice
│   ├── src/
│   │   ├── index.js
│   │   ├── db.js
│   │   └── routes/
│   │       └── auth.js
│   ├── db/
│   │   └── migrations/
│   │       └── 001_create_users.sql
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── frontend/             # React (Vite) frontend
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml    # Local dev environment
├── .github/
│   └── workflows/
│       └── ci.yml
└── technology-stack-final.md
```

## Quick Start

### Prerequisites

- Node.js 18+ (or use devcontainer)
- Docker & Docker Compose
- PostgreSQL 14+

### Local Development

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Jerr-99/iaps.git
   cd iaps
   ```

2. **Install dependencies:**
   ```bash
   cd api-gateway && npm install && cd ..
   cd frontend && npm install && cd ..
   ```

3. **Set up environment:**
   ```bash
   # Create .env files from examples
   cp api-gateway/.env.example api-gateway/.env
   # Edit api-gateway/.env with your values
   ```

4. **Run with Docker Compose:**
   ```bash
   docker-compose up
   ```

   Or **run services locally:**
   ```bash
   # Terminal 1: Backend
   cd api-gateway
   npm run dev

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

5. **Apply DB migrations:**
   ```bash
   cd api-gateway
   npm run migrate
   ```

### API Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token

### Environment Variables

See `api-gateway/.env.example` for required variables:
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `JWT_SECRET` - Secret key for signing JWT tokens
- `ACCESS_EXPIRES_IN` - Token expiration time (default: 15m)

## Development

### Running Tests

```bash
cd api-gateway
npm run test

cd ../frontend
npm run test
```

### Linting

```bash
npm run lint
```

## Deployment

See `.github/workflows/ci.yml` for CI/CD pipeline. Configure GitHub Actions secrets for:
- `GHCR_TOKEN` - Container registry credentials
- `POSTGRES_PASSWORD` - Database password
- `JWT_SECRET` - JWT signing secret

## Contributing

Please create a new branch for features and submit a pull request.

## License

MIT
