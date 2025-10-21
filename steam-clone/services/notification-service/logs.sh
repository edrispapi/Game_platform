#!/bin/bash

# Notification Service Logs Script

echo "Showing Notification Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/notification-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8009)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs notification-service' to view logs"
    else
        echo "Service is not running."
    fi
fi
