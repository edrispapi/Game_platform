-- Game Catalog Service Database Initialization
CREATE DATABASE game_catalog_service;
\c game_catalog_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable GIN extension for full-text search
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE game_catalog_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;

-- Create tables
CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS platforms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    steam_app_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(500) NOT NULL,
    type VARCHAR(50) DEFAULT 'game',
    price DECIMAL(10,2) DEFAULT 0.00,
    discount DECIMAL(5,2) DEFAULT 0.00,
    final_price DECIMAL(10,2) DEFAULT 0.00,
    currency VARCHAR(10) DEFAULT 'USD',
    release_date DATE,
    developer VARCHAR(200),
    publisher VARCHAR(200),
    description TEXT,
    short_description TEXT,
    header_image TEXT,
    capsule_image TEXT,
    background TEXT,
    metacritic_score INTEGER,
    steam_score INTEGER,
    positive_reviews INTEGER DEFAULT 0,
    negative_reviews INTEGER DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    achievements INTEGER DEFAULT 0,
    dlc_count INTEGER DEFAULT 0,
    is_free BOOLEAN DEFAULT FALSE,
    is_early_access BOOLEAN DEFAULT FALSE,
    is_vr_supported BOOLEAN DEFAULT FALSE,
    is_multiplayer BOOLEAN DEFAULT FALSE,
    is_singleplayer BOOLEAN DEFAULT FALSE,
    is_coop BOOLEAN DEFAULT FALSE,
    is_online_coop BOOLEAN DEFAULT FALSE,
    is_local_coop BOOLEAN DEFAULT FALSE,
    is_pvp BOOLEAN DEFAULT FALSE,
    is_mmo BOOLEAN DEFAULT FALSE,
    is_strategy BOOLEAN DEFAULT FALSE,
    is_rpg BOOLEAN DEFAULT FALSE,
    is_action BOOLEAN DEFAULT FALSE,
    is_adventure BOOLEAN DEFAULT FALSE,
    is_simulation BOOLEAN DEFAULT FALSE,
    is_sports BOOLEAN DEFAULT FALSE,
    is_racing BOOLEAN DEFAULT FALSE,
    is_fighting BOOLEAN DEFAULT FALSE,
    is_puzzle BOOLEAN DEFAULT FALSE,
    is_horror BOOLEAN DEFAULT FALSE,
    is_indie BOOLEAN DEFAULT FALSE,
    is_casual BOOLEAN DEFAULT FALSE,
    is_educational BOOLEAN DEFAULT FALSE,
    is_utilities BOOLEAN DEFAULT FALSE,
    is_web BOOLEAN DEFAULT FALSE,
    is_software BOOLEAN DEFAULT FALSE,
    is_video BOOLEAN DEFAULT FALSE,
    is_music BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game_genres (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id, genre_id)
);

CREATE TABLE IF NOT EXISTS game_tags (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id, tag_id)
);

CREATE TABLE IF NOT EXISTS game_platforms (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    platform_id INTEGER REFERENCES platforms(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id, platform_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_games_steam_app_id ON games(steam_app_id);
CREATE INDEX IF NOT EXISTS idx_games_name ON games(name);
CREATE INDEX IF NOT EXISTS idx_games_price ON games(price);
CREATE INDEX IF NOT EXISTS idx_games_release_date ON games(release_date);
CREATE INDEX IF NOT EXISTS idx_games_steam_score ON games(steam_score);
CREATE INDEX IF NOT EXISTS idx_games_is_free ON games(is_free);
CREATE INDEX IF NOT EXISTS idx_games_is_early_access ON games(is_early_access);
CREATE INDEX IF NOT EXISTS idx_games_is_vr_supported ON games(is_vr_supported);
CREATE INDEX IF NOT EXISTS idx_games_is_multiplayer ON games(is_multiplayer);
CREATE INDEX IF NOT EXISTS idx_games_is_singleplayer ON games(is_singleplayer);
CREATE INDEX IF NOT EXISTS idx_games_is_coop ON games(is_coop);
CREATE INDEX IF NOT EXISTS idx_games_is_pvp ON games(is_pvp);
CREATE INDEX IF NOT EXISTS idx_games_is_mmo ON games(is_mmo);
CREATE INDEX IF NOT EXISTS idx_games_is_strategy ON games(is_strategy);
CREATE INDEX IF NOT EXISTS idx_games_is_rpg ON games(is_rpg);
CREATE INDEX IF NOT EXISTS idx_games_is_action ON games(is_action);
CREATE INDEX IF NOT EXISTS idx_games_is_adventure ON games(is_adventure);
CREATE INDEX IF NOT EXISTS idx_games_is_simulation ON games(is_simulation);
CREATE INDEX IF NOT EXISTS idx_games_is_sports ON games(is_sports);
CREATE INDEX IF NOT EXISTS idx_games_is_racing ON games(is_racing);
CREATE INDEX IF NOT EXISTS idx_games_is_fighting ON games(is_fighting);
CREATE INDEX IF NOT EXISTS idx_games_is_puzzle ON games(is_puzzle);
CREATE INDEX IF NOT EXISTS idx_games_is_horror ON games(is_horror);
CREATE INDEX IF NOT EXISTS idx_games_is_indie ON games(is_indie);
CREATE INDEX IF NOT EXISTS idx_games_is_casual ON games(is_casual);
CREATE INDEX IF NOT EXISTS idx_games_is_educational ON games(is_educational);
CREATE INDEX IF NOT EXISTS idx_games_is_utilities ON games(is_utilities);
CREATE INDEX IF NOT EXISTS idx_games_is_web ON games(is_web);
CREATE INDEX IF NOT EXISTS idx_games_is_software ON games(is_software);
CREATE INDEX IF NOT EXISTS idx_games_is_video ON games(is_video);
CREATE INDEX IF NOT EXISTS idx_games_is_music ON games(is_music);
CREATE INDEX IF NOT EXISTS idx_games_created_at ON games(created_at);
CREATE INDEX IF NOT EXISTS idx_games_updated_at ON games(updated_at);

-- Full-text search index
CREATE INDEX IF NOT EXISTS idx_games_search ON games USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '') || ' ' || COALESCE(short_description, '')));

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_games_updated_at BEFORE UPDATE ON games
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_genres_updated_at BEFORE UPDATE ON genres
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tags_updated_at BEFORE UPDATE ON tags
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_platforms_updated_at BEFORE UPDATE ON platforms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();