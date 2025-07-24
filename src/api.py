from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
from loguru import logger
from .sync_manager import SyncManager
from .config import settings

app = FastAPI(title="Zoho-Supabase Sync API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize sync manager
sync_manager = SyncManager()

class SyncRequest(BaseModel):
    force: bool = False

class WebhookData(BaseModel):
    event_type: str
    data: Dict
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """Initialize sync manager on startup"""
    await sync_manager.initialize()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/sync/trigger")
async def trigger_sync(background_tasks: BackgroundTasks, request: SyncRequest):
    """Trigger manual sync"""
    try:
        background_tasks.add_task(sync_manager.trigger_manual_sync)
        return {"message": "Sync triggered successfully", "force": request.force}
    except Exception as e:
        logger.error(f"Error triggering sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync/status")
async def get_sync_status():
    """Get current sync status"""
    try:
        status = {}
        schemas = ["zoho_fsm", "zoho_crm", "zoho_inventory"]
        
        for schema in schemas:
            status[schema] = {}
            tables = ["work_orders", "customers", "technicians", "appointments"]
            
            for table in tables:
                try:
                    table_status = await sync_manager.supabase_client.get_sync_status(schema, table)
                    status[schema][table] = table_status
                except:
                    status[schema][table] = {"status": "unknown"}
        
        return status
    except Exception as e:
        logger.error(f"Error getting sync status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/zoho")
async def zoho_webhook(data: WebhookData):
    """Handle Zoho webhooks for real-time updates"""
    try:
        logger.info(f"Received Zoho webhook: {data.event_type}")
        
        # Process webhook based on event type
        if data.event_type == "work_order_updated":
            await sync_manager.sync_fsm_data()
        elif data.event_type == "customer_updated":
            await sync_manager.sync_fsm_data()
        # Add more event types as needed
        
        return {"message": "Webhook processed successfully"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs(limit: int = 100):
    """Get recent sync logs"""
    try:
        # This would typically query a log table in Supabase
        # For now, return a placeholder
        return {"logs": [], "message": "Log retrieval not implemented yet"}
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/start")
async def start_continuous_sync(background_tasks: BackgroundTasks):
    """Start continuous sync"""
    try:
        background_tasks.add_task(sync_manager.start_continuous_sync)
        return {"message": "Continuous sync started"}
    except Exception as e:
        logger.error(f"Error starting continuous sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/stop")
async def stop_continuous_sync():
    """Stop continuous sync"""
    try:
        await sync_manager.stop_continuous_sync()
        return {"message": "Continuous sync stopped"}
    except Exception as e:
        logger.error(f"Error stopping continuous sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Zoho-Supabase Sync API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "sync_trigger": "/sync/trigger",
            "sync_status": "/sync/status",
            "sync_start": "/sync/start",
            "sync_stop": "/sync/stop",
            "webhook": "/webhook/zoho",
            "logs": "/logs"
        }
    } 