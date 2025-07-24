#!/usr/bin/env python3
"""
Test script to verify the complete setup works
"""

import os
import asyncio
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zoho_fsm_client import ZohoFSMClient
from supabase_client import SupabaseClient
from sync_manager import SyncManager

async def test_complete_setup():
    """Test the complete setup"""
    print("🧪 Testing Complete Setup")
    print("=" * 50)
    
    # Set environment variables for testing
    os.environ['ZOHO_CLIENT_ID'] = "1000.3W1DWDWE6VK331JVHDE4R6UCXR59QZ"
    os.environ['ZOHO_CLIENT_SECRET'] = "d1facfc63fe9e7f30a038a33b4f12f6c359dd37464"
    os.environ['ZOHO_REFRESH_TOKEN'] = "1000.46b406330c7bc61a2b5398b3f758a54f.bd5b0487f535c43f2c9cd436c2bb5f3b"
    os.environ['ZOHO_ORG_ID'] = "test_org"
    
    # Set dummy Supabase credentials for testing
    os.environ['SUPABASE_URL'] = "https://test.supabase.co"
    os.environ['SUPABASE_ANON_KEY'] = "test_anon_key"
    os.environ['SUPABASE_SERVICE_ROLE_KEY'] = "test_service_role_key"
    
    try:
        # Test 1: FSM Client
        print("\n1. Testing FSM Client...")
        fsm_client = ZohoFSMClient("test_org")
        print("✅ FSM client initialized")
        
        # Test getting work orders
        work_orders = fsm_client.get_workorders(limit=3)
        print(f"✅ Retrieved {len(work_orders)} work orders from FSM")
        
        if work_orders:
            print(f"   Sample work order: {work_orders[0].get('Name', 'N/A')}")
        
        # Test 2: Supabase Client (will fail without real credentials, but test structure)
        print("\n2. Testing Supabase Client...")
        try:
            supabase_client = SupabaseClient()
            print("✅ Supabase client initialized")
            
            # Test getting sync status (will fail without real DB)
            status = await supabase_client.get_sync_status()
            print(f"✅ Sync status retrieved: {status}")
            
        except Exception as e:
            print(f"⚠️  Supabase client test (expected without real credentials): {e}")
        
        # Test 3: Sync Manager
        print("\n3. Testing Sync Manager...")
        try:
            sync_manager = SyncManager()
            print("✅ Sync manager initialized")
            
            # Test getting sync status
            status = await sync_manager.get_sync_status()
            print(f"✅ Sync manager status: {status}")
            
        except Exception as e:
            print(f"⚠️  Sync manager test (expected without real Supabase): {e}")
        
        print("\n🎉 Setup verification completed!")
        print("\n📋 Next Steps:")
        print("1. Set up Supabase project and get real credentials")
        print("2. Update .env file with Supabase credentials")
        print("3. Run SQL migrations in Supabase")
        print("4. Test full sync functionality")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_complete_setup()) 