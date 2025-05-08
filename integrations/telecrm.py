import requests
import logging
from typing import Dict, List, Any, Optional
import json
import os

logger = logging.getLogger(__name__)

class TeleCRMClient:
    """
    Client for interacting with TeleCRM API
    """
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Check if we're using a demo key
        self.is_demo = "demo" in api_key.lower()
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Helper method to make requests to TeleCRM API
        """
        # If using demo key, return mock data
        if self.is_demo:
            return self._get_mock_response(endpoint, method, params)
            
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when calling TeleCRM API: {e}")
            if response.text:
                logger.error(f"Response content: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling TeleCRM API: {e}")
            raise
    
    def _get_mock_response(self, endpoint: str, method: str, params: Optional[Dict] = None) -> Dict:
        """
        Return mock data for demo mode
        """
        logger.info(f"DEMO MODE: Returning mock data for {method} {endpoint}")
        
        # Mock leads data
        if endpoint.startswith('/leads'):
            if endpoint == "/leads" and method == "GET":
                # Return a list of mock leads
                return {
                    "data": [
                        {
                            "id": "lead1",
                            "name": "John Doe",
                            "email": "john.doe@example.com",
                            "phone": "1234567890",
                            "company": "ABC Corp",
                            "status": "New",
                            "source": "Website",
                            "address": "123 Main St",
                            "city": "New York",
                            "country": "USA",
                            "custom_fields": {
                                "Last Contact": "2023-06-15",
                                "Interest": "Product Demo"
                            }
                        },
                        {
                            "id": "lead2",
                            "name": "Jane Smith",
                            "email": "jane.smith@example.com",
                            "phone": "0987654321",
                            "company": "XYZ Inc",
                            "status": "Qualified",
                            "source": "Referral",
                            "address": "456 Park Ave",
                            "city": "Boston",
                            "country": "USA",
                            "custom_fields": {
                                "Last Contact": "2023-06-20",
                                "Interest": "Pricing"
                            }
                        }
                    ],
                    "total": 2,
                    "page": 1,
                    "per_page": 100
                }
            elif "/leads/" in endpoint and method == "GET":
                # Return a specific lead
                lead_id = endpoint.split("/")[-1]
                return {
                    "id": lead_id,
                    "name": "John Doe" if lead_id == "lead1" else "Jane Smith",
                    "email": f"demo_lead_{lead_id}@example.com",
                    "phone": "1234567890",
                    "company": "Demo Company",
                    "status": "New",
                    "source": "Website",
                    "address": "123 Main St",
                    "city": "New York",
                    "country": "USA",
                    "custom_fields": {
                        "Last Contact": "2023-06-15",
                        "Interest": "Product Demo"
                    }
                }
        
        # Mock segments data
        elif endpoint.startswith('/segments'):
            if endpoint == "/segments" and method == "GET":
                # Return a list of mock segments
                return [
                    {
                        "id": "segment1",
                        "name": "New Leads"
                    },
                    {
                        "id": "segment2",
                        "name": "Qualified Leads"
                    }
                ]
            elif "/segments/" in endpoint and method == "GET":
                # Return a specific segment
                segment_id = endpoint.split("/")[-1]
                return {
                    "id": segment_id,
                    "name": f"Demo Segment {segment_id}",
                    "criteria": {
                        "status": "New" if segment_id == "segment1" else "Qualified"
                    }
                }
        
        # Default empty response
        return {}
    
    def get_leads(self, filter_criteria: Optional[Dict] = None, page: int = 1, per_page: int = 100) -> Dict:
        """
        Get leads from TeleCRM with optional filtering
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        # Add filter criteria to params if provided
        if filter_criteria:
            for key, value in filter_criteria.items():
                params[key] = value
        
        return self._make_request("GET", "/leads", params=params)
    
    def get_lead_by_id(self, lead_id: str) -> Dict:
        """
        Get a specific lead by ID
        """
        return self._make_request("GET", f"/leads/{lead_id}")
    
    def get_leads_by_segment(self, segment_id: str, page: int = 1, per_page: int = 100) -> Dict:
        """
        Get leads that belong to a specific segment
        """
        params = {
            "segment_id": segment_id,
            "page": page,
            "per_page": per_page
        }
        
        return self._make_request("GET", "/leads", params=params)
    
    def get_all_segments(self) -> List[Dict]:
        """
        Get all segments defined in TeleCRM
        """
        return self._make_request("GET", "/segments")
    
    def get_segment_by_id(self, segment_id: str) -> Dict:
        """
        Get a specific segment by ID
        """
        return self._make_request("GET", f"/segments/{segment_id}")
    
    def get_all_leads_by_segment(self, segment_id: str, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Get all leads in a segment with pagination handling
        """
        # For demo mode, return a simpler result without paging
        if self.is_demo:
            response = self.get_leads_by_segment(segment_id)
            return response.get("data", [])
            
        all_leads = []
        page = 1
        per_page = 100
        
        while True:
            response = self.get_leads_by_segment(segment_id, page, per_page)
            leads = response.get("data", [])
            
            if not leads:
                break
                
            all_leads.extend(leads)
            
            # Check if we've reached the last page
            if len(leads) < per_page:
                break
                
            page += 1
            
        return all_leads 