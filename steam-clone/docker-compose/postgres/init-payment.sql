-- Payment Service Database Initialization
CREATE DATABASE payment_service;
\c payment_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE payment_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;