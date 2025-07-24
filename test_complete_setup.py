#!/usr/bin/env python3
"""
Complete Setup Test
This script tests the entire system after Supabase migrations are applied.
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv
from supabase import create_client, Client
from loguru import logger

# Load environment variables
load_dotenv()

def test_supabase_functions():
    """Test Supabase functions after migrations"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        supabase: Client = create_client(supabase_url, supabase_service_role_key)
        
        # Test get_sync_status function
        logger.info("Testing get_sync_status function...")
        result = supabase.rpc('get_sync_status', {
            'p_schema': 'zoho_fsm',
            'p_table': 'work_orders'
        }).execute()
        logger.success("✅ get_sync_status function working")
        
        # Test update_sync_status function
        logger.info("Testing update_sync_status function...")
        supabase.rpc('update_sync_status', {
            'p_last_sync': '2024-01-01T00:00:00Z',
            'p_schema': 'zoho_fsm',
            'p_status': 'test',
            'p_table': 'work_orders'
        }).execute()
        logger.success("✅ update_sync_status function working")
        
        # Test table access
        logger.info("Testing table access...")
        result = supabase.table('zoho_fsm.sync_status').select('*').execute()
        logger.success("✅ Table access working")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Supabase test failed: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints"""
    try:
        async with httpx.AsyncClient() as client:
            base_url = "http://localhost:8000"
            
            # Test health endpoint
            response = await client.get(f'{base_url}/health')
            if response.status_code == 200:
                logger.success("✅ Health endpoint working")
            else:
                logger.error(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test sync status endpoint
            response = await client.get(f'{base_url}/sync/status')
            if response.status_code == 200:
                logger.success("✅ Sync status endpoint working")
            else:
                logger.error(f"❌ Sync status endpoint failed: {response.status_code}")
                return False
            
            # Test manual sync trigger
            response = await client.post(f'{base_url}/sync/trigger', json={"force": False})
            if response.status_code == 200:
                logger.success("✅ Manual sync trigger working")
            else:
                logger.error(f"❌ Manual sync trigger failed: {response.status_code}")
                return False
            
            return True
            
    except Exception as e:
        logger.error(f"❌ API test failed: {e}")
        return False

async def main():
    """Main test function"""
    logger.info("🚀 Starting complete setup test...")
    
    # Test 1: Supabase functions
    logger.info("\n=== Testing Supabase Functions ===")
    supabase_ok = test_supabase_functions()
    
    # Test 2: API endpoints
    logger.info("\n=== Testing API Endpoints ===")
    api_ok = await test_api_endpoints()
    
    # Summary
    logger.info("\n=== Test Summary ===")
    if supabase_ok and api_ok:
        logger.success("🎉 All tests passed! Your setup is complete.")
        logger.info("Next steps:")
        logger.info("1. Start the sync service: python main.py")
        logger.info("2. Monitor the logs for sync activity")
        logger.info("3. Check the API documentation at http://localhost:8000/docs")
    else:
        logger.error("❌ Some tests failed. Please check the setup.")
        if not supabase_ok:
            logger.error("   - Supabase functions need to be created")
            logger.error("   - Run the migrations in SUPABASE_SETUP_COMPLETE.md")
        if not api_ok:
            logger.error("   - API server may not be running")
            logger.error("   - Start with: python main.py")

if __name__ == "__main__":
    asyncio.run(main()) 