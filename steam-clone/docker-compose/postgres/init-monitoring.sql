-- Monitoring Service Database Initialization
CREATE DATABASE monitoring_service;
\c monitoring_service;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE monitoring_service TO user;
GRANT ALL PRIVILEGES ON SCHEMA public TO user;

-- Create tables
CREATE TABLE IF NOT EXISTS service_health (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'healthy', 'unhealthy', 'degraded', 'unknown'
    response_time_ms INTEGER,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    network_in DECIMAL(10,2),
    network_out DECIMAL(10,2),
    active_connections INTEGER,
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER NOT NULL,
    request_size_bytes INTEGER,
    response_size_bytes INTEGER,
    user_id UUID,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS error_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    level VARCHAR(20) NOT NULL, -- 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    message TEXT NOT NULL,
    stack_trace TEXT,
    user_id UUID,
    request_id UUID,
    endpoint VARCHAR(500),
    method VARCHAR(10),
    status_code INTEGER,
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    metric_unit VARCHAR(20),
    tags JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    service_name VARCHAR(100),
    metric_name VARCHAR(100),
    threshold_value DECIMAL(15,4),
    comparison_operator VARCHAR(10), -- '>', '<', '>=', '<=', '==', '!='
    severity VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'resolved'
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id UUID REFERENCES alerts(id) ON DELETE CASCADE,
    service_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    threshold_value DECIMAL(15,4) NOT NULL,
    status VARCHAR(20) DEFAULT 'open', -- 'open', 'acknowledged', 'resolved', 'closed'
    severity VARCHAR(20) NOT NULL,
    message TEXT,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) NOT NULL,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    network_in DECIMAL(10,2),
    network_out DECIMAL(10,2),
    active_connections INTEGER,
    request_count INTEGER,
    error_count INTEGER,
    response_time_avg DECIMAL(10,2),
    response_time_p95 DECIMAL(10,2),
    response_time_p99 DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    service_name VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(100),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_service_health_service_name ON service_health(service_name);
CREATE INDEX IF NOT EXISTS idx_service_health_status ON service_health(status);
CREATE INDEX IF NOT EXISTS idx_service_health_created_at ON service_health(created_at);

CREATE INDEX IF NOT EXISTS idx_api_metrics_service_name ON api_metrics(service_name);
CREATE INDEX IF NOT EXISTS idx_api_metrics_endpoint ON api_metrics(endpoint);
CREATE INDEX IF NOT EXISTS idx_api_metrics_method ON api_metrics(method);
CREATE INDEX IF NOT EXISTS idx_api_metrics_status_code ON api_metrics(status_code);
CREATE INDEX IF NOT EXISTS idx_api_metrics_user_id ON api_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_api_metrics_created_at ON api_metrics(created_at);

CREATE INDEX IF NOT EXISTS idx_error_logs_service_name ON error_logs(service_name);
CREATE INDEX IF NOT EXISTS idx_error_logs_level ON error_logs(level);
CREATE INDEX IF NOT EXISTS idx_error_logs_user_id ON error_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_error_logs_request_id ON error_logs(request_id);
CREATE INDEX IF NOT EXISTS idx_error_logs_created_at ON error_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_performance_metrics_service_name ON performance_metrics(service_name);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_metric_name ON performance_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_created_at ON performance_metrics(created_at);

CREATE INDEX IF NOT EXISTS idx_alerts_name ON alerts(name);
CREATE INDEX IF NOT EXISTS idx_alerts_service_name ON alerts(service_name);
CREATE INDEX IF NOT EXISTS idx_alerts_metric_name ON alerts(metric_name);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_is_enabled ON alerts(is_enabled);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at);

CREATE INDEX IF NOT EXISTS idx_alert_incidents_alert_id ON alert_incidents(alert_id);
CREATE INDEX IF NOT EXISTS idx_alert_incidents_service_name ON alert_incidents(service_name);
CREATE INDEX IF NOT EXISTS idx_alert_incidents_status ON alert_incidents(status);
CREATE INDEX IF NOT EXISTS idx_alert_incidents_severity ON alert_incidents(severity);
CREATE INDEX IF NOT EXISTS idx_alert_incidents_created_at ON alert_incidents(created_at);

CREATE INDEX IF NOT EXISTS idx_system_metrics_service_name ON system_metrics(service_name);
CREATE INDEX IF NOT EXISTS idx_system_metrics_created_at ON system_metrics(created_at);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_service_name ON audit_logs(service_name);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_id ON audit_logs(resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_alerts_updated_at BEFORE UPDATE ON alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alert_incidents_updated_at BEFORE UPDATE ON alert_incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();