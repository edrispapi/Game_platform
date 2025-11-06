# Steam Clone - Standardized Microservice Project Structure

## 📁 Complete Directory Structure

```
red-game/
├── services/                          # Microservices
│   ├── user-service/                  # User management & authentication
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py               # FastAPI application
│   │   │   ├── models.py             # SQLAlchemy models
│   │   │   ├── schemas.py            # Pydantic schemas
│   │   │   ├── routes.py             # API routes
│   │   │   ├── crud.py               # Database operations
│   │   │   └── database.py           # Database configuration
│   │   ├── migrations/               # Alembic migrations
│   │   │   ├── env.py
│   │   │   └── script.py.mako
│   │   ├── tests/                    # Unit tests
│   │   ├── requirements.txt          # Service dependencies
│   │   ├── Dockerfile               # Service container
│   │   ├── alembic.ini              # Alembic configuration
│   │   ├── start.sh                 # Start script
│   │   ├── stop.sh                  # Stop script
│   │   ├── test.sh                  # Test script
│   │   └── logs.sh                  # Logs script
│   ├── game-catalog-service/         # Game library & search
│   │   ├── app/                     # Same structure as user-service
│   │   ├── migrations/              # Same structure as user-service
│   │   ├── tests/                   # Same structure as user-service
│   │   ├── requirements.txt         # Same structure as user-service
│   │   ├── Dockerfile              # Same structure as user-service
│   │   ├── alembic.ini             # Same structure as user-service
│   │   └── *.sh                    # Same scripts as user-service
│   ├── review-service/              # Reviews & comments
│   ├── shopping-service/            # Shopping cart & wishlist
│   ├── purchase-service/            # Order processing
│   ├── payment-service/             # Payment processing
│   ├── online-service/              # Online status & multiplayer
│   ├── social-service/              # Friends & social features
│   ├── notification-service/        # Notifications
│   ├── recommendation-service/      # ML recommendations
│   ├── achievement-service/         # Achievements tracking
│   ├── monitoring-service/          # Monitoring & logging
│   └── api-gateway/                 # API Gateway
│       ├── app/
│       │   ├── __init__.py
│       │   └── main.py
│       ├── requirements.txt
│       └── Dockerfile
├── shared/                           # Shared utilities
│   ├── __init__.py
│   ├── database.py                   # Database utilities
│   ├── auth.py                       # Authentication utilities
│   ├── models.py                     # Shared Pydantic models
│   └── config.py                     # Configuration settings
├── docker-compose/                   # Docker configurations
│   └── postgres/                     # PostgreSQL init scripts
│       ├── init-user.sql
│       ├── init-game-catalog.sql
│       ├── init-review.sql
│       ├── init-shopping.sql
│       ├── init-purchase.sql
│       ├── init-payment.sql
│       ├── init-online.sql
│       ├── init-social.sql
│       ├── init-notification.sql
│       ├── init-recommendation.sql
│       ├── init-achievement.sql
│       └── init-monitoring.sql
├── kubernetes/                       # Kubernetes manifests
├── docs/                            # Documentation
├── templates/                       # Frontend templates and static assets
├── tests/                           # Integration tests
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   ├── e2e/                         # End-to-end tests
│   ├── conftest.py                  # Pytest configuration
│   └── __init__.py
├── scripts/                         # Utility scripts
│   ├── start.sh                     # Start services
│   ├── stop.sh                      # Stop services
│   ├── restart.sh                   # Restart services
│   ├── logs.sh                      # View logs
│   └── create_service_template.py   # Service template generator
├── .github/                         # GitHub Actions
│   └── workflows/
│       ├── ci.yml                   # CI pipeline
│       └── deploy.yml               # Deployment pipeline
├── docker-compose.yml               # Main Docker Compose file
├── docker-compose.prod.yml          # Production Docker Compose file
├── requirements.txt                 # Global Python dependencies
├── requirements-global.txt          # Development tools
├── .env.example                     # Environment template
├── setup.sh                         # Setup script
├── README.md                        # Project documentation
├── PROJECT_STRUCTURE.md             # Detailed structure documentation
└── PROJECT_STRUCTURE_SUMMARY.md     # This file
```

## 🏗️ Standardized Service Structure

Each microservice follows this exact structure:

### Core Application Files
- `app/__init__.py` - Package initialization
- `app/main.py` - FastAPI application entry point
- `app/models.py` - SQLAlchemy database models
- `app/schemas.py` - Pydantic request/response schemas
- `app/routes.py` - API route definitions
- `app/crud.py` - Database CRUD operations
- `app/database.py` - Database configuration

### Database Migration Files
- `migrations/env.py` - Alembic environment configuration
- `migrations/script.py.mako` - Alembic migration template
- `alembic.ini` - Alembic configuration file

### Testing Files
- `tests/` - Service-specific test directory
- `conftest.py` - Pytest configuration (if needed)

### Configuration Files
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `alembic.ini` - Database migration configuration

### Shell Scripts
- `start.sh` - Start the service
- `stop.sh` - Stop the service
- `test.sh` - Run tests
- `logs.sh` - View logs

## 🔧 Service Ports

| Service | Port | Database Port | Description |
|---------|------|---------------|-------------|
| API Gateway | 8000 | - | Main entry point |
| User Service | 8001 | 5432 | User management |
| Game Catalog Service | 8002 | 5433 | Game library |
| Review Service | 8003 | 5434 | Reviews & comments |
| Shopping Service | 8004 | 5435 | Shopping cart |
| Purchase Service | 8005 | 5436 | Order processing |
| Payment Service | 8006 | 5437 | Payment processing |
| Online Service | 8007 | 5438 | Online status |
| Social Service | 8008 | 5439 | Social features |
| Notification Service | 8009 | 5440 | Notifications |
| Recommendation Service | 8010 | 5441 | ML recommendations |
| Achievement Service | 8011 | 5442 | Achievements |
| Monitoring Service | 8012 | 5443 | Monitoring |

## 🐳 Infrastructure Services

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL (User) | 5432 | User database |
| PostgreSQL (Game Catalog) | 5433 | Game catalog database |
| PostgreSQL (Review) | 5434 | Review database |
| PostgreSQL (Shopping) | 5435 | Shopping database |
| PostgreSQL (Purchase) | 5436 | Purchase database |
| PostgreSQL (Payment) | 5437 | Payment database |
| PostgreSQL (Online) | 5438 | Online database |
| PostgreSQL (Social) | 5439 | Social database |
| PostgreSQL (Notification) | 5440 | Notification database |
| PostgreSQL (Recommendation) | 5441 | Recommendation database |
| PostgreSQL (Achievement) | 5442 | Achievement database |
| PostgreSQL (Monitoring) | 5443 | Monitoring database |
| Redis | 6379 | Caching & sessions |
| Elasticsearch | 9200 | Search engine |
| Kafka | 9092 | Message queue |

## 🚀 Quick Start Commands

```bash
# Setup and start all services
./setup.sh

# Start services
./scripts/start.sh

# Stop services
./scripts/stop.sh

# Restart services
./scripts/restart.sh

# View logs
./scripts/logs.sh <service-name> [follow]

# Check service status
docker-compose ps

# View all logs
docker-compose logs -f

# Run tests
pytest tests/ -v

# Run specific service tests
cd services/user-service && ./test.sh
```

## 📊 Key Features Implemented

### ✅ Completed Services
- **User Service**: Complete with authentication, profiles, sessions
- **Game Catalog Service**: Complete with search, filtering, categories
- **Review Service**: Complete with reviews, comments, moderation
- **Shopping Service**: Complete with cart, wishlist, coupons
- **Purchase Service**: Complete with order processing, refunds
- **Payment Service**: Complete with payment methods, transactions
- **Online Service**: Complete with online status, multiplayer
- **Social Service**: Complete with friends, groups, messages
- **Notification Service**: Complete with notifications, templates
- **Recommendation Service**: Complete with ML recommendations
- **Achievement Service**: Complete with achievements tracking
- **Monitoring Service**: Complete with logging, metrics, alerts
- **API Gateway**: Complete with routing, rate limiting

### 🎯 Core Features
- Microservices architecture
- PostgreSQL databases per service
- Redis caching
- Elasticsearch search
- Kafka messaging
- Docker containerization
- API Gateway with rate limiting
- Comprehensive database schemas
- RESTful APIs with OpenAPI docs
- Health checks and monitoring
- Comprehensive testing framework
- CI/CD pipeline
- Production-ready configuration

## 🧪 Testing Framework

- **Unit Tests**: Individual service testing
- **Integration Tests**: Service-to-service testing
- **End-to-End Tests**: Full system testing
- **Pytest Configuration**: Centralized test configuration
- **Test Fixtures**: Reusable test data and setup
- **Coverage Reporting**: Code coverage tracking

## 🔄 CI/CD Pipeline

- **GitHub Actions**: Automated testing and deployment
- **Docker Builds**: Containerized service builds
- **Security Scanning**: Vulnerability scanning with Trivy
- **Code Quality**: Linting with flake8, black, isort
- **Test Coverage**: Coverage reporting with pytest-cov
- **Production Deployment**: Kubernetes deployment ready

## 📝 Documentation

- **README.md**: Main project documentation
- **PROJECT_STRUCTURE.md**: Detailed structure documentation
- **PROJECT_STRUCTURE_SUMMARY.md**: This summary
- **API Documentation**: Auto-generated OpenAPI docs
- **Service Documentation**: Individual service READMEs

## 🛠️ Development Tools

- **Service Template Generator**: Automated service creation
- **Shell Scripts**: Standardized service management
- **Environment Configuration**: Comprehensive .env.example
- **Database Migrations**: Alembic for all services
- **Docker Compose**: Development and production configurations

This standardized structure ensures consistency across all microservices, making development, testing, and deployment more efficient and maintainable.