#!/bin/bash

# Payment Service Stop Script

echo "Stopping Payment Service..."

# Find and kill the process running on port 8006
PID=$(lsof -t -i:8006)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8006..."
    kill -9 $PID
    echo "Payment Service stopped."
else
    echo "No process found running on port 8006."
fi
