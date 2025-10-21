#!/bin/bash

# Payment Service Logs Script

echo "Showing Payment Service logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/payment-service.log
else
    # Check if service is running
    PID=$(lsof -t -i:8006)
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs payment-service' to view logs"
    else
        echo "Service is not running."
    fi
fi
