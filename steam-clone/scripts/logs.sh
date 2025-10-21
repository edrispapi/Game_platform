#!/bin/bash

# View Steam Clone Service Logs
set -e

if [ $# -eq 0 ]; then
    echo "📋 Available services:"
    echo "   user-service, game-catalog-service, api-gateway, redis, elasticsearch, kafka"
    echo ""
    echo "Usage: $0 <service-name> [follow]"
    echo "Example: $0 user-service follow"
    exit 1
fi

SERVICE=$1
FOLLOW=${2:-""}

if [ "$FOLLOW" = "follow" ]; then
    echo "📋 Following logs for $SERVICE (Ctrl+C to stop)..."
    docker-compose logs -f $SERVICE
else
    echo "📋 Recent logs for $SERVICE:"
    docker-compose logs --tail=100 $SERVICE
fi