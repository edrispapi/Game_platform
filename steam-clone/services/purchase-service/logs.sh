#!/bin/bash

# View Purchase Service logs
echo "Viewing Purchase Service logs..."

# Check if service is running
PID=$(lsof -t -i:8005)
if [ ! -z "$PID" ]; then
    echo "Service is running with PID: $PID"
    echo "Press Ctrl+C to stop viewing logs"
    tail -f /proc/$PID/fd/1
else
    echo "Purchase Service is not running."
    echo "Start the service first with ./start.sh"
fi