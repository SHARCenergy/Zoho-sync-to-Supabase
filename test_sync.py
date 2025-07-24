#!/usr/bin/env python3
"""
Simple test script to verify the Zoho-Supabase sync functionality
"""

import asyncio
import httpx
from loguru import logger

async def test_api_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        try:
            # Test health endpoint
            logger.info("Testing health endpoint...")
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                logger.success("Health endpoint working")
            else:
                logger.error(f"Health endpoint failed: {response.status_code}")
            
            # Test root endpoint
            logger.info("Testing root endpoint...")
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                logger.success("Root endpoint working")
                data = response.json()
                logger.info(f"Available endpoints: {list(data.get('endpoints', {}).keys())}")
            else:
                logger.error(f"Root endpoint failed: {response.status_code}")
            
            # Test sync status endpoint
            logger.info("Testing sync status endpoint...")
            response = await client.get(f"{base_url}/sync/status")
            if response.status_code == 200:
                logger.success("Sync status endpoint working")
                data = response.json()
                logger.info(f"Sync status: {data}")
            else:
                logger.error(f"Sync status endpoint failed: {response.status_code}")
            
        except httpx.ConnectError:
            logger.error("Could not connect to API server. Make sure it's running on localhost:8000")
        except Exception as e:
            logger.error(f"Test failed: {e}")

async def test_manual_sync():
    """Test manual sync trigger"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        try:
            logger.info("Testing manual sync trigger...")
            response = await client.post(
                f"{base_url}/sync/trigger",
                json={"force": True}
            )
            if response.status_code == 200:
                logger.success("Manual sync trigger working")
                data = response.json()
                logger.info(f"Sync response: {data}")
            else:
                logger.error(f"Manual sync trigger failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Manual sync test failed: {e}")

async def main():
    """Main test function"""
    logger.info("Starting Zoho-Supabase sync tests...")
    
    # Test API endpoints
    await test_api_endpoints()
    
    # Test manual sync (optional - requires proper credentials)
    # await test_manual_sync()
    
    logger.info("Tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 