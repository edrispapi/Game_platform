"""Simplified API gateway exposing frontend-focused aggregates."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Steam Clone API Gateway",
    description="API Gateway for Steam-like platform microservices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _hero_payload() -> dict:
    return {
        "title": "Build next-gen gaming experiences",
        "subtitle": "Craft, test, and ship multiplayer games with the Vibe Coding AI toolkit.",
        "primary_cta": "Start building",
        "secondary_cta": "Explore marketplace",
    }


def _trending_games() -> list:
    return [
        {
            "id": "demo-1",
            "title": "Neon Racers",
            "genre": "Racing",
            "description": "Boost through synthwave skylines with co-op rivals.",
            "price": 19.99,
            "discount_percent": 15,
            "capsule_image_url": "https://placehold.co/300x400?text=Neon",
        },
        {
            "id": "demo-2",
            "title": "Stellar Forge",
            "genre": "Strategy",
            "description": "Build, automate, and defend an interstellar factory fleet.",
            "price": 29.99,
            "discount_percent": 0,
            "capsule_image_url": "https://placehold.co/300x400?text=Forge",
        },
    ]


def _discover_sections() -> list:
    return [
        {
            "title": "AI assisted tooling",
            "items": [
                {
                    "label": "Prompt-to-gameplay",
                    "description": "Generate gameplay scaffolds and asset stubs directly from natural language prompts.",
                },
                {
                    "label": "Live balance feedback",
                    "description": "Surface telemetry insights while you tweak combat values in the editor.",
                },
            ],
        },
        {
            "title": "Launch ready",
            "items": [
                {
                    "label": "Marketplace integration",
                    "description": "Publish to web and desktop clients with managed billing and entitlement services.",
                },
                {
                    "label": "Player community",
                    "description": "Enable chat, parties, and achievements backed by the social microservice suite.",
                },
            ],
        },
    ]


def _testimonial_cards() -> list:
    return [
        {
            "quote": "Our team shipped a multiplayer prototype in a weekend thanks to the unified toolkit.",
            "author": "Indie Collective",
            "rating": 5,
            "game_id": "demo-1",
        },
        {
            "quote": "The live dashboards keep our designers and analysts aligned during playtests.",
            "author": "Solar Studios",
            "rating": 4,
            "game_id": "demo-2",
        },
    ]


def _dashboard_assets() -> list:
    return [
        {"name": "environment.glb", "type": "3D Model", "size": "2.3 MB"},
        {"name": "soundtrack.wav", "type": "Audio", "size": "5.1 MB"},
        {"name": "abilities.json", "type": "Config", "size": "8 KB"},
    ]


def _share_links() -> list:
    base_url = "https://example.com/vibe"
    return [
        {"label": "Live preview", "url": f"{base_url}/preview"},
        {"label": "Download build", "url": f"{base_url}/build.zip"},
        {"label": "Invite collaborators", "url": f"{base_url}/invite"},
    ]


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "service": "api-gateway"}


@app.get("/")
def root() -> dict:
    return {
        "message": "Steam Clone API Gateway",
        "version": "1.0.0",
        "services": ["/api/v1/frontend/home", "/api/v1/frontend/dashboard"],
    }


@app.get("/api/v1/frontend/home")
def frontend_home(request: Request) -> dict:
    # Basic rate limiting analogue: allow up to 120 requests per minute per client.
    counter = getattr(request, "_rate_counter", 0)
    if counter > 120:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    setattr(request, "_rate_counter", counter + 1)

    return {
        "hero": _hero_payload(),
        "trending": _trending_games(),
        "discover": _discover_sections(),
        "testimonials": _testimonial_cards(),
    }


@app.get("/api/v1/frontend/dashboard")
def frontend_dashboard(request: Request) -> dict:
    counter = getattr(request, "_rate_counter", 0)
    if counter > 120:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    setattr(request, "_rate_counter", counter + 1)

    return {
        "script": "// Game loop entry\nfunction update(dt) { /* ... */ }",
        "build_status": {
            "progress": 0.68,
            "message": "Building Windows x64 artifact",
            "eta_seconds": 75,
        },
        "assets": _dashboard_assets(),
        "share_links": _share_links(),
    }
