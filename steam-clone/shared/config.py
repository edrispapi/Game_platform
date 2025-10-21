"""
Shared configuration settings
"""
import os
from typing import List

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/steamdb")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Kafka settings
    KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "localhost:9092")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Elasticsearch settings
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    
    # Service ports
    USER_SERVICE_PORT: int = int(os.getenv("USER_SERVICE_PORT", "8001"))
    GAME_CATALOG_SERVICE_PORT: int = int(os.getenv("GAME_CATALOG_SERVICE_PORT", "8002"))
    REVIEW_SERVICE_PORT: int = int(os.getenv("REVIEW_SERVICE_PORT", "8003"))
    SHOPPING_SERVICE_PORT: int = int(os.getenv("SHOPPING_SERVICE_PORT", "8004"))
    PURCHASE_SERVICE_PORT: int = int(os.getenv("PURCHASE_SERVICE_PORT", "8005"))
    PAYMENT_SERVICE_PORT: int = int(os.getenv("PAYMENT_SERVICE_PORT", "8006"))
    ONLINE_SERVICE_PORT: int = int(os.getenv("ONLINE_SERVICE_PORT", "8007"))
    SOCIAL_SERVICE_PORT: int = int(os.getenv("SOCIAL_SERVICE_PORT", "8008"))
    NOTIFICATION_SERVICE_PORT: int = int(os.getenv("NOTIFICATION_SERVICE_PORT", "8009"))
    RECOMMENDATION_SERVICE_PORT: int = int(os.getenv("RECOMMENDATION_SERVICE_PORT", "8010"))
    ACHIEVEMENT_SERVICE_PORT: int = int(os.getenv("ACHIEVEMENT_SERVICE_PORT", "8011"))
    API_GATEWAY_PORT: int = int(os.getenv("API_GATEWAY_PORT", "8000"))
    MONITORING_SERVICE_PORT: int = int(os.getenv("MONITORING_SERVICE_PORT", "8012"))
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # File upload settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif"]

settings = Settings()