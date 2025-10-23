-- Recommendation Service Database Initialization
CREATE DATABASE recommendation_service;
\c recommendation_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE recommendation_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;

-- Create tables
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL,
    favorite_genres JSONB,
    favorite_tags JSONB,
    favorite_developers JSONB,
    favorite_publishers JSONB,
    price_range_min DECIMAL(10,2),
    price_range_max DECIMAL(10,2),
    preferred_platforms JSONB,
    language_preferences JSONB,
    age_rating_preferences JSONB,
    multiplayer_preference BOOLEAN,
    vr_preference BOOLEAN,
    early_access_preference BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_behavior (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    game_id INTEGER NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- 'view', 'purchase', 'play', 'wishlist', 'review', 'like', 'dislike'
    duration_seconds INTEGER,
    session_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game_features (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id INTEGER UNIQUE NOT NULL,
    features JSONB NOT NULL, -- ML features extracted from game data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    game_id INTEGER NOT NULL,
    algorithm VARCHAR(50) NOT NULL, -- 'collaborative', 'content_based', 'hybrid', 'popularity'
    score DECIMAL(5,4) NOT NULL, -- 0.0000 to 1.0000
    reason TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendation_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    version VARCHAR(20) NOT NULL,
    parameters JSONB,
    performance_metrics JSONB,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_training_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID REFERENCES recommendation_models(id) ON DELETE CASCADE,
    training_data_size INTEGER,
    training_duration_seconds INTEGER,
    accuracy DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall_score DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_similarity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID NOT NULL,
    user2_id UUID NOT NULL,
    similarity_score DECIMAL(5,4) NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user1_id, user2_id, algorithm)
);

CREATE TABLE IF NOT EXISTS game_similarity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game1_id INTEGER NOT NULL,
    game2_id INTEGER NOT NULL,
    similarity_score DECIMAL(5,4) NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game1_id, game2_id, algorithm)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_preferences_created_at ON user_preferences(created_at);

CREATE INDEX IF NOT EXISTS idx_user_behavior_user_id ON user_behavior(user_id);
CREATE INDEX IF NOT EXISTS idx_user_behavior_game_id ON user_behavior(game_id);
CREATE INDEX IF NOT EXISTS idx_user_behavior_action_type ON user_behavior(action_type);
CREATE INDEX IF NOT EXISTS idx_user_behavior_session_id ON user_behavior(session_id);
CREATE INDEX IF NOT EXISTS idx_user_behavior_created_at ON user_behavior(created_at);

CREATE INDEX IF NOT EXISTS idx_game_features_game_id ON game_features(game_id);
CREATE INDEX IF NOT EXISTS idx_game_features_created_at ON game_features(created_at);

CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_game_id ON recommendations(game_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_algorithm ON recommendations(algorithm);
CREATE INDEX IF NOT EXISTS idx_recommendations_score ON recommendations(score);
CREATE INDEX IF NOT EXISTS idx_recommendations_is_active ON recommendations(is_active);
CREATE INDEX IF NOT EXISTS idx_recommendations_created_at ON recommendations(created_at);
CREATE INDEX IF NOT EXISTS idx_recommendations_expires_at ON recommendations(expires_at);

CREATE INDEX IF NOT EXISTS idx_recommendation_models_name ON recommendation_models(name);
CREATE INDEX IF NOT EXISTS idx_recommendation_models_algorithm ON recommendation_models(algorithm);
CREATE INDEX IF NOT EXISTS idx_recommendation_models_is_active ON recommendation_models(is_active);
CREATE INDEX IF NOT EXISTS idx_recommendation_models_created_at ON recommendation_models(created_at);

CREATE INDEX IF NOT EXISTS idx_model_training_logs_model_id ON model_training_logs(model_id);
CREATE INDEX IF NOT EXISTS idx_model_training_logs_created_at ON model_training_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_user_similarity_user1_id ON user_similarity(user1_id);
CREATE INDEX IF NOT EXISTS idx_user_similarity_user2_id ON user_similarity(user2_id);
CREATE INDEX IF NOT EXISTS idx_user_similarity_algorithm ON user_similarity(algorithm);
CREATE INDEX IF NOT EXISTS idx_user_similarity_similarity_score ON user_similarity(similarity_score);

CREATE INDEX IF NOT EXISTS idx_game_similarity_game1_id ON game_similarity(game1_id);
CREATE INDEX IF NOT EXISTS idx_game_similarity_game2_id ON game_similarity(game2_id);
CREATE INDEX IF NOT EXISTS idx_game_similarity_algorithm ON game_similarity(algorithm);
CREATE INDEX IF NOT EXISTS idx_game_similarity_similarity_score ON game_similarity(similarity_score);

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_game_features_updated_at BEFORE UPDATE ON game_features
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recommendation_models_updated_at BEFORE UPDATE ON recommendation_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();