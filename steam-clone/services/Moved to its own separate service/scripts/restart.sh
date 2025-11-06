#!/bin/bash

# Restart Steam Clone Services
set -e

echo "🔄 Restarting Steam Clone services..."

# Stop services
docker-compose down

# Start services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 20

# Check service health
echo "🏥 Checking service health..."
services=("user-service" "game-catalog-service" "api-gateway")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is not running"
        echo "   Check logs: docker-compose logs $service"
    fi
done

echo "🎉 Services restarted successfully!"