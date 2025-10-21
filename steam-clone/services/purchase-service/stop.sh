#!/bin/bash

# Stop Purchase Service
echo "Stopping Purchase Service..."

# Find and kill the process running on port 8005
PID=$(lsof -t -i:8005)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8005..."
    kill -9 $PID
    echo "Purchase Service stopped."
else
    echo "No process found running on port 8005."
fi