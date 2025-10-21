-- Monitoring Service Database Initialization
-- This script creates the initial database structure for the monitoring service

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create log_entries table
CREATE TABLE IF NOT EXISTS log_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create metrics table
CREATE TABLE IF NOT EXISTS metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    metric_type VARCHAR(20) NOT NULL, -- counter, gauge, histogram, summary
    labels JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    alert_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- critical, warning, info
    status VARCHAR(20) NOT NULL, -- active, resolved, acknowledged
    message TEXT NOT NULL,
    labels JSONB,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_log_entries_service_timestamp ON log_entries(service_name, timestamp);
CREATE INDEX IF NOT EXISTS idx_log_entries_level ON log_entries(level);
CREATE INDEX IF NOT EXISTS idx_log_entries_timestamp ON log_entries(timestamp);

CREATE INDEX IF NOT EXISTS idx_metrics_service_name ON metrics(service_name);
CREATE INDEX IF NOT EXISTS idx_metrics_metric_name ON metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp);

CREATE INDEX IF NOT EXISTS idx_alerts_service_name ON alerts(service_name);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_started_at ON alerts(started_at);

-- Create indexes for JSONB columns
CREATE INDEX IF NOT EXISTS idx_log_entries_metadata ON log_entries USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_metrics_labels ON metrics USING GIN(labels);
CREATE INDEX IF NOT EXISTS idx_alerts_labels ON alerts USING GIN(labels);

-- Insert some sample data
INSERT INTO log_entries (service_name, level, message, metadata) VALUES
('monitoring-service', 'INFO', 'Monitoring service started', '{"version": "1.0.0", "port": 8012}'),
('user-service', 'INFO', 'User service health check passed', '{"response_time": 15}'),
('game-catalog-service', 'INFO', 'Game catalog service health check passed', '{"response_time": 23}');

INSERT INTO metrics (service_name, metric_name, metric_value, metric_type, labels) VALUES
('monitoring-service', 'service_uptime', 3600, 'gauge', '{"status": "running"}'),
('user-service', 'request_count', 150, 'counter', '{"endpoint": "/health"}'),
('game-catalog-service', 'request_count', 89, 'counter', '{"endpoint": "/health"}');

-- Create a function to clean up old logs (older than 30 days)
CREATE OR REPLACE FUNCTION cleanup_old_logs()
RETURNS void AS $$
BEGIN
    DELETE FROM log_entries WHERE created_at < NOW() - INTERVAL '30 days';
    DELETE FROM metrics WHERE created_at < NOW() - INTERVAL '30 days';
    DELETE FROM alerts WHERE created_at < NOW() - INTERVAL '30 days' AND status = 'resolved';
END;
$$ LANGUAGE plpgsql;

-- Create a function to get service health status
CREATE OR REPLACE FUNCTION get_service_health(service_name_param VARCHAR)
RETURNS TABLE (
    service_name VARCHAR,
    last_health_check TIMESTAMP WITH TIME ZONE,
    is_healthy BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        service_name_param,
        MAX(timestamp) as last_health_check,
        CASE 
            WHEN MAX(timestamp) > NOW() - INTERVAL '5 minutes' THEN true
            ELSE false
        END as is_healthy
    FROM log_entries 
    WHERE service_name = service_name_param 
    AND level = 'INFO' 
    AND message LIKE '%health check%';
END;
$$ LANGUAGE plpgsql;