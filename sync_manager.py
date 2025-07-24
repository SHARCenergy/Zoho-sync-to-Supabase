#!/usr/bin/env python3
"""
Sync manager for bidirectional synchronization between Zoho FSM and Supabase
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from zoho_fsm_client import ZohoFSMClient
from supabase_client import SupabaseClient

class SyncStatus(Enum):
    IDLE = "idle"
    SYNCING = "syncing"
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class SyncResult:
    table_name: str
    status: SyncStatus
    records_processed: int
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class SyncManager:
    def __init__(self):
        """Initialize sync manager"""
        self.zoho_client = ZohoFSMClient("test_org")  # org_id will be updated
        self.supabase_client = SupabaseClient()
        self.is_running = False
        self.sync_interval = int(os.getenv("SYNC_INTERVAL", 300))  # 5 minutes default
        self.batch_size = int(os.getenv("BATCH_SIZE", 100))
        self.max_retries = int(os.getenv("MAX_RETRIES", 3))
        
        logging.info("Sync manager initialized")
    
    async def start_continuous_sync(self) -> bool:
        """Start continuous sync process"""
        if self.is_running:
            logging.warning("Sync is already running")
            return False
        
        self.is_running = True
        logging.info(f"Starting continuous sync with {self.sync_interval}s interval")
        
        try:
            while self.is_running:
                await self.sync_all()
                await asyncio.sleep(self.sync_interval)
        except Exception as e:
            logging.error(f"Continuous sync failed: {e}")
            self.is_running = False
            return False
        
        return True
    
    async def stop_continuous_sync(self) -> bool:
        """Stop continuous sync process"""
        self.is_running = False
        logging.info("Continuous sync stopped")
        return True
    
    async def sync_all(self) -> Dict[str, SyncResult]:
        """Sync all FSM data"""
        results = {}
        
        try:
            # Sync work orders
            results["work_orders"] = await self.sync_work_orders()
            
            # Sync service appointments
            results["service_appointments"] = await self.sync_service_appointments()
            
            # Log overall sync status
            success_count = sum(1 for r in results.values() if r.status == SyncStatus.SUCCESS)
            total_count = len(results)
            
            logging.info(f"Sync completed: {success_count}/{total_count} successful")
            
        except Exception as e:
            logging.error(f"Sync all failed: {e}")
            results["error"] = SyncResult(
                table_name="all",
                status=SyncStatus.ERROR,
                records_processed=0,
                error_message=str(e)
            )
        
        return results
    
    async def sync_work_orders(self) -> SyncResult:
        """Sync work orders from Zoho to Supabase"""
        start_time = datetime.now(timezone.utc)
        
        try:
            # Update sync status
            await self.supabase_client.update_sync_status("work_orders", "syncing")
            
            # Get work orders from Zoho
            work_orders = self.zoho_client.get_workorders(limit=self.batch_size)
            
            if not work_orders:
                logging.info("No work orders to sync")
                result = SyncResult(
                    table_name="work_orders",
                    status=SyncStatus.SUCCESS,
                    records_processed=0,
                    start_time=start_time,
                    end_time=datetime.now(timezone.utc)
                )
                await self.supabase_client.update_sync_status("work_orders", "success")
                return result
            
            # Upsert to Supabase
            success = await self.supabase_client.upsert_work_orders(work_orders)
            
            end_time = datetime.now(timezone.utc)
            
            if success:
                result = SyncResult(
                    table_name="work_orders",
                    status=SyncStatus.SUCCESS,
                    records_processed=len(work_orders),
                    start_time=start_time,
                    end_time=end_time
                )
                await self.supabase_client.update_sync_status("work_orders", "success")
                logging.info(f"Synced {len(work_orders)} work orders")
            else:
                result = SyncResult(
                    table_name="work_orders",
                    status=SyncStatus.ERROR,
                    records_processed=0,
                    error_message="Failed to upsert work orders",
                    start_time=start_time,
                    end_time=end_time
                )
                await self.supabase_client.update_sync_status("work_orders", "error")
                logging.error("Failed to sync work orders")
            
            return result
            
        except Exception as e:
            end_time = datetime.now(timezone.utc)
            result = SyncResult(
                table_name="work_orders",
                status=SyncStatus.ERROR,
                records_processed=0,
                error_message=str(e),
                start_time=start_time,
                end_time=end_time
            )
            await self.supabase_client.update_sync_status("work_orders", "error")
            logging.error(f"Work orders sync failed: {e}")
            return result
    
    async def sync_service_appointments(self) -> SyncResult:
        """Sync service appointments from Zoho to Supabase"""
        start_time = datetime.now(timezone.utc)
        
        try:
            # Update sync status
            await self.supabase_client.update_sync_status("service_appointments", "syncing")
            
            # Get service appointments from Zoho
            appointments = self.zoho_client.get_appointments(limit=self.batch_size)
            
            if not appointments:
                logging.info("No service appointments to sync")
                result = SyncResult(
                    table_name="service_appointments",
                    status=SyncStatus.SUCCESS,
                    records_processed=0,
                    start_time=start_time,
                    end_time=datetime.now(timezone.utc)
                )
                await self.supabase_client.update_sync_status("service_appointments", "success")
                return result
            
            # Upsert to Supabase
            success = await self.supabase_client.upsert_service_appointments(appointments)
            
            end_time = datetime.now(timezone.utc)
            
            if success:
                result = SyncResult(
                    table_name="service_appointments",
                    status=SyncStatus.SUCCESS,
                    records_processed=len(appointments),
                    start_time=start_time,
                    end_time=end_time
                )
                await self.supabase_client.update_sync_status("service_appointments", "success")
                logging.info(f"Synced {len(appointments)} service appointments")
            else:
                result = SyncResult(
                    table_name="service_appointments",
                    status=SyncStatus.ERROR,
                    records_processed=0,
                    error_message="Failed to upsert service appointments",
                    start_time=start_time,
                    end_time=end_time
                )
                await self.supabase_client.update_sync_status("service_appointments", "error")
                logging.error("Failed to sync service appointments")
            
            return result
            
        except Exception as e:
            end_time = datetime.now(timezone.utc)
            result = SyncResult(
                table_name="service_appointments",
                status=SyncStatus.ERROR,
                records_processed=0,
                error_message=str(e),
                start_time=start_time,
                end_time=end_time
            )
            await self.supabase_client.update_sync_status("service_appointments", "error")
            logging.error(f"Service appointments sync failed: {e}")
            return result
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status"""
        try:
            status = await self.supabase_client.get_sync_status()
            return {
                "is_running": self.is_running,
                "sync_interval": self.sync_interval,
                "tables": status
            }
        except Exception as e:
            logging.error(f"Failed to get sync status: {e}")
            return {
                "is_running": self.is_running,
                "sync_interval": self.sync_interval,
                "error": str(e)
            }
    
    async def trigger_manual_sync(self, force: bool = False) -> Dict[str, SyncResult]:
        """Trigger manual sync"""
        if self.is_running and not force:
            logging.warning("Sync is already running. Use force=True to override.")
            return {"error": SyncResult(
                table_name="manual_sync",
                status=SyncStatus.ERROR,
                records_processed=0,
                error_message="Sync is already running"
            )}
        
        logging.info("Triggering manual sync")
        return await self.sync_all()

# Test function
async def test_sync_manager():
    """Test the sync manager"""
    try:
        manager = SyncManager()
        print("✅ Sync manager initialized successfully")
        
        # Test getting sync status
        status = await manager.get_sync_status()
        print(f"✅ Sync status: {status}")
        
        # Test manual sync
        print("🔄 Testing manual sync...")
        results = await manager.trigger_manual_sync()
        print(f"✅ Manual sync completed: {results}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sync manager test failed: {e}")
        return False

if __name__ == "__main__":
    import os
    asyncio.run(test_sync_manager()) 