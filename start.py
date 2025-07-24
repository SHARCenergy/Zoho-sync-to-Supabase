#!/usr/bin/env python3
"""
Startup script for Zoho-Supabase sync service
"""

import os
import sys
import asyncio
from pathlib import Path
from loguru import logger

def check_environment():
    """Check if environment is properly configured"""
    required_vars = [
        'ZOHO_CLIENT_ID',
        'ZOHO_CLIENT_SECRET', 
        'ZOHO_REFRESH_TOKEN',
        'ZOHO_ORG_ID',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY',
        'WEBHOOK_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.info("Please copy env.example to .env and configure your credentials")
        return False
    
    logger.success("Environment variables configured")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import supabase
        import loguru
        logger.success("All dependencies installed")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.info("Please run: pip install -r requirements.txt")
        return False

async def main():
    """Main startup function"""
    logger.info("Starting Zoho-Supabase Sync Service...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and start the service
    try:
        from main import main as start_service
        await start_service()
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 