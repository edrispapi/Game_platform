#!/bin/bash

# Monitoring Service Logs Script

echo "Showing Monitoring Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/monitoring-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8012)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs monitoring-service' to view logs"
    else
        echo "Service is not running."
    fi
fi
