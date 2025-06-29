-- =================================================================
-- Airflow Database Creation Script  
-- =================================================================

-- Create airflow database for Airflow system tables
CREATE DATABASE airflow;

-- Grant privileges to admin user
GRANT ALL PRIVILEGES ON DATABASE airflow TO admin; 