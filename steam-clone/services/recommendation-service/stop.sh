#!/bin/bash

# Recommendation Service Stop Script

echo "Stopping Recommendation Service..."

# Find and kill the process running on port 8010
PID=$(lsof -t -i:8010)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8010..."
    kill -9 $PID
    echo "Recommendation Service stopped."
else
    echo "No process found running on port 8010."
fi
