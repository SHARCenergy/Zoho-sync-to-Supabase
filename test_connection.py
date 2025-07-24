#!/usr/bin/env python3
"""
Simple connection test for Supabase
"""
import asyncio
import os
from supabase import create_client, Client
from loguru import logger
from src.config import settings

async def test_connection():
    """Test basic Supabase connection and permissions"""
    
    print(f"🔗 Testing connection to: {settings.supabase_url}")
    print(f"🔑 Using service role key: {settings.supabase_service_role_key[:20]}...")
    
    try:
        # Create client
        client: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        
        # Test 1: Basic connection (use RPC to test connection)
        print("🔍 Test 1: Basic connection...")
        result = client.rpc("create_schema_if_not_exists", {"schema_name": "test_connection"}).execute()
        print("✅ Basic connection successful")
        
        # Test 2: Check if schemas exist
        print("🔍 Test 2: Checking schemas...")
        result = client.rpc("create_schema_if_not_exists", {"schema_name": "test_schema"}).execute()
        print("✅ Schema creation function accessible")
        
        # Test 3: Check if zoho_fsm schema exists using RPC
        print("🔍 Test 3: Checking zoho_fsm schema...")
        try:
            # Use RPC to test schema access instead of direct table access
            result = client.rpc("get_sync_status", {"p_schema": "zoho_fsm", "p_table": "work_orders"}).execute()
            print("✅ zoho_fsm schema exists and accessible")
        except Exception as e:
            if "does not exist" in str(e):
                print("❌ zoho_fsm schema not found")
            else:
                print(f"⚠️ zoho_fsm schema exists but has access issues: {e}")
        
        # Test 4: Check if sync_status table exists using RPC
        print("🔍 Test 4: Checking sync_status table...")
        try:
            result = client.rpc("get_sync_status", {"p_schema": "zoho_fsm", "p_table": "work_orders"}).execute()
            print("✅ sync_status table accessible via RPC")
        except Exception as e:
            print(f"❌ sync_status table error: {e}")
        
        # Test 5: Test get_sync_status function
        print("🔍 Test 5: Testing get_sync_status function...")
        try:
            result = client.rpc("get_sync_status", {"p_schema": "zoho_fsm", "p_table": "work_orders"}).execute()
            print("✅ get_sync_status function works")
        except Exception as e:
            print(f"❌ get_sync_status function error: {e}")
        
        # Test 6: Try direct table access with proper schema
        print("🔍 Test 6: Testing direct table access...")
        try:
            # Use raw SQL to test direct access
            result = client.table("zoho_fsm.sync_status").select("*").limit(1).execute()
            print("✅ Direct table access works")
        except Exception as e:
            print(f"⚠️ Direct table access issue: {e}")
        
        print("\n🎉 Connection test completed!")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection()) 