#!/usr/bin/env python3
"""
Service Template Generator
Creates standardized microservice structure for all services
"""

import os
import sys
from pathlib import Path

# Service configurations
SERVICES = {
    "payment-service": {
        "port": 8006,
        "db_port": 5437,
        "description": "Payment processing service for Steam-like platform",
        "models": ["Payment", "PaymentMethod", "Transaction"],
        "routes": ["payments", "payment-methods", "transactions"]
    },
    "online-service": {
        "port": 8007,
        "db_port": 5438,
        "description": "Online status and multiplayer service for Steam-like platform",
        "models": ["OnlineStatus", "GameSession", "MultiplayerRoom"],
        "routes": ["online", "sessions", "multiplayer"]
    },
    "social-service": {
        "port": 8008,
        "db_port": 5439,
        "description": "Social features and friends service for Steam-like platform",
        "models": ["Friend", "FriendRequest", "Group", "Message"],
        "routes": ["friends", "groups", "messages"]
    },
    "notification-service": {
        "port": 8009,
        "db_port": 5440,
        "description": "Notifications service for Steam-like platform",
        "models": ["Notification", "NotificationTemplate", "UserNotification"],
        "routes": ["notifications", "templates", "user-notifications"]
    },
    "recommendation-service": {
        "port": 8010,
        "db_port": 5441,
        "description": "ML-based recommendations service for Steam-like platform",
        "models": ["Recommendation", "UserPreference", "MLModel"],
        "routes": ["recommendations", "preferences", "models"]
    },
    "achievement-service": {
        "port": 8011,
        "db_port": 5442,
        "description": "Achievements tracking service for Steam-like platform",
        "models": ["Achievement", "UserAchievement", "GameAchievement"],
        "routes": ["achievements", "user-achievements", "game-achievements"]
    },
    "monitoring-service": {
        "port": 8012,
        "db_port": 5443,
        "description": "Monitoring and logging service for Steam-like platform",
        "models": ["LogEntry", "Metric", "Alert"],
        "routes": ["logs", "metrics", "alerts"]
    }
}

def create_service_structure(service_name, config):
    """Create standardized service structure"""
    service_dir = Path(f"services/{service_name}")
    app_dir = service_dir / "app"
    migrations_dir = service_dir / "migrations"
    
    # Create directories
    app_dir.mkdir(parents=True, exist_ok=True)
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    (app_dir / "__init__.py").write_text('"""\n' + config["description"] + '\n"""\n')
    
    # Create main.py
    main_content = f'''"""
{config["description"]}
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
    title="{service_name.replace('-', ' ').title()}",
    description="{config['description']}",
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
app.include_router(routes.router, prefix="/api/v1/{service_name.split('-')[0]}", tags=["{service_name.split('-')[0]}"])

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "service": "{service_name}"}}

@app.get("/")
def root():
    """Root endpoint"""
    return {{"message": "{service_name.replace('-', ' ').title()} API", "version": "1.0.0"}}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.{service_name.replace('-', '_').upper()}_SERVICE_PORT,
        reload=True
    )
'''
    (app_dir / "main.py").write_text(main_content)
    
    # Create models.py
    models_content = f'''"""
{service_name.replace('-', ' ').title()} Database Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Add your models here
# Example:
# class {config['models'][0]}(Base):
#     __tablename__ = "{config['models'][0].lower()}s"
#     
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''
    (app_dir / "models.py").write_text(models_content)
    
    # Create schemas.py
    schemas_content = f'''"""
{service_name.replace('-', ' ').title()} Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Add your schemas here
# Example:
# class {config['models'][0]}Base(BaseModel):
#     pass
# 
# class {config['models'][0]}Create({config['models'][0]}Base):
#     pass
# 
# class {config['models'][0]}Response({config['models'][0]}Base):
#     id: str
#     created_at: datetime
#     
#     class Config:
#         from_attributes = True
'''
    (app_dir / "schemas.py").write_text(schemas_content)
    
    # Create database.py
    database_content = f'''"""
{service_name.replace('-', ' ').title()} Database Configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from shared.config import settings

# Database URL
DATABASE_URL = os.getenv("{service_name.replace('-', '_').upper()}_DATABASE_URL", f"postgresql://user:password@localhost:{config['db_port']}/{service_name.replace('-', '_')}_service")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    (app_dir / "database.py").write_text(database_content)
    
    # Create crud.py
    crud_content = f'''"""
{service_name.replace('-', ' ').title()} CRUD Operations
"""
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# Add your CRUD operations here
# Example:
# def create_{config['models'][0].lower()}(db: Session, {config['models'][0].lower()}: schemas.{config['models'][0]}Create) -> models.{config['models'][0]}:
#     """Create a new {config['models'][0].lower()}"""
#     db_{config['models'][0].lower()} = models.{config['models'][0]}()
#     db.add(db_{config['models'][0].lower()})
#     db.commit()
#     db.refresh(db_{config['models'][0].lower()})
#     return db_{config['models'][0].lower()}
'''
    (app_dir / "crud.py").write_text(crud_content)
    
    # Create routes.py
    routes_content = f'''"""
{service_name.replace('-', ' ').title()} API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()

# Add your routes here
# Example:
# @router.post("/", response_model=schemas.{config['models'][0]}Response, status_code=status.HTTP_201_CREATED)
# def create_{config['models'][0].lower()}(
#     {config['models'][0].lower()}: schemas.{config['models'][0]}Create,
#     db: Session = Depends(database.get_db)
# ):
#     """Create a new {config['models'][0].lower()}"""
#     return crud.create_{config['models'][0].lower()}(db=db, {config['models'][0].lower()}={config['models'][0].lower()})
'''
    (app_dir / "routes.py").write_text(routes_content)
    
    # Create requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
redis==5.0.1
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
'''
    (service_dir / "requirements.txt").write_text(requirements_content)
    
    # Create Dockerfile
    dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE {config['port']}

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "{config['port']}"]
'''
    (service_dir / "Dockerfile").write_text(dockerfile_content)
    
    # Create alembic.ini
    alembic_content = f'''# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = migrations

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version number format
version_num_format = %04d

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses
# os.pathsep. If this key is omitted entirely, it falls back to the legacy
# behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = postgresql://user:password@localhost:{config['db_port']}/{service_name.replace('-', '_')}_service


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
    (service_dir / "alembic.ini").write_text(alembic_content)
    
    # Create migrations/env.py
    env_content = f'''"""
Alembic Environment Configuration
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the parent directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base
from shared.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    """Get database URL from environment or config"""
    return os.getenv("{service_name.replace('-', '_').upper()}_DATABASE_URL", "postgresql://user:password@localhost:{config['db_port']}/{service_name.replace('-', '_')}_service")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={{"paramstyle": "named"}},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
    (migrations_dir / "env.py").write_text(env_content)
    
    # Create migrations/script.py.mako
    script_mako_content = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
'''
    (migrations_dir / "script.py.mako").write_text(script_mako_content)
    
    # Create shell scripts
    create_shell_scripts(service_dir, service_name, config)

def create_shell_scripts(service_dir, service_name, config):
    """Create shell scripts for the service"""
    
    # start.sh
    start_content = f'''#!/bin/bash

# {service_name.replace('-', ' ').title()} Start Script

echo "Starting {service_name.replace('-', ' ').title()}..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the service
echo "Starting {service_name.replace('-', ' ').title()} on port {config['port']}..."
uvicorn app.main:app --host 0.0.0.0 --port {config['port']} --reload
'''
    (service_dir / "start.sh").write_text(start_content)
    
    # stop.sh
    stop_content = f'''#!/bin/bash

# {service_name.replace('-', ' ').title()} Stop Script

echo "Stopping {service_name.replace('-', ' ').title()}..."

# Find and kill the process running on port {config['port']}
PID=$(lsof -t -i:{config['port']})
if [ ! -z "$PID" ]; then
    echo "Killing process $PID on port {config['port']}..."
    kill -9 $PID
    echo "{service_name.replace('-', ' ').title()} stopped."
else
    echo "No process found running on port {config['port']}."
fi
'''
    (service_dir / "stop.sh").write_text(stop_content)
    
    # test.sh
    test_content = f'''#!/bin/bash

# {service_name.replace('-', ' ').title()} Test Script

echo "Running {service_name.replace('-', ' ').title()} tests..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install test dependencies
echo "Installing test dependencies..."
pip install pytest pytest-asyncio httpx

# Run tests
echo "Running tests..."
pytest tests/ -v

echo "Tests completed."
'''
    (service_dir / "test.sh").write_text(test_content)
    
    # logs.sh
    logs_content = f'''#!/bin/bash

# {service_name.replace('-', ' ').title()} Logs Script

echo "Showing {service_name.replace('-', ' ').title()} logs..."

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container..."
    tail -f /var/log/{service_name}.log
else
    # Check if service is running
    PID=$(lsof -t -i:{config['port']})
    if [ ! -z "$PID" ]; then
        echo "Service is running with PID: $PID"
        echo "Use 'docker-compose logs {service_name}' to view logs"
    else
        echo "Service is not running."
    fi
fi
'''
    (service_dir / "logs.sh").write_text(logs_content)
    
    # Make scripts executable
    os.chmod(service_dir / "start.sh", 0o755)
    os.chmod(service_dir / "stop.sh", 0o755)
    os.chmod(service_dir / "test.sh", 0o755)
    os.chmod(service_dir / "logs.sh", 0o755)

def main():
    """Main function to create all services"""
    print("Creating standardized microservice structure...")
    
    for service_name, config in SERVICES.items():
        print(f"Creating {service_name}...")
        create_service_structure(service_name, config)
        print(f"✓ {service_name} created successfully")
    
    print("\nAll services created successfully!")
    print("\nNext steps:")
    print("1. Update docker-compose.yml to include all services")
    print("2. Update shared/config.py with service ports")
    print("3. Create .env.example file")
    print("4. Run database migrations for each service")

if __name__ == "__main__":
    main()