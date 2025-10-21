"""
Game Catalog Service Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import routes, models, database
from .database import engine
from shared.config import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Game Catalog Service",
    description="Game catalog and search service for Steam-like platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(routes.router, prefix="/api/v1/catalog", tags=["catalog"])

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "game-catalog-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Game Catalog Service API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.GAME_CATALOG_SERVICE_PORT,
        reload=True
    )