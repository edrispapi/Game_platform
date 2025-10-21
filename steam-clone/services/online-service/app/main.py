"""
Online status and multiplayer service for Steam-like platform
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import routes, models, database
from .database import engine, get_db
from shared.config import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Online Service",
    description="Online status and multiplayer service for Steam-like platform",
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
app.include_router(routes.router, prefix="/api/v1/online", tags=["online"])

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "online-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Online Service API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.ONLINE_SERVICE_SERVICE_PORT,
        reload=True
    )
