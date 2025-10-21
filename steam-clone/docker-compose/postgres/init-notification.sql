-- Notification Service Database Initialization
CREATE DATABASE notification_service;
\c notification_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE notification_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;