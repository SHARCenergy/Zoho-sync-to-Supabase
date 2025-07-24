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