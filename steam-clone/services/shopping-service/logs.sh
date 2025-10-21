#!/bin/bash

# Shopping Service Logs Script

echo "Showing Shopping Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/shopping-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8004)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs shopping-service' to view logs"
    else
        echo "Service is not running."
    fi
fi