# Steam Clone Project Structure

## 📁 Directory Structure

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
│   │   ├── tests/                    # Unit tests
│   │   ├── requirements.txt          # Service dependencies
│   │   └── Dockerfile               # Service container
│   ├── game-catalog-service/         # Game library & search
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── crud.py
│   │   │   └── database.py
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── review-service/               # Reviews & comments
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── crud.py
│   │   │   └── database.py
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── shopping-service/             # Shopping cart & wishlist
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── crud.py
│   │   │   └── database.py
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── purchase-service/             # Order processing
│   ├── payment-service/              # Payment processing
│   ├── online-service/               # Online status & multiplayer
│   ├── social-service/               # Friends & social features
│   ├── notification-service/         # Notifications
│   ├── recommendation-service/       # ML recommendations
│   ├── achievement-service/          # Achievements tracking
│   ├── api-gateway/                  # API Gateway
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── monitoring-service/           # Monitoring & logging
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
│       └── init-achievement.sql
├── kubernetes/                       # Kubernetes manifests
├── docs/                            # Documentation
├── templates/                       # Frontend templates and static assets
├── tests/                           # Integration tests
├── scripts/                         # Utility scripts
│   ├── start.sh                     # Start services
│   ├── stop.sh                      # Stop services
│   ├── restart.sh                   # Restart services
│   └── logs.sh                      # View logs
├── docker-compose.yml               # Main Docker Compose file
├── requirements.txt                 # Global Python dependencies
├── requirements-global.txt          # Development tools
├── .env.example                     # Environment template
├── setup.sh                         # Setup script
└── README.md                        # Project documentation
```

## 🗄️ Database Architecture

Each microservice has its own PostgreSQL database:

### User Service Database (user_service)
- **users**: User accounts and profiles
- **user_sessions**: Active user sessions
- **user_preferences**: User settings and preferences

### Game Catalog Service Database (game_catalog_service)
- **games**: Game information and metadata
- **genres**: Game genres
- **tags**: Game tags
- **platforms**: Supported platforms
- **game_reviews**: Game reviews (denormalized)
- **game_achievements**: Game achievements
- **game_dlcs**: DLC relationships
- **game_bundles**: Game bundles

### Review Service Database (review_service)
- **reviews**: User reviews
- **review_comments**: Review comments
- **review_votes**: Review helpfulness votes
- **comment_votes**: Comment helpfulness votes
- **review_reports**: Review reports
- **review_moderation_logs**: Moderation history

### Shopping Service Database (shopping_service)
- **shopping_carts**: Shopping carts
- **cart_items**: Cart items
- **wishlists**: User wishlists
- **wishlist_items**: Wishlist items
- **coupons**: Discount coupons
- **coupon_usage**: Coupon usage tracking
- **price_alerts**: Price drop alerts

## 🔧 Service Ports

| Service | Port | Description |
|---------|------|-------------|
| API Gateway | 8000 | Main entry point |
| User Service | 8001 | User management |
| Game Catalog Service | 8002 | Game library |
| Review Service | 8003 | Reviews & comments |
| Shopping Service | 8004 | Shopping cart |
| Purchase Service | 8005 | Order processing |
| Payment Service | 8006 | Payment processing |
| Online Service | 8007 | Online status |
| Social Service | 8008 | Social features |
| Notification Service | 8009 | Notifications |
| Recommendation Service | 8010 | ML recommendations |
| Achievement Service | 8011 | Achievements |
| Monitoring Service | 8012 | Monitoring |

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
```

## 📊 Key Features Implemented

### ✅ Completed Services
- **User Service**: Complete with authentication, profiles, sessions
- **Game Catalog Service**: Complete with search, filtering, categories
- **Review Service**: Complete with reviews, comments, moderation
- **Shopping Service**: Complete with cart, wishlist, coupons
- **API Gateway**: Complete with routing, rate limiting

### 🔄 In Progress
- Purchase Service
- Payment Service
- Online Service
- Social Service
- Notification Service
- Recommendation Service
- Achievement Service
- Monitoring Service

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