-- Online Service Database Initialization
CREATE DATABASE online_service;
\c online_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE online_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;

-- Create tables
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'online', -- 'online', 'away', 'busy', 'invisible', 'offline'
    game_id INTEGER,
    game_name VARCHAR(500),
    server_name VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS multiplayer_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id INTEGER NOT NULL,
    host_user_id UUID NOT NULL,
    session_name VARCHAR(200) NOT NULL,
    max_players INTEGER DEFAULT 4,
    current_players INTEGER DEFAULT 1,
    is_public BOOLEAN DEFAULT TRUE,
    password VARCHAR(100),
    status VARCHAR(20) DEFAULT 'waiting', -- 'waiting', 'in_progress', 'finished', 'cancelled'
    server_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    ended_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS session_participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES multiplayer_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    left_at TIMESTAMP,
    is_host BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS game_servers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    ip_address INET NOT NULL,
    port INTEGER NOT NULL,
    max_players INTEGER DEFAULT 32,
    current_players INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    region VARCHAR(50),
    server_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS server_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    server_id UUID REFERENCES game_servers(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    network_in DECIMAL(10,2),
    network_out DECIMAL(10,2),
    active_connections INTEGER DEFAULT 0
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_session_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_status ON user_sessions(status);
CREATE INDEX IF NOT EXISTS idx_user_sessions_game_id ON user_sessions(game_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_last_activity ON user_sessions(last_activity);
CREATE INDEX IF NOT EXISTS idx_user_sessions_created_at ON user_sessions(created_at);

CREATE INDEX IF NOT EXISTS idx_multiplayer_sessions_game_id ON multiplayer_sessions(game_id);
CREATE INDEX IF NOT EXISTS idx_multiplayer_sessions_host_user_id ON multiplayer_sessions(host_user_id);
CREATE INDEX IF NOT EXISTS idx_multiplayer_sessions_is_public ON multiplayer_sessions(is_public);
CREATE INDEX IF NOT EXISTS idx_multiplayer_sessions_status ON multiplayer_sessions(status);
CREATE INDEX IF NOT EXISTS idx_multiplayer_sessions_created_at ON multiplayer_sessions(created_at);

CREATE INDEX IF NOT EXISTS idx_session_participants_session_id ON session_participants(session_id);
CREATE INDEX IF NOT EXISTS idx_session_participants_user_id ON session_participants(user_id);
CREATE INDEX IF NOT EXISTS idx_session_participants_is_host ON session_participants(is_host);
CREATE INDEX IF NOT EXISTS idx_session_participants_joined_at ON session_participants(joined_at);

CREATE INDEX IF NOT EXISTS idx_game_servers_game_id ON game_servers(game_id);
CREATE INDEX IF NOT EXISTS idx_game_servers_ip_address ON game_servers(ip_address);
CREATE INDEX IF NOT EXISTS idx_game_servers_is_active ON game_servers(is_active);
CREATE INDEX IF NOT EXISTS idx_game_servers_region ON game_servers(region);
CREATE INDEX IF NOT EXISTS idx_game_servers_created_at ON game_servers(created_at);

CREATE INDEX IF NOT EXISTS idx_server_stats_server_id ON server_stats(server_id);
CREATE INDEX IF NOT EXISTS idx_server_stats_timestamp ON server_stats(timestamp);

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_sessions_updated_at BEFORE UPDATE ON user_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_multiplayer_sessions_updated_at BEFORE UPDATE ON multiplayer_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_game_servers_updated_at BEFORE UPDATE ON game_servers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();