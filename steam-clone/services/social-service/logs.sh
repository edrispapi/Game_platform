#!/bin/bash

# Social Service Logs Script

echo "Showing Social Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/social-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8008)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs social-service' to view logs"
    else
        echo "Service is not running."
    fi
fi
