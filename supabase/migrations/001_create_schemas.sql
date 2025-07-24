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

-- Enable Row Level Security (RLS) on schemas
ALTER SCHEMA zoho_fsm SET row_security = on;
ALTER SCHEMA zoho_crm SET row_security = on;
ALTER SCHEMA zoho_inventory SET row_security = on; 