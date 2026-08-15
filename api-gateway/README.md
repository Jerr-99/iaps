# Backend API Gateway

The IAPS API Gateway is the main microservice handling authentication and user provisioning.

## Features

- User registration and login
- JWT-based authentication
- bcrypt password hashing
- PostgreSQL database integration

## Environment Variables

Create `.env` file based on `.env.example`:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=iaps
JWT_SECRET=your-super-secret-key
ACCESS_EXPIRES_IN=15m
PORT=4000
NODE_ENV=development
```

## Running Locally

```bash
npm install
npm run migrate  # Apply migrations
npm run dev      # Start dev server with nodemon
```

## API Endpoints

- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

## Architecture

- **src/index.js** - Express app setup and middleware
- **src/db.js** - PostgreSQL connection pool
- **src/routes/auth.js** - Authentication routes
- **db/migrations/** - SQL migrations for database schema
