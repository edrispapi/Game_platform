# Red Game Platform - Standardized Microservice Project Structure

## 📁 Complete Directory Structure

```
red-game/
├── services/                          # Microservices
│   ├── user-service/                  # User management & authentication
│   ├── game-catalog-service/          # Game library & search
│   ├── review-service/                # Reviews & comments
│   ├── shopping-service/              # Shopping cart & wishlist
│   ├── purchase-service/              # Order processing
│   ├── payment-service/               # Payment processing
│   ├── online-service/                # Online status & multiplayer
│   ├── social-service/                # Friends & social features
│   ├── notification-service/          # Notifications & templates
│   ├── recommendation-service/        # ML recommendations
│   ├── achievement-service/           # Achievements tracking
│   ├── monitoring-service/            # Monitoring & logging
│   └── api-gateway/                   # API Gateway
├── shared/                            # Shared utilities
├── docker-compose/                    # Docker configurations
│   └── postgres/                      # PostgreSQL init scripts
├── scripts/                           # Utility scripts
├── sample_data/                       # Generated sample data
├── templates/                         # Placeholder templates & future UI assets
├── tests/                             # Integration tests
├── requirements.txt                   # Global Python dependencies
├── requirements-global.txt            # Development tools
├── docker-compose.yml                 # Main Docker Compose file
├── docker-compose.prod.yml            # Production Docker Compose file
├── .env.example                       # Environment template
├── setup.sh                           # Setup script
├── README.md                          # Project documentation
├── PROJECT_STRUCTURE.md               # Detailed structure documentation
└── PROJECT_STRUCTURE_SUMMARY.md       # This file
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
| Notification Service | 8009 | 5440 | Notifications & templates |
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
| Redis | 6379 | Caching |
| Elasticsearch | 9200 | Search |
| Kafka | 9092 | Message queue |

## 🧾 Templates Directory

The `templates/` directory remains part of version control with a placeholder file. Use it to stage future UI, email, and notification assets without reworking downstream automation.
