-- Purchase Service Database Initialization
CREATE DATABASE purchase_service;
\c purchase_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE purchase_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;