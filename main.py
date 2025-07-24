import asyncio
import uvicorn
from loguru import logger
from src.api import app
from src.sync_manager import SyncManager
from src.config import settings

async def main():
    """Main application entry point"""
    logger.info("Starting Zoho-Supabase Sync Service...")
    
    # Configure logging
    logger.add(
        settings.log_file,
        rotation="1 day",
        retention="7 days",
        level=settings.log_level
    )
    
    # Start the FastAPI server
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower()
    )
    
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main()) 