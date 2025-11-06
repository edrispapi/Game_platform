#!/bin/bash

# Stop Steam Clone Services
set -e

echo "🛑 Stopping Steam Clone services..."

# Stop all services
docker-compose down

echo "✅ Services stopped successfully!"