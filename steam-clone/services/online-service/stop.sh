#!/bin/bash

# Online Service Stop Script

echo "Stopping Online Service..."

# Find and kill the process running on port 8007
PID=$(lsof -t -i:8007)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8007..."
    kill -9 $PID
    echo "Online Service stopped."
else
    echo "No process found running on port 8007."
fi
