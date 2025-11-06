#!/bin/bash

# Restart Purchase Service
echo "Restarting Purchase Service..."

# Stop the service
./stop.sh

# Wait a moment
sleep 2

# Start the service
./start.sh