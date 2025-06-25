# Playdate Organiser

A web application for parents to organize playdates for their children. Built with FastAPI (backend) and Next.js (frontend).

## Features

- User registration and authentication
- Manage children profiles
- Create and browse playdates
- Express interest in playdates
- Allow/deny lists for filtering who can see your playdates
- Mobile-responsive design

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Alembic
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Authentication**: JWT tokens
- **Deployment**: Docker & Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd playdate-organiser
```

2. Create environment files:
```bash
# Root directory (for Docker Compose)
cp .env.example .env

# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env

# IMPORTANT: Edit the .env files and change default passwords!
```

3. Start the application:
```bash
docker compose up
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies with uv:
```bash
pip install uv
uv sync
```

3. Set up the database:
```bash
# Start PostgreSQL (you can use Docker)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=playdate_db postgres:15-alpine

# Run migrations
uv run alembic upgrade head
```

4. Start the development server:
```bash
uv run uvicorn app.main:app --reload
```

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Database Migrations

To create a new migration:
```bash
cd backend
uv run alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```bash
uv run alembic upgrade head
```

## API Documentation

When the backend is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
playdate-organiser/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── crud/         # CRUD operations
│   │   ├── db/           # Database configuration
│   │   ├── models/       # SQLAlchemy models
│   │   └── schemas/      # Pydantic schemas
│   ├── alembic/          # Database migrations
│   ├── tests/            # Backend tests
│   └── Dockerfile
├── frontend/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── contexts/         # React contexts
│   ├── lib/              # Utility functions
│   ├── types/            # TypeScript types
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/playdate_db
SECRET_KEY=your-secret-key-here-change-in-production
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## License

This project is licensed under the MIT License.