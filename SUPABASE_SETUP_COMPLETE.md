# Complete Supabase Setup Guide

## 🎯 Current Status
- ✅ **Supabase Connection**: Working
- ✅ **Environment Variables**: Configured
- 🔄 **Database Schema**: Ready to apply (clean slate)
- 🔄 **Functions**: Ready to apply

## 📋 Step-by-Step Setup

### Step 0: Clean Database (IMPORTANT - Start Fresh)
**If you've run any previous migrations or are getting errors, run this cleanup first:**

Copy and paste this SQL into the SQL Editor:

```sql
-- Cleanup Database Script
-- This script removes all existing Zoho-related schemas, tables, functions, and policies
-- Run this BEFORE applying the new migrations

-- Drop all triggers first
DROP TRIGGER IF EXISTS update_work_orders_updated_at ON zoho_fsm.work_orders;
DROP TRIGGER IF EXISTS update_service_appointments_updated_at ON zoho_fsm.service_appointments;
DROP TRIGGER IF EXISTS update_customers_updated_at ON zoho_fsm.customers;
DROP TRIGGER IF EXISTS update_technicians_updated_at ON zoho_fsm.technicians;
DROP TRIGGER IF EXISTS update_sync_status_updated_at ON zoho_fsm.sync_status;

-- Drop all policies
DROP POLICY IF EXISTS "Allow all operations on work_orders" ON zoho_fsm.work_orders;
DROP POLICY IF EXISTS "Allow all operations on service_appointments" ON zoho_fsm.service_appointments;
DROP POLICY IF EXISTS "Allow all operations on customers" ON zoho_fsm.customers;
DROP POLICY IF EXISTS "Allow all operations on technicians" ON zoho_fsm.technicians;
DROP POLICY IF EXISTS "Allow all operations on sync_status" ON zoho_fsm.sync_status;

-- Drop all tables in zoho_fsm schema
DROP TABLE IF EXISTS zoho_fsm.work_orders CASCADE;
DROP TABLE IF EXISTS zoho_fsm.service_appointments CASCADE;
DROP TABLE IF EXISTS zoho_fsm.customers CASCADE;
DROP TABLE IF EXISTS zoho_fsm.technicians CASCADE;
DROP TABLE IF EXISTS zoho_fsm.sync_status CASCADE;

-- Drop all tables in zoho_crm schema
DROP TABLE IF EXISTS zoho_crm.work_orders CASCADE;
DROP TABLE IF EXISTS zoho_crm.customers CASCADE;
DROP TABLE IF EXISTS zoho_crm.technicians CASCADE;
DROP TABLE IF EXISTS zoho_crm.appointments CASCADE;

-- Drop all tables in zoho_inventory schema
DROP TABLE IF EXISTS zoho_inventory.work_orders CASCADE;
DROP TABLE IF EXISTS zoho_inventory.customers CASCADE;
DROP TABLE IF EXISTS zoho_inventory.technicians CASCADE;
DROP TABLE IF EXISTS zoho_inventory.appointments CASCADE;

-- Drop functions
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
DROP FUNCTION IF EXISTS create_schema_if_not_exists(TEXT) CASCADE;
DROP FUNCTION IF EXISTS upsert_record(TEXT, TEXT, JSONB, TEXT) CASCADE;
DROP FUNCTION IF EXISTS get_records(TEXT, TEXT, JSONB) CASCADE;
DROP FUNCTION IF EXISTS delete_record(TEXT, TEXT, TEXT) CASCADE;
DROP FUNCTION IF EXISTS get_sync_status(TEXT, TEXT) CASCADE;
DROP FUNCTION IF EXISTS update_sync_status(TEXT, TEXT, TEXT, TEXT) CASCADE;

-- Drop schemas (this will drop everything in them)
DROP SCHEMA IF EXISTS zoho_fsm CASCADE;
DROP SCHEMA IF EXISTS zoho_crm CASCADE;
DROP SCHEMA IF EXISTS zoho_inventory CASCADE;

-- Verify cleanup
SELECT 'Cleanup completed successfully' as status;
```

**Click "Run" to execute the cleanup.**

### Step 1: Access Your Supabase Dashboard
1. Go to: https://supabase.com/dashboard
2. Select your project: `dmgeqehmgolsiurahmud`
3. Navigate to **SQL Editor** in the left sidebar

### Step 2: Apply Migration 1 - Create Schemas

Copy and paste this SQL into the SQL Editor:

```sql
-- Create schemas for different Zoho apps
-- Migration: 001_create_schemas.sql

-- Create schema for Zoho FSM (Field Service Management)
CREATE SCHEMA IF NOT EXISTS zoho_fsm;

-- Create schema for Zoho CRM (Customer Relationship Management)
CREATE SCHEMA IF NOT EXISTS zoho_crm;

-- Create schema for Zoho Inventory
CREATE SCHEMA IF NOT EXISTS zoho_inventory;

-- Grant permissions to authenticated users
GRANT USAGE ON SCHEMA zoho_fsm TO authenticated;
GRANT USAGE ON SCHEMA zoho_crm TO authenticated;
GRANT USAGE ON SCHEMA zoho_inventory TO authenticated;

-- Grant permissions to anon users (if needed for public access)
GRANT USAGE ON SCHEMA zoho_fsm TO anon;
GRANT USAGE ON SCHEMA zoho_crm TO anon;
GRANT USAGE ON SCHEMA zoho_inventory TO anon;

-- Note: Row Level Security (RLS) is enabled at the table level, not schema level
-- RLS will be enabled on individual tables when they are created
```

**Click "Run" to execute this migration.**

### Step 3: Apply Migration 2 - Create FSM Tables

Copy and paste this SQL into the SQL Editor:

```sql
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
    ('zoho_fsm.work_orders', 'idle'),
    ('zoho_fsm.service_appointments', 'idle'),
    ('zoho_fsm.customers', 'idle'),
    ('zoho_fsm.technicians', 'idle')
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
```

**Click "Run" to execute this migration.**

### Step 4: Apply Migration 3 - Create Functions

Copy and paste this SQL into the SQL Editor:

```sql
-- Function to create schema if not exists
CREATE OR REPLACE FUNCTION create_schema_if_not_exists(schema_name TEXT)
RETURNS VOID AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE information_schema.schemata.schema_name = $1) THEN
        EXECUTE 'CREATE SCHEMA ' || quote_ident($1);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to upsert record in any schema.table
CREATE OR REPLACE FUNCTION upsert_record(
    p_schema TEXT,
    p_table TEXT,
    p_data JSONB,
    p_unique_field TEXT DEFAULT 'id'
)
RETURNS JSONB AS $$
DECLARE
    sql_query TEXT;
    result JSONB;
    columns_list TEXT;
    values_list TEXT;
    update_list TEXT;
BEGIN
    -- Build dynamic SQL for upsert
    SELECT 
        string_agg(quote_ident(key), ','),
        string_agg('$1->>' || quote_literal(key), ','),
        string_agg(quote_ident(key) || ' = EXCLUDED.' || quote_ident(key), ',')
    INTO columns_list, values_list, update_list
    FROM jsonb_object_keys(p_data);
    
    sql_query := format(
        'INSERT INTO %I.%I (%s) VALUES (%s) 
         ON CONFLICT (%I) DO UPDATE SET %s, updated_at = NOW()
         RETURNING to_jsonb(%I.*)',
        p_schema, p_table, columns_list, values_list, p_unique_field, update_list, p_table
    );
    
    EXECUTE sql_query INTO result USING p_data;
    RETURN result;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in upsert_record: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to get records from any schema.table
CREATE OR REPLACE FUNCTION get_records(
    p_schema TEXT,
    p_table TEXT,
    p_filters JSONB DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    sql_query TEXT;
    where_clause TEXT := '';
    result JSONB;
BEGIN
    -- Build WHERE clause from filters
    IF p_filters IS NOT NULL THEN
        SELECT string_agg(quote_ident(key) || ' = ' || quote_literal(value::text), ' AND ')
        INTO where_clause
        FROM jsonb_each(p_filters);
        
        where_clause := ' WHERE ' || where_clause;
    END IF;
    
    -- Build dynamic SQL
    sql_query := format(
        'SELECT to_jsonb(array_agg(%I.*)) FROM %I.%I%s',
        p_table, p_schema, p_table, where_clause
    );
    
    EXECUTE sql_query INTO result;
    RETURN COALESCE(result, '[]'::jsonb);
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in get_records: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to delete record from any schema.table
CREATE OR REPLACE FUNCTION delete_record(
    p_schema TEXT,
    p_table TEXT,
    p_record_id TEXT
)
RETURNS BOOLEAN AS $$
DECLARE
    sql_query TEXT;
    affected_rows INTEGER;
BEGIN
    sql_query := format(
        'DELETE FROM %I.%I WHERE id = %L',
        p_schema, p_table, p_record_id
    );
    
    EXECUTE sql_query;
    GET DIAGNOSTICS affected_rows = ROW_COUNT;
    RETURN affected_rows > 0;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in delete_record: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to get sync status (updated to match actual table structure)
CREATE OR REPLACE FUNCTION get_sync_status(
    p_schema TEXT,
    p_table TEXT
)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
    full_table_name TEXT;
BEGIN
    -- Create full table name for lookup
    full_table_name := p_schema || '.' || p_table;
    
    SELECT to_jsonb(s.*) INTO result
    FROM sync_status s
    WHERE s.table_name = full_table_name;
    
    RETURN result;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in get_sync_status: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to update sync status (updated to match actual table structure)
CREATE OR REPLACE FUNCTION update_sync_status(
    p_last_sync TEXT,
    p_schema TEXT,
    p_status TEXT,
    p_table TEXT
)
RETURNS VOID AS $$
DECLARE
    full_table_name TEXT;
BEGIN
    -- Create full table name for storage
    full_table_name := p_schema || '.' || p_table;
    
    INSERT INTO sync_status (table_name, last_sync, status, updated_at)
    VALUES (full_table_name, p_last_sync::timestamp with time zone, p_status, NOW())
    ON CONFLICT (table_name)
    DO UPDATE SET 
        last_sync = EXCLUDED.last_sync,
        status = EXCLUDED.status,
        updated_at = NOW();
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in update_sync_status: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;
```

**Click "Run" to execute this migration.**

## ✅ Verification Steps

After running all three migrations, verify the setup:

### 1. Check Schemas
Run this query to verify schemas were created:
```sql
SELECT schema_name FROM information_schema.schemata 
WHERE schema_name IN ('zoho_fsm', 'zoho_crm', 'zoho_inventory');
```

### 2. Check Tables
Run this query to verify tables were created:
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'zoho_fsm';
```

### 3. Check Functions
Run this query to verify functions were created:
```sql
SELECT routine_name FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND routine_name IN ('get_sync_status', 'update_sync_status', 'upsert_record');
```

## 🚀 Next Steps

After successful database setup:

1. **Test the API**: Run `python test_api.py`
2. **Start the sync service**: Run `python main.py`
3. **Monitor logs**: Check the sync status and error logs

## 🔧 Troubleshooting

### Common Issues:

1. **Permission Errors**: Make sure you're using the service role key
2. **Function Not Found**: Ensure all three migrations ran successfully
3. **Schema Not Found**: Verify the schemas were created in the correct order

### If You Get Errors:

1. Check the SQL Editor for any error messages
2. Make sure you're running the migrations in the correct order
3. Verify that your Supabase project has the necessary permissions

## 📞 Support

If you encounter any issues:
1. Check the error logs in the SQL Editor
2. Verify your Supabase project settings
3. Ensure all environment variables are correctly set 