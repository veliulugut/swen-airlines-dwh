#!/bin/bash
set -e

# Create multiple databases script for PostgreSQL
# This script creates separate databases for Swen Airlines DWH and Airflow

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    -- Create Swen Airlines DWH database
    CREATE DATABASE swen_dwh;
    GRANT ALL PRIVILEGES ON DATABASE swen_dwh TO $POSTGRES_USER;
    
    -- Create Airflow database  
    CREATE DATABASE airflow_db;
    GRANT ALL PRIVILEGES ON DATABASE airflow_db TO $POSTGRES_USER;
    
    -- Log created databases
    \echo 'ℹ️ Created databases: swen_dwh, airflow_db'
EOSQL

echo "✅ Multiple databases created successfully!" 