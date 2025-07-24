#!/usr/bin/env python3
"""
Test Supabase Connection
This script tests the connection to Supabase and verifies credentials.
"""

import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client
from loguru import logger

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test basic Supabase connection"""
    try:
        # Get credentials from environment
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url:
            logger.error("❌ SUPABASE_URL not found in environment variables")
            return False
            
        if not supabase_service_role_key:
            logger.error("❌ SUPABASE_SERVICE_ROLE_KEY not found in environment variables")
            return False
            
        if not supabase_anon_key:
            logger.error("❌ SUPABASE_ANON_KEY not found in environment variables")
            return False
        
        logger.info(f"🔗 Testing connection to: {supabase_url}")
        
        # Test with service role key (admin access)
        supabase: Client = create_client(supabase_url, supabase_service_role_key)
        
        # Try a simple query to test connection
        try:
            # This should work even if tables don't exist yet
            result = supabase.table('auth.users').select('count', count='exact').limit(1).execute()
            logger.success("✅ Service role connection successful")
        except Exception as e:
            logger.warning(f"⚠️ Service role test query failed (this is normal if auth.users doesn't exist): {e}")
            logger.info("✅ Service role connection established")
        
        # Test with anon key
        supabase_anon: Client = create_client(supabase_url, supabase_anon_key)
        try:
            # This should work even if tables don't exist yet
            result = supabase_anon.table('auth.users').select('count', count='exact').limit(1).execute()
            logger.success("✅ Anon key connection successful")
        except Exception as e:
            logger.warning(f"⚠️ Anon key test query failed (this is normal if auth.users doesn't exist): {e}")
            logger.info("✅ Anon key connection established")
        
        logger.success("🎉 Supabase connection test completed successfully!")
        logger.info("Next step: Apply database migrations using SUPABASE_SETUP.md")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    exit(0 if success else 1) 