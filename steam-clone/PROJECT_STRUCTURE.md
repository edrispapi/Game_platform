# Red Game Platform Project Structure

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
│   │   └── Dockerfile                # Service container
│   ├── game-catalog-service/         # Game library & search
│   ├── review-service/               # Reviews & comments
│   ├── shopping-service/             # Shopping cart & wishlist
│   ├── purchase-service/             # Order processing
│   ├── payment-service/              # Payment processing
│   ├── online-service/               # Online status & multiplayer
│   ├── social-service/               # Friends & social features
│   ├── notification-service/         # Notifications & templates
│   ├── recommendation-service/       # ML recommendations
│   ├── achievement-service/          # Achievements tracking
│   ├── monitoring-service/           # Monitoring & logging
│   └── api-gateway/                  # API Gateway entry point
├── shared/                           # Shared utilities
├── docker-compose/                   # Docker configurations
│   └── postgres/                     # PostgreSQL init scripts
├── scripts/                          # Utility & automation scripts
├── sample_data/                      # Generated sample data
├── templates/                        # Placeholder assets for future UI work
├── tests/                            # Integration tests
├── docker-compose.yml                # Main Docker Compose file
├── requirements.txt                  # Global Python dependencies
├── requirements-global.txt           # Development tools
├── .env.example                      # Environment template
├── setup.sh                          # Setup script
└── README.md                         # Project documentation
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
| Notification Service | 8009 | Notifications & templates |
| Recommendation Service | 8010 | ML recommendations |
| Achievement Service | 8011 | Achievements |
| Monitoring Service | 8012 | Monitoring & logging |

## 🧾 Templates Directory

The `templates/` folder is tracked to support future UI and notification assets. It currently contains placeholder content so downstream tooling can depend on the path even before front-end resources are added back in.
