-- Create Schemas and Tables
-- This creates the missing schemas and tables

-- Step 1: Create schemas
SELECT create_schema_if_not_exists('zoho_fsm');
SELECT create_schema_if_not_exists('zoho_crm');
SELECT create_schema_if_not_exists('zoho_inventory');

-- Step 2: Create tables in zoho_fsm schema
CREATE TABLE IF NOT EXISTS zoho_fsm.work_orders (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    status VARCHAR(100),
    priority VARCHAR(50),
    customer_id VARCHAR(255),
    technician_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_fsm.service_appointments (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    status VARCHAR(100),
    scheduled_date TIMESTAMP WITH TIME ZONE,
    customer_id VARCHAR(255),
    technician_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_fsm.customers (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_fsm.technicians (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    skills TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_fsm.sync_status (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) UNIQUE NOT NULL,
    last_sync TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'pending',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Step 3: Create tables in zoho_crm schema
CREATE TABLE IF NOT EXISTS zoho_crm.work_orders (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    status VARCHAR(100),
    priority VARCHAR(50),
    customer_id VARCHAR(255),
    technician_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_crm.customers (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_crm.technicians (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    skills TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_crm.service_appointments (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    status VARCHAR(100),
    scheduled_date TIMESTAMP WITH TIME ZONE,
    customer_id VARCHAR(255),
    technician_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

-- Step 4: Create tables in zoho_inventory schema
CREATE TABLE IF NOT EXISTS zoho_inventory.work_orders (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    status VARCHAR(100),
    priority VARCHAR(50),
    customer_id VARCHAR(255),
    technician_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_inventory.customers (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_inventory.technicians (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    skills TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS zoho_inventory.service_appointments (
    id SERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    status VARCHAR(100),
    scheduled_date TIMESTAMP WITH TIME ZONE,
    customer_id VARCHAR(255),
    technician_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'zoho',
    sync_status VARCHAR(50) DEFAULT 'synced',
    error_message TEXT
);

-- Step 5: Insert initial sync status records
INSERT INTO zoho_fsm.sync_status (table_name, last_sync, status) VALUES
('zoho_fsm.work_orders', NULL, 'pending'),
('zoho_fsm.service_appointments', NULL, 'pending'),
('zoho_fsm.customers', NULL, 'pending'),
('zoho_fsm.technicians', NULL, 'pending')
ON CONFLICT (table_name) DO NOTHING;

-- Step 6: Grant permissions on all new tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO anon;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO anon;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO anon;

-- Step 7: Grant permissions on sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO service_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO anon;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_crm TO service_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_crm TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_crm TO anon;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_inventory TO service_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_inventory TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_inventory TO anon;

-- Verify creation
SELECT 'SCHEMAS AND TABLES CREATED SUCCESSFULLY' as status; 