# Steam Clone - Microservices Platform

A comprehensive Steam-like gaming platform built with microservices architecture using FastAPI and PostgreSQL.

## 🎮 Features

- **User Management**: Registration, authentication, profiles, preferences
- **Game Catalog**: Game library, search, filtering, categories
- **Reviews & Comments**: User reviews, ratings, moderation
- **Shopping Cart**: Add/remove games, wishlist management
- **Purchase System**: Order processing, payment integration
- **Social Features**: Friends, chat, groups
- **Online Status**: Real-time presence, multiplayer support
- **Achievements**: Game achievements and progress tracking
- **Recommendations**: ML-based game recommendations
- **Notifications**: Real-time notifications system
- **Monitoring**: Comprehensive logging and metrics

## 🏗️ Architecture

### Microservices

1. **User Service** (Port 8001) - User management and authentication
2. **Game Catalog Service** (Port 8002) - Game library and search
3. **Review Service** (Port 8003) - Reviews and comments
4. **Shopping Service** (Port 8004) - Shopping cart and wishlist
5. **Purchase Service** (Port 8005) - Order processing
6. **Payment Service** (Port 8006) - Payment processing
7. **Online Service** (Port 8007) - Real-time online status
8. **Social Service** (Port 8008) - Friends and social features
9. **Notification Service** (Port 8009) - Notifications
10. **Recommendation Service** (Port 8010) - ML recommendations
11. **Achievement Service** (Port 8011) - Achievements tracking
12. **API Gateway** (Port 8000) - Single entry point

### Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Databases**: PostgreSQL (one per service)
- **Caching**: Redis
- **Search**: Elasticsearch
- **Message Queue**: Kafka
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (optional)

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd steam-clone
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables as needed
nano .env
```

### 3. Start with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access the Services

- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **User Service**: http://localhost:8001
- **Game Catalog Service**: http://localhost:8002
- **Redis**: localhost:6379
- **Elasticsearch**: http://localhost:9200
- **Kafka**: localhost:9092

## 🛠️ Development

### Local Development Setup

1. **Install Dependencies**

```bash
# Install global requirements
pip install -r requirements-global.txt

# Install service-specific requirements
cd services/user-service
pip install -r requirements.txt
```

2. **Start Infrastructure Services**

```bash
# Start only databases and supporting services
docker-compose up -d user-db game-catalog-db redis elasticsearch kafka
```

3. **Run Services Locally**

```bash
# User Service
cd services/user-service
uvicorn app.main:app --reload --port 8001

# Game Catalog Service
cd services/game-catalog-service
uvicorn app.main:app --reload --port 8002

# API Gateway
cd services/api-gateway
uvicorn app.main:app --reload --port 8000
```

### Database Migrations

```bash
# User Service
cd services/user-service
alembic upgrade head

# Game Catalog Service
cd services/game-catalog-service
alembic upgrade head
```

## 📊 Database Schema

Each service has its own PostgreSQL database:

- **user_service**: Users, sessions, preferences
- **game_catalog_service**: Games, genres, tags, platforms
- **review_service**: Reviews, comments, ratings
- **shopping_service**: Shopping carts, wishlists
- **purchase_service**: Orders, transactions
- **payment_service**: Payment methods, transactions
- **online_service**: Online status, multiplayer sessions
- **social_service**: Friends, groups, messages
- **notification_service**: Notifications, templates
- **recommendation_service**: User preferences, ML models
- **achievement_service**: Achievements, progress

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example`):

```bash
# Database URLs
USER_DATABASE_URL=postgresql://user:password@localhost:5432/user_service
GAME_CATALOG_DATABASE_URL=postgresql://user:password@localhost:5432/game_catalog_service

# Redis
REDIS_URL=redis://localhost:6379

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200

# Kafka
KAFKA_BROKER=localhost:9092

# JWT
SECRET_KEY=your-secret-key-here
```

## 🧪 Testing

```bash
# Run tests for a specific service
cd services/user-service
pytest

# Run all tests
pytest services/*/tests/
```

## 📈 Monitoring

- **Health Checks**: Each service provides `/health` endpoint
- **Logs**: Centralized logging via Docker Compose
- **Metrics**: Prometheus integration (optional)
- **Tracing**: OpenTelemetry support (optional)

## 🚀 Deployment

### Docker Compose (Development)

```bash
docker-compose up -d
```

### Kubernetes (Production)

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods
kubectl get services
```

## 📝 API Documentation

Each service provides interactive API documentation:

- **API Gateway**: http://localhost:8000/docs
- **User Service**: http://localhost:8001/docs
- **Game Catalog Service**: http://localhost:8002/docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the API docs at `/docs` endpoints

## 🗺️ Roadmap

- [ ] Complete all microservices
- [ ] Add comprehensive testing
- [ ] Implement monitoring and logging
- [ ] Add CI/CD pipeline
- [ ] Performance optimization
- [ ] Security enhancements
- [ ] Mobile app support