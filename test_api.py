#!/usr/bin/env python3
"""
Test script for the Zoho Sync API
Verifies all endpoints are working correctly after database setup
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

async def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

async def test_sync_status():
    """Test the sync status endpoint"""
    print("\n🔍 Testing sync status endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/sync/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Sync status retrieved: {json.dumps(data, indent=2)}")
                return True
            else:
                print(f"❌ Sync status failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Sync status error: {e}")
        return False

async def test_manual_sync():
    """Test manual sync trigger"""
    print("\n🔍 Testing manual sync trigger...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/sync/start")
            if response.status_code in [200, 202]:
                data = response.json()
                print(f"✅ Manual sync triggered: {data}")
                return True
            else:
                print(f"❌ Manual sync failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Manual sync error: {e}")
        return False

async def test_data_endpoints():
    """Test data retrieval endpoints"""
    print("\n🔍 Testing data endpoints...")
    
    # Test FSM tables
    fsm_tables = ['work_orders', 'service_appointments', 'customers', 'technicians']
    
    for table in fsm_tables:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BASE_URL}/data/zoho_fsm/{table}")
                if response.status_code == 200:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else 0
                    print(f"✅ {table}: {count} records")
                else:
                    print(f"⚠️  {table}: {response.status_code}")
        except Exception as e:
            print(f"❌ {table} error: {e}")

async def test_database_functions():
    """Test database functions directly"""
    print("\n🔍 Testing database functions...")
    
    try:
        from src.supabase_client import SupabaseClient
        
        supabase_client = SupabaseClient()
        
        # Test get_sync_status function
        result = await supabase_client.get_sync_status('zoho_fsm', 'work_orders')
        
        print(f"✅ Database function test: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Database function error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting API Tests")
    print("=" * 50)
    
    # Check if API is running
    print("🔍 Checking if API is running...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ API is running")
            else:
                print("❌ API is not responding correctly")
                print("Please start the API with: python main.py")
                return
    except Exception as e:
        print("❌ API is not running")
        print("Please start the API with: python main.py")
        return
    
    # Run tests
    tests = [
        test_health(),
        test_sync_status(),
        test_manual_sync(),
        test_data_endpoints(),
        test_database_functions()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for r in results if r is True)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is working correctly.")
        print("\nNext steps:")
        print("1. The API is ready for production use")
        print("2. You can start syncing data from Zoho")
        print("3. Monitor the sync status via API endpoints")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify your environment variables are set correctly")
        print("2. Check that the database schema was applied successfully")
        print("3. Review the application logs in sync.log")

if __name__ == "__main__":
    asyncio.run(main()) 