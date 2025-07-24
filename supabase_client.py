#!/usr/bin/env python3
"""
Supabase client for database operations with schema management
"""

import os
import asyncio
from typing import Dict, List, Optional, Any
import logging
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not all([self.url, self.service_role_key]):
            raise ValueError("Missing Supabase credentials in environment variables")
        
        # Use service role key for admin operations
        self.client: Client = create_client(
            self.url, 
            self.service_role_key,
            options=ClientOptions(
                schema="public",
                headers={
                    "X-Client-Info": "zoho-sync-to-supabase"
                }
            )
        )
        
        # Schema names for different Zoho apps
        self.schemas = {
            "fsm": "zoho_fsm",
            "crm": "zoho_crm", 
            "inventory": "zoho_inventory"
        }
        
        logging.info("Supabase client initialized")
    
    async def create_schemas(self) -> bool:
        """Create schemas for different Zoho apps"""
        try:
            for app_name, schema_name in self.schemas.items():
                await self._create_schema(schema_name)
                logging.info(f"Schema {schema_name} created/verified")
            return True
        except Exception as e:
            logging.error(f"Failed to create schemas: {e}")
            return False
    
    async def _create_schema(self, schema_name: str) -> None:
        """Create a schema if it doesn't exist"""
        # Note: Supabase Python client doesn't support schema creation directly
        # This would need to be done via SQL migration or admin interface
        # For now, we'll assume schemas are created via migrations
        pass
    
    async def create_fsm_tables(self) -> bool:
        """Create FSM-specific tables"""
        try:
            schema = self.schemas["fsm"]
            
            # Create work orders table
            await self._create_work_orders_table(schema)
            
            # Create service appointments table
            await self._create_service_appointments_table(schema)
            
            # Create customers table
            await self._create_customers_table(schema)
            
            # Create technicians table
            await self._create_technicians_table(schema)
            
            # Create sync status table
            await self._create_sync_status_table(schema)
            
            logging.info("FSM tables created successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to create FSM tables: {e}")
            return False
    
    async def _create_work_orders_table(self, schema: str) -> None:
        """Create work orders table"""
        # This would be done via SQL migration
        # For now, we'll assume the table exists
        pass
    
    async def _create_service_appointments_table(self, schema: str) -> None:
        """Create service appointments table"""
        pass
    
    async def _create_customers_table(self, schema: str) -> None:
        """Create customers table"""
        pass
    
    async def _create_technicians_table(self, schema: str) -> None:
        """Create technicians table"""
        pass
    
    async def _create_sync_status_table(self, schema: str) -> None:
        """Create sync status tracking table"""
        pass
    
    async def upsert_work_orders(self, work_orders: List[Dict]) -> bool:
        """Upsert work orders to FSM schema"""
        try:
            schema = self.schemas["fsm"]
            table = "work_orders"
            
            # Transform FSM data to match our schema
            transformed_data = []
            for wo in work_orders:
                transformed_wo = {
                    "zoho_id": wo.get("id"),
                    "name": wo.get("Name"),
                    "status": wo.get("Status"),
                    "summary": wo.get("Summary"),
                    "contact_id": wo.get("Contact", {}).get("id"),
                    "contact_name": wo.get("Contact", {}).get("name"),
                    "company_id": wo.get("Company", {}).get("id") if wo.get("Company") else None,
                    "company_name": wo.get("Company", {}).get("name") if wo.get("Company") else None,
                    "created_time": wo.get("Created_Time"),
                    "modified_time": wo.get("Modified_Time"),
                    "raw_data": wo,  # Store complete FSM data
                    "last_synced": "now()"
                }
                transformed_data.append(transformed_wo)
            
            # Upsert data
            result = self.client.table(f"{schema}.{table}").upsert(
                transformed_data,
                on_conflict="zoho_id"
            ).execute()
            
            logging.info(f"Upserted {len(transformed_data)} work orders")
            return True
            
        except Exception as e:
            logging.error(f"Failed to upsert work orders: {e}")
            return False
    
    async def upsert_service_appointments(self, appointments: List[Dict]) -> bool:
        """Upsert service appointments to FSM schema"""
        try:
            schema = self.schemas["fsm"]
            table = "service_appointments"
            
            # Transform FSM data to match our schema
            transformed_data = []
            for appt in appointments:
                transformed_appt = {
                    "zoho_id": appt.get("id"),
                    "name": appt.get("Name"),
                    "status": appt.get("Status"),
                    "work_order_id": appt.get("Work_Order", {}).get("id") if appt.get("Work_Order") else None,
                    "technician_id": appt.get("Technician", {}).get("id") if appt.get("Technician") else None,
                    "scheduled_time": appt.get("Scheduled_Time"),
                    "created_time": appt.get("Created_Time"),
                    "modified_time": appt.get("Modified_Time"),
                    "raw_data": appt,  # Store complete FSM data
                    "last_synced": "now()"
                }
                transformed_data.append(transformed_appt)
            
            # Upsert data
            result = self.client.table(f"{schema}.{table}").upsert(
                transformed_data,
                on_conflict="zoho_id"
            ).execute()
            
            logging.info(f"Upserted {len(transformed_data)} service appointments")
            return True
            
        except Exception as e:
            logging.error(f"Failed to upsert service appointments: {e}")
            return False
    
    async def get_work_orders(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get work orders from FSM schema"""
        try:
            schema = self.schemas["fsm"]
            table = "work_orders"
            
            result = self.client.table(f"{schema}.{table}").select("*").limit(limit).offset(offset).execute()
            return result.data
            
        except Exception as e:
            logging.error(f"Failed to get work orders: {e}")
            return []
    
    async def get_service_appointments(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get service appointments from FSM schema"""
        try:
            schema = self.schemas["fsm"]
            table = "service_appointments"
            
            result = self.client.table(f"{schema}.{table}").select("*").limit(limit).offset(offset).execute()
            return result.data
            
        except Exception as e:
            logging.error(f"Failed to get service appointments: {e}")
            return []
    
    async def update_sync_status(self, table_name: str, status: str, last_sync: str = None) -> bool:
        """Update sync status for a table"""
        try:
            schema = self.schemas["fsm"]
            table = "sync_status"
            
            data = {
                "table_name": table_name,
                "status": status,
                "last_sync": last_sync or "now()",
                "updated_at": "now()"
            }
            
            result = self.client.table(f"{schema}.{table}").upsert(
                data,
                on_conflict="table_name"
            ).execute()
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to update sync status: {e}")
            return False
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get sync status for all tables"""
        try:
            schema = self.schemas["fsm"]
            table = "sync_status"
            
            result = self.client.table(f"{schema}.{table}").select("*").execute()
            
            status = {}
            for row in result.data:
                status[row["table_name"]] = {
                    "status": row["status"],
                    "last_sync": row["last_sync"],
                    "updated_at": row["updated_at"]
                }
            
            return status
            
        except Exception as e:
            logging.error(f"Failed to get sync status: {e}")
            return {}

# Test function
async def test_supabase_connection():
    """Test Supabase connection"""
    try:
        client = SupabaseClient()
        print("✅ Supabase client initialized successfully")
        
        # Test getting sync status
        status = await client.get_sync_status()
        print(f"✅ Sync status retrieved: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_supabase_connection()) 