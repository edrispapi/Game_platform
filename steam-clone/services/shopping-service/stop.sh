#!/bin/bash

# Shopping Service Stop Script

echo "Stopping Shopping Service..."

# Find and kill the process running on port 8004
PID=$(lsof -t -i:8004)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8004..."
    kill -9 $PID
    echo "Shopping Service stopped."
else
    echo "No process found running on port 8004."
fi