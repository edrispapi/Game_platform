#!/bin/bash

# Online Service Logs Script

echo "Showing Online Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/online-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8007)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs online-service' to view logs"
    else
        echo "Service is not running."
    fi
fi
