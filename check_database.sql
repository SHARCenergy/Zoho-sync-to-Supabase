-- Database Diagnostic Script
-- Run this to see what's actually in your database

-- Check if schemas exist
SELECT 'SCHEMAS:' as check_type;
SELECT schema_name FROM information_schema.schemata 
WHERE schema_name IN ('zoho_fsm', 'zoho_crm', 'zoho_inventory');

-- Check if tables exist in zoho_fsm
SELECT 'ZOHO_FSM TABLES:' as check_type;
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'zoho_fsm';

-- Check if functions exist
SELECT 'FUNCTIONS:' as check_type;
SELECT routine_name FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND routine_name IN ('get_sync_status', 'update_sync_status', 'upsert_record', 'get_records', 'delete_record', 'create_schema_if_not_exists');

-- Check sync_status table specifically
SELECT 'SYNC_STATUS TABLE:' as check_type;
SELECT EXISTS (
    SELECT 1 FROM information_schema.tables 
    WHERE table_schema = 'zoho_fsm' 
    AND table_name = 'sync_status'
) as sync_status_exists;

-- Check permissions
SELECT 'PERMISSIONS:' as check_type;
SELECT schemaname, tablename, tableowner 
FROM pg_tables 
WHERE schemaname IN ('zoho_fsm', 'zoho_crm', 'zoho_inventory'); 