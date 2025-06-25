## Project Setup Instructions

**Create a new playdate organiser app with the following structure:**

```
playdate-organiser/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend  
├── docker-compose.yml
└── README.md
```

## Backend Requirements (FastAPI)

**Create a FastAPI backend in the `backend/` directory with:**

1. **Dependencies**: FastAPI, SQLAlchemy, Alembic, python-jose, passlib, python-multipart, uvicorn, psycopg2-binary, python-dotenv

2. **Database Models** (using SQLAlchemy):
   - User: id, email, name, hashed_password, school_verified, created_at, updated_at
   - Child: id, name, year_group, age, parent_id (FK to User), created_at
   - Playdate: id, title, description, date_time, location, child_id (FK), parent_id (FK), status, created_at
   - Interest: id, playdate_id (FK), parent_id (FK), message, created_at
   - UserList: id, user_id (FK), target_user_id (FK), list_type (enum: allowlist/denylist)

3. **API Endpoints**:
   - Authentication: register, login, logout, get current user
   - User management: get/update profile, manage children
   - Playdates: CRUD operations with filtering logic
   - Interest management: express/withdraw interest
   - Allow/deny lists: manage user preferences
   - Basic messaging between interested parties

4. **Key Features**:
   - JWT authentication
   - Password hashing with bcrypt
   - Database migrations with Alembic
   - Environment configuration with .env
   - CORS middleware for frontend integration
   - Input validation with Pydantic models

5. **Filtering Logic**: When fetching playdates, filter out posts where current user is denylisted or not on allowlist (if allowlist exists)

## Frontend Requirements (Next.js)

**Create a Next.js frontend in the `frontend/` directory with:**

1. **Dependencies**: Next.js 14+, React, TypeScript, Tailwind CSS, Axios/fetch for API calls, React Hook Form, date-fns or similar for date handling

2. **Pages/Components**:
   - Authentication: login, register pages
   - Dashboard: view available playdates
   - Create playdate: form to post new playdate
   - Profile management: edit user info and children
   - Settings: manage allow/deny lists
   - Responsive mobile-first design

3. **State Management**: Use React Context or simple useState for authentication state

4. **API Integration**: Create API client to communicate with FastAPI backend

5. **Styling**: Use Tailwind CSS for responsive, mobile-friendly design

## Development Setup

**Include these files:**

1. **docker-compose.yml**: PostgreSQL database, Redis (optional), backend and frontend services
2. **Backend Dockerfile**: Python environment with FastAPI
3. **Frontend Dockerfile**: Node.js environment with Next.js
4. **Environment files**: .env templates for both backend and frontend
5. **Database initialization**: Alembic migrations for initial schema

## Additional Requirements

- **Security**: Implement proper CORS, input validation, rate limiting
- **Error Handling**: Comprehensive error responses and frontend error boundaries
- **Logging**: Basic logging setup for debugging
- **Documentation**: API documentation with FastAPI's built-in Swagger
- **Testing**: Basic test structure (optional for MVP)

**The app should be ready to run locally with `docker-compose up` and include sample data for testing.**
