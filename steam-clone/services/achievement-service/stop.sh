#!/bin/bash

# Achievement Service Stop Script

echo "Stopping Achievement Service..."

# Find and kill the process running on port 8011
PID=$(lsof -t -i:8011)
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port 8011..."
    kill -9 $PID
    echo "Achievement Service stopped."
else
    echo "No process found running on port 8011."
fi
