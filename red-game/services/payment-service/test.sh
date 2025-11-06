#!/bin/bash

# Payment Service Test Script

echo "Running Payment Service tests..."

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

# Install test dependencies
echo "Installing test dependencies..."
pip install pytest pytest-asyncio httpx

# Run tests
echo "Running tests..."
pytest tests/ -v

echo "Tests completed."
