import httpx
import asyncio
from typing import Dict, List, Optional, Any
from loguru import logger
from .config import settings
from datetime import datetime, timedelta

class ZohoClient:
    def __init__(self):
        self.base_url = settings.zoho_base_url
        self.client_id = settings.zoho_client_id
        self.client_secret = settings.zoho_client_secret
        self.refresh_token = settings.zoho_refresh_token
        self.org_id = settings.zoho_org_id
        self.access_token = None
        self.token_expires_at = None
        
    async def _get_access_token(self) -> str:
        """Get or refresh access token"""
        if (self.access_token and self.token_expires_at and 
            datetime.now() < self.token_expires_at):
            return self.access_token
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.zoho.com/oauth/v2/token",
                data={
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "refresh_token"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.token_expires_at = datetime.now() + timedelta(hours=1)
                return self.access_token
            else:
                raise Exception(f"Failed to get access token: {response.text}")
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request to Zoho API"""
        token = await self._get_access_token()
        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "orgId": self.org_id,
            **kwargs.get("headers", {})
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, headers=headers, **kwargs
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                logger.error(f"Zoho API error: {response.status_code} - {response.text}")
                raise Exception(f"Zoho API error: {response.status_code}")
    
    # FSM-specific methods
    async def get_work_orders(self, modified_since: Optional[datetime] = None) -> List[Dict]:
        """Get work orders from Zoho FSM"""
        params = {}
        if modified_since:
            params["modified_time"] = modified_since.isoformat()
            
        return await self._make_request("GET", "fsm/v1/workorders", params=params)
    
    async def create_work_order(self, data: Dict) -> Dict:
        """Create work order in Zoho FSM"""
        return await self._make_request("POST", "fsm/v1/workorders", json=data)
    
    async def update_work_order(self, work_order_id: str, data: Dict) -> Dict:
        """Update work order in Zoho FSM"""
        return await self._make_request("PUT", f"fsm/v1/workorders/{work_order_id}", json=data)
    
    async def get_customers(self, modified_since: Optional[datetime] = None) -> List[Dict]:
        """Get customers from Zoho FSM"""
        params = {}
        if modified_since:
            params["modified_time"] = modified_since.isoformat()
            
        return await self._make_request("GET", "fsm/v1/customers", params=params)
    
    async def create_customer(self, data: Dict) -> Dict:
        """Create customer in Zoho FSM"""
        return await self._make_request("POST", "fsm/v1/customers", json=data)
    
    async def update_customer(self, customer_id: str, data: Dict) -> Dict:
        """Update customer in Zoho FSM"""
        return await self._make_request("PUT", f"fsm/v1/customers/{customer_id}", json=data)
    
    async def get_technicians(self, modified_since: Optional[datetime] = None) -> List[Dict]:
        """Get technicians from Zoho FSM"""
        params = {}
        if modified_since:
            params["modified_time"] = modified_since.isoformat()
            
        return await self._make_request("GET", "fsm/v1/technicians", params=params)
    
    async def create_technician(self, data: Dict) -> Dict:
        """Create technician in Zoho FSM"""
        return await self._make_request("POST", "fsm/v1/technicians", json=data)
    
    async def update_technician(self, technician_id: str, data: Dict) -> Dict:
        """Update technician in Zoho FSM"""
        return await self._make_request("PUT", f"fsm/v1/technicians/{technician_id}", json=data)
    
    async def get_appointments(self, modified_since: Optional[datetime] = None) -> List[Dict]:
        """Get appointments from Zoho FSM"""
        params = {}
        if modified_since:
            params["modified_time"] = modified_since.isoformat()
            
        return await self._make_request("GET", "fsm/v1/appointments", params=params)
    
    async def create_appointment(self, data: Dict) -> Dict:
        """Create appointment in Zoho FSM"""
        return await self._make_request("POST", "fsm/v1/appointments", json=data)
    
    async def update_appointment(self, appointment_id: str, data: Dict) -> Dict:
        """Update appointment in Zoho FSM"""
        return await self._make_request("PUT", f"fsm/v1/appointments/{appointment_id}", json=data) 