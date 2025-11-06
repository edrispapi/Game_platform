#!/bin/bash

# Review Service Stop Script

echo "Stopping Review Service..."

# Find and kill the process running on port 8003
PID=$(lsof -t -i:8003)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8003..."
    kill -9 $PID
    echo "Review Service stopped."
else
    echo "No process found running on port 8003."
fi