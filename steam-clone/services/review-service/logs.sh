#!/bin/bash

# Review Service Logs Script

echo "Showing Review Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/review-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8003)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs review-service' to view logs"
    else
        echo "Service is not running."
    fi
fi