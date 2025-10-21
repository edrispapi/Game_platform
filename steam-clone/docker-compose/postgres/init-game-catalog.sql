-- Game Catalog Service Database Initialization
CREATE DATABASE game_catalog_service;
\c game_catalog_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable GIN extension for full-text search
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE game_catalog_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;