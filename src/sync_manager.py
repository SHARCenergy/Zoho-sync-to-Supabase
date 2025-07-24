import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
from .zoho_client import ZohoClient
from .supabase_client import SupabaseClient
from .config import settings

class SyncManager:
    def __init__(self):
        self.zoho_client = ZohoClient()
        self.supabase_client = SupabaseClient()
        self.sync_status = {}
        self.is_running = False
        
    async def initialize(self):
        """Initialize sync manager and create schemas"""
        logger.info("Initializing sync manager...")
        
        # Create schemas for different Zoho apps
        schemas = ["zoho_fsm", "zoho_crm", "zoho_inventory"]
        for schema in schemas:
            await self.supabase_client.create_schema(schema)
        
        logger.info("Sync manager initialized successfully")
    
    async def sync_fsm_data(self):
        """Sync Zoho FSM data to Supabase"""
        logger.info("Starting FSM data sync...")
        
        try:
            # Get last sync time
            sync_status = await self.supabase_client.get_sync_status("zoho_fsm", "work_orders")
            last_sync = sync_status.get("last_sync") if sync_status else None
            
            # Sync work orders
            work_orders = await self.zoho_client.get_work_orders(
                modified_since=datetime.fromisoformat(last_sync) if last_sync else None
            )
            
            for work_order in work_orders:
                # Add metadata for tracking
                work_order["source"] = "zoho"
                work_order["sync_status"] = "synced"
                work_order["updated_at"] = datetime.now().isoformat()
                
                await self.supabase_client.upsert_record(
                    "zoho_fsm", "work_orders", work_order, "id"
                )
            
            # Sync customers
            customers = await self.zoho_client.get_customers(
                modified_since=datetime.fromisoformat(last_sync) if last_sync else None
            )
            
            for customer in customers:
                customer["source"] = "zoho"
                customer["sync_status"] = "synced"
                customer["updated_at"] = datetime.now().isoformat()
                
                await self.supabase_client.upsert_record(
                    "zoho_fsm", "customers", customer, "id"
                )
            
            # Sync technicians
            technicians = await self.zoho_client.get_technicians(
                modified_since=datetime.fromisoformat(last_sync) if last_sync else None
            )
            
            for technician in technicians:
                technician["source"] = "zoho"
                technician["sync_status"] = "synced"
                technician["updated_at"] = datetime.now().isoformat()
                
                await self.supabase_client.upsert_record(
                    "zoho_fsm", "technicians", technician, "id"
                )
            
            # Sync appointments
            appointments = await self.zoho_client.get_appointments(
                modified_since=datetime.fromisoformat(last_sync) if last_sync else None
            )
            
            for appointment in appointments:
                appointment["source"] = "zoho"
                appointment["sync_status"] = "synced"
                appointment["updated_at"] = datetime.now().isoformat()
                
                await self.supabase_client.upsert_record(
                    "zoho_fsm", "appointments", appointment, "id"
                )
            
            # Update sync status
            await self.supabase_client.update_sync_status(
                "zoho_fsm", "work_orders", 
                datetime.now().isoformat(), "success"
            )
            
            logger.info(f"FSM sync completed: {len(work_orders)} work orders, "
                       f"{len(customers)} customers, {len(technicians)} technicians, "
                       f"{len(appointments)} appointments")
            
        except Exception as e:
            logger.error(f"Error during FSM sync: {e}")
            await self.supabase_client.update_sync_status(
                "zoho_fsm", "work_orders", 
                datetime.now().isoformat(), "error"
            )
            raise
    
    async def sync_from_supabase_to_zoho(self):
        """Sync changes from Supabase back to Zoho"""
        logger.info("Starting Supabase to Zoho sync...")
        
        try:
            # Get records that were modified in Supabase
            modified_work_orders = await self.supabase_client.get_records(
                "zoho_fsm", "work_orders",
                {"sync_status": "pending", "source": "supabase"}
            )
            
            for work_order in modified_work_orders:
                try:
                    if work_order.get("zoho_id"):
                        # Update in Zoho
                        await self.zoho_client.update_work_order(
                            work_order["zoho_id"], work_order
                        )
                    else:
                        # Create in Zoho
                        result = await self.zoho_client.create_work_order(work_order)
                        # Update Supabase record with Zoho ID
                        work_order["zoho_id"] = result["id"]
                    
                    # Mark as synced
                    work_order["sync_status"] = "synced"
                    work_order["source"] = "zoho"
                    await self.supabase_client.upsert_record(
                        "zoho_fsm", "work_orders", work_order, "id"
                    )
                    
                except Exception as e:
                    logger.error(f"Error syncing work order {work_order.get('id')}: {e}")
                    work_order["sync_status"] = "error"
                    work_order["error_message"] = str(e)
                    await self.supabase_client.upsert_record(
                        "zoho_fsm", "work_orders", work_order, "id"
                    )
            
            # Sync customers
            modified_customers = await self.supabase_client.get_records(
                "zoho_fsm", "customers",
                {"sync_status": "pending", "source": "supabase"}
            )
            
            for customer in modified_customers:
                try:
                    if customer.get("zoho_id"):
                        await self.zoho_client.update_customer(
                            customer["zoho_id"], customer
                        )
                    else:
                        result = await self.zoho_client.create_customer(customer)
                        customer["zoho_id"] = result["id"]
                    
                    customer["sync_status"] = "synced"
                    customer["source"] = "zoho"
                    await self.supabase_client.upsert_record(
                        "zoho_fsm", "customers", customer, "id"
                    )
                    
                except Exception as e:
                    logger.error(f"Error syncing customer {customer.get('id')}: {e}")
                    customer["sync_status"] = "error"
                    customer["error_message"] = str(e)
                    await self.supabase_client.upsert_record(
                        "zoho_fsm", "customers", customer, "id"
                    )
            
            # Sync technicians
            modified_technicians = await self.supabase_client.get_records(
                "zoho_fsm", "technicians",
                {"sync_status": "pending", "source": "supabase"}
            )
            
            for technician in modified_technicians:
                try:
                    if technician.get("zoho_id"):
                        await self.zoho_client.update_technician(
                            technician["zoho_id"], technician
                        )
                    else:
                        result = await self.zoho_client.create_technician(technician)
                        technician["zoho_id"] = result["id"]
                    
                    technician["sync_status"] = "synced"
                    technician["source"] = "zoho"
                    await self.supabase_client.upsert_record(
                        "zoho_fsm", "technicians", technician, "id"
                    )
                    
                except Exception as e:
                    logger.error(f"Error syncing technician {technician.get('id')}: {e}")
                    technician["sync_status"] = "error"
                    technician["error_message"] = str(e)
                    await self.supabase_client.upsert_record(
                        "zoho_fsm", "technicians", technician, "id"
                    )
            
            logger.info(f"Supabase to Zoho sync completed: {len(modified_work_orders)} work orders, "
                       f"{len(modified_customers)} customers, {len(modified_technicians)} technicians")
            
        except Exception as e:
            logger.error(f"Error during Supabase to Zoho sync: {e}")
            raise
    
    async def run_sync_cycle(self):
        """Run a complete sync cycle"""
        logger.info("Starting sync cycle...")
        
        try:
            # Sync from Zoho to Supabase
            await self.sync_fsm_data()
            
            # Sync from Supabase to Zoho
            await self.sync_from_supabase_to_zoho()
            
            logger.info("Sync cycle completed successfully")
            
        except Exception as e:
            logger.error(f"Error during sync cycle: {e}")
            raise
    
    async def start_continuous_sync(self):
        """Start continuous sync with specified interval"""
        self.is_running = True
        logger.info(f"Starting continuous sync with {settings.sync_interval}s interval")
        
        while self.is_running:
            try:
                await self.run_sync_cycle()
                await asyncio.sleep(settings.sync_interval)
            except Exception as e:
                logger.error(f"Error in continuous sync: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def stop_continuous_sync(self):
        """Stop continuous sync"""
        self.is_running = False
        logger.info("Continuous sync stopped")
    
    async def trigger_manual_sync(self):
        """Trigger a manual sync"""
        logger.info("Manual sync triggered")
        await self.run_sync_cycle() 