-- Recommendation Service Database Initialization
CREATE DATABASE recommendation_service;
\c recommendation_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE recommendation_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;