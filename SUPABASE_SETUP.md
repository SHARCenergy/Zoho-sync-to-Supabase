# Supabase Database Setup Guide

This guide will help you set up your Supabase database with the required schemas, tables, and functions for the Zoho sync system.

## Prerequisites

1. **Supabase Project**: You need a Supabase project created
2. **Service Role Key**: Get your service role key from Supabase dashboard
3. **Environment Variables**: Configure your `.env` file

## Step 1: Configure Environment Variables

Make sure your `.env` file contains the following Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

## Step 2: Apply Database Migrations

You have several options to apply the migrations:

### Option A: Using Supabase Dashboard (Recommended)

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Run the following SQL files in order:

#### 1. Create Schemas
```sql
-- Copy content from: supabase/migrations/001_create_schemas.sql
```

#### 2. Create FSM Tables
```sql
-- Copy content from: supabase/migrations/002_create_fsm_tables.sql
```

#### 3. Create Functions
```sql
-- Copy content from: supabase/migrations/002_functions.sql
```

### Option B: Using Supabase CLI

If you have Supabase CLI installed:

```bash
# Install Supabase CLI (if not already installed)
npm install -g supabase

# Login to Supabase
supabase login

# Link your project
supabase link --project-ref your-project-id

# Apply migrations
supabase db push
```

### Option C: Using Python Script

Run the setup script:

```bash
python setup_supabase.py
```

## Step 3: Verify Setup

After applying the migrations, verify that:

1. **Schemas exist**: `zoho_fsm`, `zoho_crm`, `zoho_inventory`
2. **Tables exist**: `work_orders`, `service_appointments`, `customers`, `technicians`, `sync_status`
3. **Functions exist**: `get_sync_status`, `update_sync_status`, `upsert_record`

## Step 4: Test the Setup

Run the test script to verify everything is working:

```bash
python test_api.py
```

## Troubleshooting

### Common Issues

1. **Function not found errors**: Make sure you've run the functions migration
2. **Permission errors**: Ensure you're using the service role key, not the anon key
3. **Schema not found**: Verify the schemas were created successfully

### Error: "Could not find the function public.get_sync_status"

This error occurs when the database functions haven't been created. Solution:

1. Run the functions migration: `supabase/migrations/002_functions.sql`
2. Make sure you're using the service role key for database operations
3. Check that the `sync_status` table exists and has the correct structure

### Error: "Schema cache" issues

This usually means the functions exist but aren't accessible. Solution:

1. Check your Supabase permissions
2. Ensure you're using the correct API key (service role for admin operations)
3. Try refreshing the schema cache in Supabase dashboard

## Next Steps

After successful setup:

1. **Test API endpoints**: Verify all endpoints are working
2. **Configure Zoho**: Set up your Zoho credentials
3. **Start sync**: Begin the bidirectional sync process
4. **Monitor logs**: Check sync status and error logs

## Database Schema Overview

### Schemas
- `zoho_fsm`: Field Service Management data
- `zoho_crm`: Customer Relationship Management data  
- `zoho_inventory`: Inventory Management data

### Key Tables (in zoho_fsm schema)
- `work_orders`: Work orders and jobs
- `service_appointments`: Scheduled appointments
- `customers`: Customer information
- `technicians`: Field technicians
- `sync_status`: Sync status tracking

### Key Functions
- `get_sync_status(p_schema, p_table)`: Get sync status for a table
- `update_sync_status(p_last_sync, p_schema, p_status, p_table)`: Update sync status
- `upsert_record(p_schema, p_table, p_data, p_unique_field)`: Upsert data to any table

## Security Notes

- The service role key has full database access
- Row Level Security (RLS) is enabled on all tables
- Default policies allow all operations (customize as needed)
- Consider implementing more restrictive policies for production 