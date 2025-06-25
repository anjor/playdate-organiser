#!/bin/bash
# This script creates the initial migration
# Run this after starting the postgres container but before starting the backend

echo "Creating initial migration..."
uv run alembic revision --autogenerate -m "Initial migration"
echo "Migration created successfully!"