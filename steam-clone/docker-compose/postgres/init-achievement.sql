-- Achievement Service Database Initialization
CREATE DATABASE achievement_service;
\c achievement_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE achievement_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;