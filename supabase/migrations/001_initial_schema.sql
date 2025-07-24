-- Create schemas for different Zoho apps
CREATE SCHEMA IF NOT EXISTS zoho_fsm;
CREATE SCHEMA IF NOT EXISTS zoho_crm;
CREATE SCHEMA IF NOT EXISTS zoho_inventory;

-- Create sync status tracking table
CREATE TABLE IF NOT EXISTS sync_status (
    id SERIAL PRIMARY KEY,
    schema_name VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    last_sync TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'unknown',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(schema_name, table_name)
);

-- Create FSM tables
CREATE TABLE IF NOT EXISTS zoho_fsm.work_orders (
    id VARCHAR(100) PRIMARY KEY,
    zoho_id VARCHAR(100) UNIQUE,
    work_order_number VARCHAR(100),
    customer_id VARCHAR(100),
    technician_id VARCHAR(100),
    status VARCHAR(50),
    priority VARCHAR(20),
    description TEXT,
    scheduled_date TIMESTAMP WITH TIME ZONE,
    completed_date TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'synced',
    source VARCHAR(20) DEFAULT 'zoho',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zoho_fsm.customers (
    id VARCHAR(100) PRIMARY KEY,
    zoho_id VARCHAR(100) UNIQUE,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    sync_status VARCHAR(20) DEFAULT 'synced',
    source VARCHAR(20) DEFAULT 'zoho',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zoho_fsm.technicians (
    id VARCHAR(100) PRIMARY KEY,
    zoho_id VARCHAR(100) UNIQUE,
    technician_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    skills TEXT[],
    sync_status VARCHAR(20) DEFAULT 'synced',
    source VARCHAR(20) DEFAULT 'zoho',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zoho_fsm.appointments (
    id VARCHAR(100) PRIMARY KEY,
    zoho_id VARCHAR(100) UNIQUE,
    work_order_id VARCHAR(100),
    technician_id VARCHAR(100),
    scheduled_time TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER,
    status VARCHAR(50),
    sync_status VARCHAR(20) DEFAULT 'synced',
    source VARCHAR(20) DEFAULT 'zoho',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_work_orders_sync_status ON zoho_fsm.work_orders(sync_status);
CREATE INDEX IF NOT EXISTS idx_work_orders_source ON zoho_fsm.work_orders(source);
CREATE INDEX IF NOT EXISTS idx_customers_sync_status ON zoho_fsm.customers(sync_status);
CREATE INDEX IF NOT EXISTS idx_technicians_sync_status ON zoho_fsm.technicians(sync_status);
CREATE INDEX IF NOT EXISTS idx_appointments_sync_status ON zoho_fsm.appointments(sync_status); 