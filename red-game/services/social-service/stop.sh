#!/bin/bash

# Social Service Stop Script

echo "Stopping Social Service..."

# Find and kill the process running on port 8008
PID=$(lsof -t -i:8008)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8008..."
    kill -9 $PID
    echo "Social Service stopped."
else
    echo "No process found running on port 8008."
fi
