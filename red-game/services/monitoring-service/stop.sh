#!/bin/bash

# Monitoring Service Stop Script

echo "Stopping Monitoring Service..."

# Find and kill the process running on port 8012
PID=$(lsof -t -i:8012)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8012..."
    kill -9 $PID
    echo "Monitoring Service stopped."
else
    echo "No process found running on port 8012."
fi
