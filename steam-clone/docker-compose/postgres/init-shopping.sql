-- Shopping Service Database Initialization
CREATE DATABASE shopping_service;
\c shopping_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE shopping_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;