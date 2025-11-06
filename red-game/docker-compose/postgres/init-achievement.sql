-- Achievement Service Database Initialization
CREATE DATABASE achievement_service;
\c achievement_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE achievement_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;

-- Create tables
CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    icon_url TEXT,
    points INTEGER DEFAULT 0,
    is_hidden BOOLEAN DEFAULT FALSE,
    is_rare BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    progress INTEGER DEFAULT 0,
    is_unlocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS achievement_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS achievement_category_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
    category_id UUID REFERENCES achievement_categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(achievement_id, category_id)
);

CREATE TABLE IF NOT EXISTS achievement_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    achievement_id UUID REFERENCES achievements(id) ON DELETE CASCADE,
    current_progress INTEGER DEFAULT 0,
    max_progress INTEGER DEFAULT 1,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, achievement_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_achievements_game_id ON achievements(game_id);
CREATE INDEX IF NOT EXISTS idx_achievements_name ON achievements(name);
CREATE INDEX IF NOT EXISTS idx_achievements_points ON achievements(points);
CREATE INDEX IF NOT EXISTS idx_achievements_is_hidden ON achievements(is_hidden);
CREATE INDEX IF NOT EXISTS idx_achievements_is_rare ON achievements(is_rare);
CREATE INDEX IF NOT EXISTS idx_achievements_created_at ON achievements(created_at);

CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_achievement_id ON user_achievements(achievement_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_unlocked_at ON user_achievements(unlocked_at);
CREATE INDEX IF NOT EXISTS idx_user_achievements_is_unlocked ON user_achievements(is_unlocked);

CREATE INDEX IF NOT EXISTS idx_achievement_categories_name ON achievement_categories(name);
CREATE INDEX IF NOT EXISTS idx_achievement_categories_created_at ON achievement_categories(created_at);

CREATE INDEX IF NOT EXISTS idx_achievement_category_assignments_achievement_id ON achievement_category_assignments(achievement_id);
CREATE INDEX IF NOT EXISTS idx_achievement_category_assignments_category_id ON achievement_category_assignments(category_id);

CREATE INDEX IF NOT EXISTS idx_achievement_progress_user_id ON achievement_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_achievement_progress_achievement_id ON achievement_progress(achievement_id);
CREATE INDEX IF NOT EXISTS idx_achievement_progress_last_updated ON achievement_progress(last_updated);

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_achievements_updated_at BEFORE UPDATE ON achievements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_achievement_categories_updated_at BEFORE UPDATE ON achievement_categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();