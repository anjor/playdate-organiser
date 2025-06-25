FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Install dependencies manually
RUN uv pip install --system fastapi uvicorn[standard] sqlalchemy alembic psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv pydantic pydantic-settings email-validator

# Copy application files
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY start.sh ./

# Make start script executable
RUN chmod +x start.sh

# Run the application
CMD ["./start.sh"]