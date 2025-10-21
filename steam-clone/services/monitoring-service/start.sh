#!/bin/bash

# Monitoring Service Start Script

echo "Starting Monitoring Service..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the service
echo "Starting Monitoring Service on port 8012..."
uvicorn app.main:app --host 0.0.0.0 --port 8012 --reload
