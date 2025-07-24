#!/usr/bin/env python3
"""
Simple data retrieval test
"""
import asyncio
from src.supabase_client import SupabaseClient

async def test_data_retrieval():
    """Test simple data retrieval from tables"""
    
    client = SupabaseClient()
    
    print("🔍 Testing data retrieval from zoho_fsm tables...")
    
    # Test 1: Get records from work_orders
    try:
        print("🔍 Test 1: Getting work_orders...")
        result = await client.get_records("zoho_fsm", "work_orders")
        print(f"✅ work_orders: {len(result) if isinstance(result, list) else 'No data'}")
    except Exception as e:
        print(f"❌ work_orders error: {e}")
    
    # Test 2: Get records from customers
    try:
        print("🔍 Test 2: Getting customers...")
        result = await client.get_records("zoho_fsm", "customers")
        print(f"✅ customers: {len(result) if isinstance(result, list) else 'No data'}")
    except Exception as e:
        print(f"❌ customers error: {e}")
    
    # Test 3: Get records from technicians
    try:
        print("🔍 Test 3: Getting technicians...")
        result = await client.get_records("zoho_fsm", "technicians")
        print(f"✅ technicians: {len(result) if isinstance(result, list) else 'No data'}")
    except Exception as e:
        print(f"❌ technicians error: {e}")
    
    # Test 4: Get records from service_appointments
    try:
        print("🔍 Test 4: Getting service_appointments...")
        result = await client.get_records("zoho_fsm", "service_appointments")
        print(f"✅ service_appointments: {len(result) if isinstance(result, list) else 'No data'}")
    except Exception as e:
        print(f"❌ service_appointments error: {e}")
    
    print("\n🎉 Data retrieval test completed!")

if __name__ == "__main__":
    asyncio.run(test_data_retrieval()) 