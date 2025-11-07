"""Entry point for the simplified review service."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "service": "review-service"}


@app.get("/")
def root() -> dict:
    return {"message": "Review Service API", "version": "1.0.0"}


app.include_router(routes.router, prefix="/api/v1/reviews", tags=["reviews"])
