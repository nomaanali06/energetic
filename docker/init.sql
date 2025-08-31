-- Database initialization script for Energetic Backend
-- This script creates the initial database structure

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if it doesn't exist
-- (This will be handled by the container environment)

-- Set timezone
SET timezone = 'UTC';

-- Create custom types if needed
-- (PostgreSQL will create these automatically from the SQLAlchemy models)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE energetic_db TO postgres;

-- Create a simple test table to verify database connection
CREATE TABLE IF NOT EXISTS db_health_check (
    id SERIAL PRIMARY KEY,
    check_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'healthy'
);

-- Insert initial health check record
INSERT INTO db_health_check (status) VALUES ('initialized');

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Energetic Backend database initialized successfully at %', NOW();
END $$;
