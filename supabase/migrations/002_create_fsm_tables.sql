-- Create FSM-specific tables
-- Migration: 002_create_fsm_tables.sql

-- Set search path to FSM schema
SET search_path TO zoho_fsm;

-- Create work orders table
CREATE TABLE IF NOT EXISTS work_orders (
    id BIGSERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    status VARCHAR(100),
    summary TEXT,
    contact_id VARCHAR(255),
    contact_name VARCHAR(255),
    company_id VARCHAR(255),
    company_name VARCHAR(255),
    created_time TIMESTAMPTZ,
    modified_time TIMESTAMPTZ,
    raw_data JSONB, -- Store complete FSM data
    last_synced TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create service appointments table
CREATE TABLE IF NOT EXISTS service_appointments (
    id BIGSERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    status VARCHAR(100),
    work_order_id VARCHAR(255),
    technician_id VARCHAR(255),
    scheduled_time TIMESTAMPTZ,
    created_time TIMESTAMPTZ,
    modified_time TIMESTAMPTZ,
    raw_data JSONB, -- Store complete FSM data
    last_synced TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id BIGSERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    company_name VARCHAR(255),
    created_time TIMESTAMPTZ,
    modified_time TIMESTAMPTZ,
    raw_data JSONB, -- Store complete FSM data
    last_synced TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create technicians table
CREATE TABLE IF NOT EXISTS technicians (
    id BIGSERIAL PRIMARY KEY,
    zoho_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    status VARCHAR(100),
    created_time TIMESTAMPTZ,
    modified_time TIMESTAMPTZ,
    raw_data JSONB, -- Store complete FSM data
    last_synced TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create sync status tracking table
CREATE TABLE IF NOT EXISTS sync_status (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'idle', -- idle, syncing, success, error
    last_sync TIMESTAMPTZ,
    error_message TEXT,
    records_processed INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_work_orders_zoho_id ON work_orders(zoho_id);
CREATE INDEX IF NOT EXISTS idx_work_orders_status ON work_orders(status);
CREATE INDEX IF NOT EXISTS idx_work_orders_modified_time ON work_orders(modified_time);

CREATE INDEX IF NOT EXISTS idx_service_appointments_zoho_id ON service_appointments(zoho_id);
CREATE INDEX IF NOT EXISTS idx_service_appointments_status ON service_appointments(status);
CREATE INDEX IF NOT EXISTS idx_service_appointments_work_order_id ON service_appointments(work_order_id);

CREATE INDEX IF NOT EXISTS idx_customers_zoho_id ON customers(zoho_id);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);

CREATE INDEX IF NOT EXISTS idx_technicians_zoho_id ON technicians(zoho_id);
CREATE INDEX IF NOT EXISTS idx_technicians_email ON technicians(email);

-- Create GIN indexes for JSONB columns
CREATE INDEX IF NOT EXISTS idx_work_orders_raw_data ON work_orders USING GIN (raw_data);
CREATE INDEX IF NOT EXISTS idx_service_appointments_raw_data ON service_appointments USING GIN (raw_data);
CREATE INDEX IF NOT EXISTS idx_customers_raw_data ON customers USING GIN (raw_data);
CREATE INDEX IF NOT EXISTS idx_technicians_raw_data ON technicians USING GIN (raw_data);

-- Enable Row Level Security (RLS)
ALTER TABLE work_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE service_appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE technicians ENABLE ROW LEVEL SECURITY;
ALTER TABLE sync_status ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (allow all operations for now - customize as needed)
CREATE POLICY "Allow all operations on work_orders" ON work_orders FOR ALL USING (true);
CREATE POLICY "Allow all operations on service_appointments" ON service_appointments FOR ALL USING (true);
CREATE POLICY "Allow all operations on customers" ON customers FOR ALL USING (true);
CREATE POLICY "Allow all operations on technicians" ON technicians FOR ALL USING (true);
CREATE POLICY "Allow all operations on sync_status" ON sync_status FOR ALL USING (true);

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA zoho_fsm TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_fsm TO authenticated;

-- Insert initial sync status records
INSERT INTO sync_status (table_name, status) VALUES 
    ('work_orders', 'idle'),
    ('service_appointments', 'idle'),
    ('customers', 'idle'),
    ('technicians', 'idle')
ON CONFLICT (table_name) DO NOTHING;

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_work_orders_updated_at BEFORE UPDATE ON work_orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_service_appointments_updated_at BEFORE UPDATE ON service_appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_technicians_updated_at BEFORE UPDATE ON technicians FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sync_status_updated_at BEFORE UPDATE ON sync_status FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); 