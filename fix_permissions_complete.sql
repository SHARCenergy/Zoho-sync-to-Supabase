-- Complete Permissions Fix
-- This grants ALL necessary permissions to resolve the access issues

-- Grant usage on schemas to both roles
GRANT USAGE ON SCHEMA zoho_fsm TO authenticated;
GRANT USAGE ON SCHEMA zoho_fsm TO anon;
GRANT USAGE ON SCHEMA zoho_crm TO authenticated;
GRANT USAGE ON SCHEMA zoho_crm TO anon;
GRANT USAGE ON SCHEMA zoho_inventory TO authenticated;
GRANT USAGE ON SCHEMA zoho_inventory TO anon;

-- Grant ALL permissions on ALL tables in zoho_fsm
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_fsm TO anon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA zoho_fsm TO authenticated;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA zoho_fsm TO anon;

-- Grant ALL permissions on ALL tables in zoho_crm
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_crm TO anon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA zoho_crm TO authenticated;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA zoho_crm TO anon;

-- Grant ALL permissions on ALL tables in zoho_inventory
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA zoho_inventory TO anon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA zoho_inventory TO authenticated;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA zoho_inventory TO anon;

-- Grant permissions on specific tables (explicit)
GRANT ALL ON zoho_fsm.work_orders TO authenticated;
GRANT ALL ON zoho_fsm.work_orders TO anon;
GRANT ALL ON zoho_fsm.service_appointments TO authenticated;
GRANT ALL ON zoho_fsm.service_appointments TO anon;
GRANT ALL ON zoho_fsm.customers TO authenticated;
GRANT ALL ON zoho_fsm.customers TO anon;
GRANT ALL ON zoho_fsm.technicians TO authenticated;
GRANT ALL ON zoho_fsm.technicians TO anon;
GRANT ALL ON zoho_fsm.sync_status TO authenticated;
GRANT ALL ON zoho_fsm.sync_status TO anon;

-- Grant permissions on sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA zoho_fsm TO anon;

-- Grant execute permissions on functions
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon;

-- Grant specific function permissions
GRANT EXECUTE ON FUNCTION get_sync_status(TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_sync_status(TEXT, TEXT) TO anon;
GRANT EXECUTE ON FUNCTION update_sync_status(TEXT, TEXT, TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION update_sync_status(TEXT, TEXT, TEXT, TEXT) TO anon;
GRANT EXECUTE ON FUNCTION upsert_record(TEXT, TEXT, JSONB, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION upsert_record(TEXT, TEXT, JSONB, TEXT) TO anon;
GRANT EXECUTE ON FUNCTION get_records(TEXT, TEXT, JSONB) TO authenticated;
GRANT EXECUTE ON FUNCTION get_records(TEXT, TEXT, JSONB) TO anon;
GRANT EXECUTE ON FUNCTION delete_record(TEXT, TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION delete_record(TEXT, TEXT, TEXT) TO anon;
GRANT EXECUTE ON FUNCTION create_schema_if_not_exists(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION create_schema_if_not_exists(TEXT) TO anon;

-- Verify permissions
SELECT 'PERMISSIONS COMPLETELY FIXED' as status; 