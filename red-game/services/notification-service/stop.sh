#!/bin/bash

# Notification Service Stop Script

echo "Stopping Notification Service..."

# Find and kill the process running on port 8009
PID=$(lsof -t -i:8009)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8009..."
    kill -9 $PID
    echo "Notification Service stopped."
else
    echo "No process found running on port 8009."
fi
