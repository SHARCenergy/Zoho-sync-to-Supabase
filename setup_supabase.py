#!/usr/bin/env python3
"""
Supabase Setup Script
This script helps set up the Supabase database with the required schemas, tables, and functions.
"""

import asyncio
import os
from pathlib import Path
from supabase import create_client, Client
from loguru import logger

class SupabaseSetup:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.supabase_url or not self.supabase_service_role_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env file")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_service_role_key)
    
    def read_sql_file(self, file_path: str) -> str:
        """Read SQL file content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def execute_sql(self, sql: str, description: str):
        """Execute SQL statement"""
        try:
            logger.info(f"Executing: {description}")
            result = self.supabase.rpc('exec_sql', {'sql': sql}).execute()
            logger.success(f"✅ {description} - Success")
            return result
        except Exception as e:
            logger.error(f"❌ {description} - Error: {e}")
            raise
    
    async def setup_database(self):
        """Set up the complete database"""
        logger.info("🚀 Starting Supabase database setup...")
        
        # Get migration files
        migrations_dir = Path("supabase/migrations")
        migration_files = sorted([
            "001_create_schemas.sql",
            "002_create_fsm_tables.sql", 
            "002_functions.sql"
        ])
        
        for migration_file in migration_files:
            file_path = migrations_dir / migration_file
            if file_path.exists():
                sql_content = self.read_sql_file(file_path)
                await self.execute_sql(sql_content, f"Migration: {migration_file}")
            else:
                logger.warning(f"⚠️ Migration file not found: {file_path}")
        
        logger.success("🎉 Database setup completed!")
    
    async def verify_setup(self):
        """Verify the setup by checking if tables and functions exist"""
        logger.info("🔍 Verifying database setup...")
        
        # Check if schemas exist
        schemas = ['zoho_fsm', 'zoho_crm', 'zoho_inventory']
        for schema in schemas:
            try:
                result = self.supabase.table(f"{schema}.work_orders").select("count", count="exact").execute()
                logger.success(f"✅ Schema {schema} exists and is accessible")
            except Exception as e:
                logger.error(f"❌ Schema {schema} not accessible: {e}")
        
        # Check if functions exist
        functions = ['get_sync_status', 'update_sync_status', 'upsert_record']
        for func in functions:
            try:
                # Try to call the function with dummy parameters
                if func == 'get_sync_status':
                    result = self.supabase.rpc(func, {'p_schema': 'zoho_fsm', 'p_table': 'work_orders'}).execute()
                elif func == 'update_sync_status':
                    result = self.supabase.rpc(func, {
                        'p_last_sync': '2024-01-01T00:00:00Z',
                        'p_schema': 'zoho_fsm', 
                        'p_status': 'test',
                        'p_table': 'work_orders'
                    }).execute()
                else:
                    continue
                logger.success(f"✅ Function {func} exists and is callable")
            except Exception as e:
                logger.error(f"❌ Function {func} not accessible: {e}")

async def main():
    """Main setup function"""
    try:
        setup = SupabaseSetup()
        await setup.setup_database()
        await setup.verify_setup()
        
        logger.success("🎉 Supabase setup completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Test the API endpoints")
        logger.info("2. Configure Zoho credentials")
        logger.info("3. Start the sync process")
        
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 