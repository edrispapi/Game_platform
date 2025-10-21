-- User Service Database Initialization
CREATE DATABASE user_service;
\c user_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user_preferences schema
CREATE SCHEMA IF NOT EXISTS user_preferences;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE user_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;
GRANT ALL PRIVILEGES ON SCHEMA user_preferences TO user;