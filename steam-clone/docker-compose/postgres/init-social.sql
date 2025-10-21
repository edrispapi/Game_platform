-- Social Service Database Initialization
CREATE DATABASE social_service;
\c social_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE social_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;