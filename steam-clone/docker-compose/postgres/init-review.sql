-- Review Service Database Initialization
CREATE DATABASE review_service;
\c review_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE review_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;