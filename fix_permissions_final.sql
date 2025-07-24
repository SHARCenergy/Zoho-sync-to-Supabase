-- FINAL PERMISSIONS FIX
-- This addresses the specific permission issues we're seeing

-- First, let's check what role we're running as
SELECT current_user, session_user;

-- Grant schema creation permissions to the service role
GRANT CREATE ON DATABASE postgres TO service_role;
GRANT CREATE ON SCHEMA public TO service_role;

-- Grant usage and create permissions on all schemas
GRANT USAGE, CREATE ON SCHEMA zoho_fsm TO service_role;
GRANT USAGE, CREATE ON SCHEMA zoho_crm TO service_role;
GRANT USAGE, CREATE ON SCHEMA zoho_inventory TO service_role;

-- Grant usage on schemas to both roles
GRANT USAGE ON SCHEMA zoho_fsm TO authenticated;
GRANT USAGE ON SCHEMA zoho_fsm TO anon;
GRANT USAGE ON SCHEMA zoho_crm TO authenticated;
GRANT USAGE ON SCHEMA zoho_crm TO anon;
GRANT USAGE ON SCHEMA zoho_inventory TO authenticated;
GRANT USAGE ON SCHEMA zoho_inventory TO anon;

-- Grant ALL permissions on ALL tables in zoho_fsm
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO anon;

-- Grant ALL permissions on ALL tables in zoho_crm
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO anon;

-- Grant ALL permissions on ALL tables in zoho_inventory
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO anon;

-- Grant permissions on sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO service_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO anon;

-- Grant execute permissions on functions
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon;

-- Grant specific function permissions
GRANT EXECUTE ON FUNCTION get_sync_status(TEXT, TEXT) TO service_role;
GRANT EXECUTE ON FUNCTION get_sync_status(TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_sync_status(TEXT, TEXT) TO anon;

GRANT EXECUTE ON FUNCTION update_sync_status(TEXT, TEXT, TEXT, TEXT) TO service_role;
GRANT EXECUTE ON FUNCTION update_sync_status(TEXT, TEXT, TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION update_sync_status(TEXT, TEXT, TEXT, TEXT) TO anon;

GRANT EXECUTE ON FUNCTION upsert_record(TEXT, TEXT, JSONB, TEXT) TO service_role;
GRANT EXECUTE ON FUNCTION upsert_record(TEXT, TEXT, JSONB, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION upsert_record(TEXT, TEXT, JSONB, TEXT) TO anon;

GRANT EXECUTE ON FUNCTION get_records(TEXT, TEXT, JSONB) TO service_role;
GRANT EXECUTE ON FUNCTION get_records(TEXT, TEXT, JSONB) TO authenticated;
GRANT EXECUTE ON FUNCTION get_records(TEXT, TEXT, JSONB) TO anon;

GRANT EXECUTE ON FUNCTION delete_record(TEXT, TEXT, TEXT) TO service_role;
GRANT EXECUTE ON FUNCTION delete_record(TEXT, TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION delete_record(TEXT, TEXT, TEXT) TO anon;

GRANT EXECUTE ON FUNCTION create_schema_if_not_exists(TEXT) TO service_role;
GRANT EXECUTE ON FUNCTION create_schema_if_not_exists(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION create_schema_if_not_exists(TEXT) TO anon;

-- Grant permissions on specific tables (explicit)
GRANT ALL ON zoho_fsm.work_orders TO service_role;
GRANT ALL ON zoho_fsm.work_orders TO authenticated;
GRANT ALL ON zoho_fsm.work_orders TO anon;

GRANT ALL ON zoho_fsm.service_appointments TO service_role;
GRANT ALL ON zoho_fsm.service_appointments TO authenticated;
GRANT ALL ON zoho_fsm.service_appointments TO anon;

GRANT ALL ON zoho_fsm.customers TO service_role;
GRANT ALL ON zoho_fsm.customers TO authenticated;
GRANT ALL ON zoho_fsm.customers TO anon;

GRANT ALL ON zoho_fsm.technicians TO service_role;
GRANT ALL ON zoho_fsm.technicians TO authenticated;
GRANT ALL ON zoho_fsm.technicians TO anon;

GRANT ALL ON zoho_fsm.sync_status TO service_role;
GRANT ALL ON zoho_fsm.sync_status TO authenticated;
GRANT ALL ON zoho_fsm.sync_status TO anon;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_fsm GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_fsm GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_fsm GRANT ALL ON TABLES TO anon;

ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_crm GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_crm GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_crm GRANT ALL ON TABLES TO anon;

ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_inventory GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_inventory GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA zoho_inventory GRANT ALL ON TABLES TO anon;

-- Verify permissions
SELECT 'FINAL PERMISSIONS FIX COMPLETED' as status; 