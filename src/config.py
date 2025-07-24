from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Zoho Configuration
    zoho_client_id: str
    zoho_client_secret: str
    zoho_refresh_token: str
    zoho_org_id: str
    zoho_base_url: str = "https://www.zohoapis.com"
    
    # Supabase Configuration
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    
    # Sync Configuration
    sync_interval: int = 300  # 5 minutes
    webhook_secret: str
    max_retries: int = 3
    batch_size: int = 100
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "sync.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 