-- Fix Permissions Script
-- This grants the necessary permissions to the authenticated role

-- Grant usage on schemas
GRANT USAGE ON SCHEMA zoho_fsm TO authenticated;
GRANT USAGE ON SCHEMA zoho_crm TO authenticated;
GRANT USAGE ON SCHEMA zoho_inventory TO authenticated;

-- Grant all permissions on all tables in zoho_fsm
GRANT ALL ON ALL TABLES IN SCHEMA zoho_fsm TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_fsm TO authenticated;

-- Grant all permissions on all tables in zoho_crm
GRANT ALL ON ALL TABLES IN SCHEMA zoho_crm TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_crm TO authenticated;

-- Grant all permissions on all tables in zoho_inventory
GRANT ALL ON ALL TABLES IN SCHEMA zoho_inventory TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_inventory TO authenticated;

-- Grant permissions to anon role as well (if needed)
GRANT USAGE ON SCHEMA zoho_fsm TO anon;
GRANT USAGE ON SCHEMA zoho_crm TO anon;
GRANT USAGE ON SCHEMA zoho_inventory TO anon;

GRANT ALL ON ALL TABLES IN SCHEMA zoho_fsm TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_fsm TO anon;

GRANT ALL ON ALL TABLES IN SCHEMA zoho_crm TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_crm TO anon;

GRANT ALL ON ALL TABLES IN SCHEMA zoho_inventory TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA zoho_inventory TO anon;

-- Verify permissions
SELECT 'PERMISSIONS FIXED' as status; 