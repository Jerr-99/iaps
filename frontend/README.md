# Frontend - React with Vite

Modern React frontend for IAPS authentication and provisioning system.

## Features

- Fast development with Vite
- Login/Registration forms
- JWT token management
- Responsive design
- Clean, minimal UI

## Setup

```bash
npm install
npm run dev      # Start dev server at http://localhost:5173
npm run build    # Build for production
npm run preview  # Preview production build
```

## Environment Variables

Create `.env.local` if needed:

```
VITE_API_URL=http://localhost:4000
```

## Project Structure

- **src/main.jsx** - React app entry point
- **src/App.jsx** - Main component with login/register forms
- **src/App.css** - Component styles
- **src/index.css** - Global styles
- **index.html** - HTML template
- **vite.config.js** - Vite configuration

## API Integration

The frontend communicates with the backend at `http://localhost:4000` (or configured VITE_API_URL):

- `POST /auth/register` - User registration
- `POST /auth/login` - User login (receives JWT token)

## Styling

Gradient background with card-based design. Mobile-responsive layout.
