#!/bin/bash

# Steam Clone Setup Script
set -e

echo "🎮 Setting up Steam Clone Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update as needed."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p docker-compose/postgres
mkdir -p logs
mkdir -p data

# Set permissions
echo "🔐 Setting permissions..."
chmod +x setup.sh
chmod +x scripts/*.sh 2>/dev/null || true

# Build and start services
echo "🐳 Building and starting services..."
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
services=("user-service" "game-catalog-service" "api-gateway" "redis" "elasticsearch")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is not running"
    fi
done

# Run database migrations
echo "🗄️ Running database migrations..."
# Note: In a real setup, you would run Alembic migrations here

echo "🎉 Setup complete!"
echo ""
echo "🌐 Access the platform:"
echo "   API Gateway: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   User Service: http://localhost:8001"
echo "   Game Catalog: http://localhost:8002"
echo ""
echo "📊 Infrastructure:"
echo "   Redis: localhost:6379"
echo "   Elasticsearch: http://localhost:9200"
echo "   Kafka: localhost:9092"
echo ""
echo "🔧 Management commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   View status: docker-compose ps"