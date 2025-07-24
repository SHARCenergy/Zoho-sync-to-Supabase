#!/usr/bin/env python3
"""
Zoho FSM Client using the correct authentication method
"""

import requests
import os
from typing import Dict, List, Optional
import logging

class ZohoFSMClient:
    def __init__(self, org_id: str, access_token: str = None):
        """
        Initialize Zoho FSM client
        
        Args:
            org_id: Your Zoho organization ID
            access_token: Access token (will be refreshed if needed)
        """
        self.org_id = org_id
        self.access_token = access_token
        self.base_url = "https://www.zohoapis.com/fsm/v1"
        
        # Load credentials from environment
        self.client_id = os.getenv("ZOHO_CLIENT_ID")
        self.client_secret = os.getenv("ZOHO_CLIENT_SECRET")
        self.refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
        
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Missing Zoho credentials in environment variables")
        
        # Refresh token if not provided
        if not self.access_token:
            self.refresh_access_token()
    
    def refresh_access_token(self) -> str:
        """Refresh the access token using the refresh token"""
        url = "https://accounts.zoho.com/oauth/v2/token"
        data = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            self.access_token = result['access_token']
            return self.access_token
        else:
            raise Exception(f"Failed to refresh token: {response.status_code} - {response.text}")
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Make authenticated request to Zoho FSM API"""
        if not self.access_token:
            self.refresh_access_token()
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'Zoho-oauthtoken {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 401:
                # Token expired, refresh and retry
                self.refresh_access_token()
                headers['Authorization'] = f'Zoho-oauthtoken {self.access_token}'
                
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, params=params)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=headers, json=data)
                elif method.upper() == 'PUT':
                    response = requests.put(url, headers=headers, json=data)
                elif method.upper() == 'DELETE':
                    response = requests.delete(url, headers=headers)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise
    
    def get_workorders(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get work orders from FSM"""
        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._make_request('GET', 'Work_Orders', params=params)
        return response.get('data', [])
    
    def get_workorder(self, workorder_id: str) -> Dict:
        """Get a specific work order by ID"""
        response = self._make_request('GET', f'Work_Orders/{workorder_id}')
        return response.get('data', {})
    
    def create_workorder(self, workorder_data: Dict) -> Dict:
        """Create a new work order"""
        data = {'data': [workorder_data]}
        response = self._make_request('POST', 'Work_Orders', data=data)
        return response
    
    def update_workorder(self, workorder_id: str, workorder_data: Dict) -> Dict:
        """Update an existing work order"""
        data = {'data': [workorder_data]}
        response = self._make_request('PUT', f'Work_Orders/{workorder_id}', data=data)
        return response
    
    def get_customers(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get customers from FSM"""
        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._make_request('GET', 'customers', params=params)
        return response.get('customers', [])
    
    def get_customer(self, customer_id: str) -> Dict:
        """Get a specific customer by ID"""
        response = self._make_request('GET', f'customers/{customer_id}')
        return response.get('customer', {})
    
    def create_customer(self, customer_data: Dict) -> Dict:
        """Create a new customer"""
        data = {'customer': customer_data}
        response = self._make_request('POST', 'customers', data=data)
        return response
    
    def update_customer(self, customer_id: str, customer_data: Dict) -> Dict:
        """Update an existing customer"""
        data = {'customer': customer_data}
        response = self._make_request('PUT', f'customers/{customer_id}', data=data)
        return response
    
    def get_technicians(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get technicians from FSM"""
        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._make_request('GET', 'technicians', params=params)
        return response.get('technicians', [])
    
    def get_technician(self, technician_id: str) -> Dict:
        """Get a specific technician by ID"""
        response = self._make_request('GET', f'technicians/{technician_id}')
        return response.get('technician', {})
    
    def create_technician(self, technician_data: Dict) -> Dict:
        """Create a new technician"""
        data = {'technician': technician_data}
        response = self._make_request('POST', 'technicians', data=data)
        return response
    
    def update_technician(self, technician_id: str, technician_data: Dict) -> Dict:
        """Update an existing technician"""
        data = {'technician': technician_data}
        response = self._make_request('PUT', f'technicians/{technician_id}', data=data)
        return response
    
    def get_appointments(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get appointments from FSM"""
        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._make_request('GET', 'Service_Appointments', params=params)
        return response.get('data', [])
    
    def get_appointment(self, appointment_id: str) -> Dict:
        """Get a specific appointment by ID"""
        response = self._make_request('GET', f'Service_Appointments/{appointment_id}')
        return response.get('data', {})
    
    def create_appointment(self, appointment_data: Dict) -> Dict:
        """Create a new appointment"""
        data = {'data': [appointment_data]}
        response = self._make_request('POST', 'Service_Appointments', data=data)
        return response
    
    def update_appointment(self, appointment_id: str, appointment_data: Dict) -> Dict:
        """Update an existing appointment"""
        data = {'data': [appointment_data]}
        response = self._make_request('PUT', f'Service_Appointments/{appointment_id}', data=data)
        return response

# Test function
def test_fsm_connection():
    """Test the FSM connection"""
    try:
        org_id = os.getenv("ZOHO_ORG_ID")
        if not org_id:
            print("❌ ZOHO_ORG_ID not found in environment variables")
            return False
        
        client = ZohoFSMClient(org_id)
        print("✅ Zoho FSM client initialized successfully")
        
        # Test getting work orders
        try:
            workorders = client.get_workorders(limit=5)
            print(f"✅ Successfully retrieved {len(workorders)} work orders")
            return True
        except Exception as e:
            print(f"❌ Failed to retrieve work orders: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to initialize FSM client: {e}")
        return False

if __name__ == "__main__":
    test_fsm_connection() 