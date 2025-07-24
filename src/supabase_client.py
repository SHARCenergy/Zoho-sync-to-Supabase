from supabase import create_client, Client
from typing import Dict, List, Optional, Any
from loguru import logger
from .config import settings
import json

class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
    
    async def create_schema(self, schema_name: str) -> None:
        """Create schema for a Zoho app"""
        try:
            # Create schema using raw SQL
            await self.client.rpc(
                "create_schema_if_not_exists",
                {"schema_name": schema_name}
            ).execute()
            logger.info(f"Schema {schema_name} created successfully")
        except Exception as e:
            logger.error(f"Error creating schema {schema_name}: {e}")
    
    async def upsert_record(self, schema: str, table: str, data: Dict, 
                           unique_field: str = "id") -> Dict:
        """Upsert record in specified schema.table"""
        try:
            # Use RPC to call a function that handles schema.table operations
            result = await self.client.rpc(
                "upsert_record",
                {
                    "p_schema": schema,
                    "p_table": table,
                    "p_data": json.dumps(data),
                    "p_unique_field": unique_field
                }
            ).execute()
            
            return result.data
        except Exception as e:
            logger.error(f"Error upserting record in {schema}.{table}: {e}")
            raise
    
    async def get_records(self, schema: str, table: str, 
                         filters: Optional[Dict] = None) -> List[Dict]:
        """Get records from specified schema.table"""
        try:
            # Use RPC to call a function that handles schema.table operations
            result = await self.client.rpc(
                "get_records",
                {
                    "p_schema": schema,
                    "p_table": table,
                    "p_filters": json.dumps(filters) if filters else None
                }
            ).execute()
            
            return result.data
        except Exception as e:
            logger.error(f"Error getting records from {schema}.{table}: {e}")
            raise
    
    async def delete_record(self, schema: str, table: str, record_id: str) -> bool:
        """Delete record from specified schema.table"""
        try:
            result = await self.client.rpc(
                "delete_record",
                {
                    "p_schema": schema,
                    "p_table": table,
                    "p_record_id": record_id
                }
            ).execute()
            
            return result.data
        except Exception as e:
            logger.error(f"Error deleting record from {schema}.{table}: {e}")
            raise
    
    async def get_sync_status(self, schema: str, table: str) -> Dict:
        """Get sync status for a table"""
        try:
            result = await self.client.rpc(
                "get_sync_status",
                {
                    "p_schema": schema,
                    "p_table": table
                }
            ).execute()
            
            return result.data
        except Exception as e:
            logger.error(f"Error getting sync status for {schema}.{table}: {e}")
            raise
    
    async def update_sync_status(self, schema: str, table: str, 
                                last_sync: str, status: str) -> None:
        """Update sync status for a table"""
        try:
            await self.client.rpc(
                "update_sync_status",
                {
                    "p_schema": schema,
                    "p_table": table,
                    "p_last_sync": last_sync,
                    "p_status": status
                }
            ).execute()
        except Exception as e:
            logger.error(f"Error updating sync status for {schema}.{table}: {e}")
            raise 